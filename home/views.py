import json

# from django.core.serializers import serialize
from django.http.response import Http404, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
# from django.http import JsonResponse
# from django.contrib.auth.models import User

from leads.models import Lead
from users.models import UserProfile

from .forms import AddCustomFieldForm
from .models import CustomField, CustomFieldChoise, LeadStage, StageElementIndexLogic, StageIndexOrder
from .utils import sortQueryObj


@login_required(login_url='login')
def homePage(request):
    user = request.user
    loggedInUser = UserProfile.objects.get(user=user)
    context = {
        "loggedInUser": loggedInUser,
    }
    return render(request, 'home/home_page.html', context)


@login_required(login_url='login')
def companySetting(request):
    loggedInUser = UserProfile.objects.get(user=request.user)
    company = loggedInUser.company
    stages = LeadStage.objects.filter(company=company)

    orderIndexObj, created = StageIndexOrder.objects.get_or_create(
        company=company)

    orderIndexList = []
    if not created:
        orderIndexList = orderIndexObj.reorder_string.split(',')
    sortedStages = sortQueryObj(stages, orderIndexList)
    # w = [x for _, x in sorted(zip(Y, orderIndexList))]

    # print(stages)
    # Z = [x for _, x in sorted(zip(Y, X))]
    customFields = CustomField.objects.filter(company=company)

    context = {
        "sortedStages": sortedStages,
        "loggedInUser": loggedInUser,
        "custom_field_form": AddCustomFieldForm(),
        "customFields": customFields,
    }
    return render(request, 'home/company_setting_page.html', context)


# Adding stages for lead in company setting page
@login_required(login_url='login')
def addStage(request):
    if request.method == 'POST':
        loggedInUser = UserProfile.objects.get(user=request.user)
        company = loggedInUser.company
        newStageObj = LeadStage.objects.create(
            company=company,
            stage_label=request.POST['new_lead_stage'],
            added_by=request.user,
        )

        stageOrderIndex, created = StageIndexOrder.objects.get_or_create(
            company=company)
        if created or stageOrderIndex.reorder_string == '' or (
                stageOrderIndex.reorder_string is None):
            stageOrderIndex.reorder_string = str(newStageObj.id)
        else:
            stageOrderIndex.reorder_string = stageOrderIndex.reorder_string + \
                ',' + str(newStageObj.id)
        stageOrderIndex.save()

        # Create a Element index Logic table
        StageElementIndexLogic.objects.create(
            company=company, stage=newStageObj)
        # print("saved")
        # print("label created: ", newStageObj)
        return redirect('company_setting')


# Updating order of stages in company setting page by dragging and dropping
@login_required(login_url='login')
def updateStageOrder(request):
    if request.method == 'POST':
        loggedInUser = UserProfile.objects.get(user=request.user)
        stageOrderIndex = StageIndexOrder.objects.get(
            company=loggedInUser.company)
        data = json.loads(request.body)
        draggedItemId = data['draggedItemId']
        oldIndexItem = data['oldIndexItem']
        newIndexItem = data['newIndexItem']

        # Split string by comma
        orderList = stageOrderIndex.reorder_string.split(',')
        # print("orderList1: ", orderList)

        # Delete old index of dragged element
        del orderList[oldIndexItem]
        # print("orderList2: ", orderList)

        # Add dragged element to new index
        orderList.insert(newIndexItem, draggedItemId)
        # print("orderList3: ", orderList)
        newStr = ",".join(orderList)
        # print("new str: ", newStr)
        stageOrderIndex.reorder_string = newStr
        stageOrderIndex.save()

        return JsonResponse({"msg": "success"})


# Delete stage from settings if there is no leads in the stage
@login_required(login_url='login')
def deleteStage(request, stage_pk):
    if request.method == 'POST':
        loggedInUser = UserProfile.objects.get(user=request.user)
        company = loggedInUser.company

        stage = get_object_or_404(LeadStage, id=stage_pk)
        if company != stage.company:
            return HttpResponseForbidden()

        try:
            stageOrder = StageElementIndexLogic.objects.get(stage=stage_pk)
        except StageElementIndexLogic.DoesNotExist:
            stage.delete()
            return JsonResponse({
                "success": True,
                "msg": "Successfully deleted!!",
            })

        if stageOrder.element_index_logic == '' or (
                stageOrder.element_index_logic is None):
            stage.delete()

            stageLogicOrder = StageIndexOrder.objects.get(company=company)
            logicOrderStrList = stageLogicOrder.reorder_string.split(',')

            # print("logicOrderStrList: ", logicOrderStrList)
            logicOrderStrList.remove(str(stage_pk))
            # print(logicOrderStrList)
            newStrOrder = ",".join(logicOrderStrList)
            # print("newStrOrder: ", newStrOrder)
            stageLogicOrder.reorder_string = newStrOrder
            stageLogicOrder.save()
            return JsonResponse({
                "success": True,
                "msg": "Successfully deleted!!",
            })
        else:
            return JsonResponse({
                "success": False,
                "msg": "Can't delete this stage. Please move all the leads inside of this stage and try again."
            })


# Move leads from one stage to another stage
@login_required(login_url='login')
def moveStageLead(request):
    if request.method == 'POST':
        loggedInUser = UserProfile.objects.get(user=request.user)
        company = loggedInUser.company
        movedFrom = request.POST.get('stage_moved_from')
        movedTo = request.POST.get('stage_moved_to')
        # print(movedFrom, '-', movedTo)

        movedFromIndexLogic = StageElementIndexLogic.objects.get(
            company=company, stage=movedFrom)
        movedToIndexLogic = StageElementIndexLogic.objects.get(
            company=company, stage=movedTo)

        print(movedFromIndexLogic.element_index_logic,
              '-', movedToIndexLogic.element_index_logic)

        # Update status of all the leads which are moved
        newStage = LeadStage.objects.get(id=movedTo)
        # print(newStage.stage_label)

        leadIds = movedFromIndexLogic.element_index_logic.split(',')
        # print("leadIds: ", leadIds)

        for leadId in leadIds:
            newLead = Lead.objects.get(id=leadId)
            # print("lead Saved: ", newLead.stage.stage_label)
            newLead.stage = newStage
            newLead.save()
            # print("lead updated: ", newLead.stage.stage_label)

        # Move the order indexing from movedFrom to movedTo .
        if movedToIndexLogic.element_index_logic is None or (
                movedToIndexLogic.element_index_logic == ''):
            movedToIndexLogic.element_index_logic = movedFromIndexLogic.element_index_logic
        else:
            movedToIndexLogic.element_index_logic = movedToIndexLogic.element_index_logic + \
                ',' + movedFromIndexLogic.element_index_logic
        movedToIndexLogic.save()

        # empty the logic order of MovedFrom
        movedFromIndexLogic.element_index_logic = ''
        movedFromIndexLogic.save()

        return redirect('company_setting')


@login_required(login_url='login')
def createCustomField(request):
    if request.method == 'POST':
        loggedInUser = UserProfile.objects.get(user=request.user)
        print(request.POST)
        extra_field_size = len(request.POST)-3
        print("extra_field_size: ", extra_field_size)

        if request.POST.get('field_type') == 'drop_down' or (
                request.POST.get('field_type') == 'drop_down'):
            if(extra_field_size <= 0):
                return redirect('company_setting')

        form = AddCustomFieldForm(request.POST)
        if form.is_valid():
            print("form Valid")
            customFieldObj = form.save(commit=False)
            customFieldObj.company = loggedInUser.company
            customFieldObj.save()

            if extra_field_size > 0:
                for index in range(extra_field_size):
                    option_choise = request.POST.get(f"option_{index}")
                    if option_choise:
                        CustomFieldChoise.objects.create(
                            custom_field=customFieldObj,
                            choise_name=option_choise,
                        )

        return redirect('company_setting')
