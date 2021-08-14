import json
import uuid

from django.core.serializers import serialize
from django.http.response import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required

# from django.contrib.auth.models import User

from leads.models import Lead
from users.models import Company, UserProfile

from .forms import AddCustomFieldForm
from .models import CustomField, CustomFieldChoise, LeadStage
# from .gmail_api import syncGmailAPI
from .utils import sortQueryObj


@login_required(login_url='login')
def homePage(request, api_key=None):
    user = request.user
    loggedInUser = UserProfile.objects.get(user=user)

    # service = syncGmailAPI(user)
    # print("credssss: ", service)
    randomStr = uuid.uuid4()
    print("randomStr: ", len(str(randomStr)), '-', randomStr)
    context = {
        "loggedInUser": loggedInUser,
    }
    return render(request, 'home/home_page.html', context)


@login_required(login_url='login')
def companySetting(request):
    loggedInUser = UserProfile.objects.get(user=request.user)
    company = loggedInUser.company
    stages = LeadStage.objects.filter(company=company)

    # orderIndexObj, created = StageIndexOrder.objects.get_or_create(
    #     company=company)

    # orderIndexList = []
    # if not created:
    #     orderIndexList = orderIndexObj.reorder_string.split(',')
    # sortedStages = sortQueryObj(stages, orderIndexList)

    stageReorderLogic = company.stage_reorder_logic
    # print("stageReorderLogic: ", stageReorderLogic)
    if stageReorderLogic.strip() != '':
        sortedStages = sortQueryObj(stages, stageReorderLogic.split(','))
    else:
        sortedStages = []

    # print("sortedStages: ", sortedStages)

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

        stageReorderLogic = company.stage_reorder_logic
        if stageReorderLogic.strip() == '':
            company.stage_reorder_logic = str(newStageObj.id)
        else:
            company.stage_reorder_logic = f"{stageReorderLogic},{str(newStageObj.id)}"
        company.save()

        return redirect('company_setting')


# Updating order of stages in company setting page whem dragged
@login_required(login_url='login')
def updateStageOrder(request):
    if request.method == 'POST':
        loggedInUser = UserProfile.objects.get(user=request.user)
        company = loggedInUser.company
        stageReorderLogic = company.stage_reorder_logic

        data = json.loads(request.body)
        draggedItemId = data['draggedItemId']
        oldIndexItem = data['oldIndexItem']
        newIndexItem = data['newIndexItem']

        # Split string by comma
        orderList = stageReorderLogic.split(',')
        # print("orderList1: ", orderList)

        # Delete old index of dragged element
        del orderList[oldIndexItem]
        # print("orderList2: ", orderList)

        # Add dragged element to new index
        orderList.insert(newIndexItem, draggedItemId)
        # print("orderList3: ", orderList)
        newStr = ",".join(orderList)
        # print("new str: ", newStr)

        company.stage_reorder_logic = newStr
        company.save()

        return JsonResponse({"msg": "success"})


# Delete stage from settings if there is no leads in the stage
@login_required(login_url='login')
def deleteStage(request, stage_pk):
    if request.method == 'POST':
        loggedInUser = UserProfile.objects.get(user=request.user)
        company = loggedInUser.company
        stageReorderLogic = company.stage_reorder_logic

        stage = get_object_or_404(LeadStage, id=stage_pk)
        if company != stage.company:
            return HttpResponseForbidden()

        leadsReorderLogic = stage.leads_reorder_logic

        # check, if there is any leads in this stage
        if leadsReorderLogic.strip() == '':
            stage.delete()

            logicOrderStrList = stageReorderLogic.split(',')
            # print("logicOrderStrList: ", logicOrderStrList)

            logicOrderStrList.remove(str(stage_pk))
            # print(logicOrderStrList)

            newStageReorderLogic = ",".join(logicOrderStrList)
            # print("newStrOrder: ", newStrOrder)

            company.stage_reorder_logic = newStageReorderLogic
            company.save()

            return JsonResponse({
                "success": True,
                "msg": "Successfully deleted!!",
            })
        else:
            return JsonResponse({
                "success": False,
                "msg": "Can't delete this stage. Please move all the leads" +
                " inside of this stage and try again."
            })


# Move leads from one stage to another stage
@login_required(login_url='login')
def moveStageLead(request):
    if request.method == 'POST':
        company = UserProfile.objects.get(user=request.user).company

        movedFrom = request.POST.get('stage_moved_from')
        movedTo = request.POST.get('stage_moved_to')
        # print(movedFrom, '-', movedTo)

        movedFromStage = LeadStage.objects.get(id=movedFrom)
        # Update status of all the leads which are moved
        movedToStage = LeadStage.objects.get(id=movedTo)
        # print(newStage.stage_label)

        if company != movedFromStage.company:
            return HttpResponseForbidden()

        movedFromLeadIds = movedFromStage.leads_reorder_logic
        movedToLeadIds = movedToStage.leads_reorder_logic

        # print(movedFromLeadIds, '-', movedToLeadIds)

        if movedFromLeadIds.strip() != '':
            leadIds = movedFromLeadIds.split(',')
            # print("leadIds: ", leadIds)

            for leadId in leadIds:
                newLead = get_object_or_404(Lead, id=leadId)
                newLead.stage = movedToStage
                newLead.save()
                # print("lead updated: ", newLead.stage.stage_label)
        else:
            return redirect('company_setting')

        # Move the order indexing from movedFrom to movedTo .
        if movedToLeadIds == '':
            movedToStage.leads_reorder_logic = movedFromLeadIds
        else:
            movedToStage.leads_reorder_logic = f"{movedToLeadIds},{movedFromLeadIds}"
        movedToStage.save()

        # empty the logic order of MovedFrom
        movedFromStage.leads_reorder_logic = ''
        movedFromStage.save()

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


# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
# ------------------------------------------APIS-----------------------------------------
# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
def apiCompanySetting(request):
    api_key = request.GET.get('key')
    # print(api_key)

    if not api_key or len(api_key) < 36:
        return JsonResponse({
            "success": False,
            "msg": "Api Key is missing or invalid",
        }, status=400)

    try:
        company = Company.objects.get(api_key=api_key)
    except Company.DoesNotExist:
        return JsonResponse({
            "success": False,
            "msg": "invalid Key",
        }, status=404)

    stages = LeadStage.objects.filter(company=company)

    stageReorderLogic = company.stage_reorder_logic
    # print("stageReorderLogic: ", stageReorderLogic)
    if stageReorderLogic.strip() != '':
        sortedStages = sortQueryObj(stages, stageReorderLogic.split(','))
    else:
        sortedStages = []

    return JsonResponse({
        "success": True,
        "key": api_key,
        "stage": serialize('json', sortedStages)
    })
