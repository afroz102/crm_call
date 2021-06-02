import json

from collections import defaultdict
# from django.core.serializers import serialize
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.http.response import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
# from django.shortcuts import get_object_or_404

from home.utils import sortQueryObj
from home.models import LeadStage, StageIndexOrder, StageElementIndexLogic
from users.models import UserProfile

from .forms import AddLeadForm
from .models import Lead, LeadNote, LeadTask, LeadProfileLog


# Lead Page
@login_required(login_url='login')
def leadPage(request):
    loggedInUser = get_object_or_404(
        UserProfile, user=request.user, is_deleted=False)
    company = loggedInUser.company

    stages = LeadStage.objects.filter(company=company)

    leads = Lead.objects.filter(company=company)

    # For displaying stages in sorted order
    orderIndexObj, created = StageIndexOrder.objects.get_or_create(
        company=company)

    orderIndexList = []
    if not created:
        orderIndexList = orderIndexObj.reorder_string.split(',')
    sortedStages = sortQueryObj(stages, orderIndexList)

    # Logics For displaying item in respective stages in sorted manner
    orderIndexLogicList = []
    for stageItem in stages:
        # print(type(stageItem.stage_label), '-', stageItem.stage_label)
        try:
            orderIndexLogicObj = StageElementIndexLogic.objects.get(
                company=company, stage=stageItem)

        except StageElementIndexLogic.DoesNotExist:
            # print("Hello")
            orderIndexLogicObj = StageElementIndexLogic.objects.create(
                company=company, stage=stageItem)

        # print("orderIndexLogicObj1: ", serializers.serialize(
        #     'json', [orderIndexLogicObj]))

        # print(stageItem.stage_label, ' - ',
        #       orderIndexLogicObj.element_index_logic)

        # For listing all sorted index in a seperate stage fields
        orderIndexList = []
        if (orderIndexLogicObj.element_index_logic) is not None or (
                orderIndexLogicObj.element_index_logic != ''):
            orderIndexList = orderIndexLogicObj.element_index_logic.split(',')

        newLogicObj = {}
        newLogicObj[stageItem.stage_label] = orderIndexList
        orderIndexLogicList.append(newLogicObj)

    # print("orderIndexLogicList: ", orderIndexLogicList)

    # a default dict, for displaying item in respective stages in sorted manner
    columnOrder = defaultdict(list)
    for orderIndexLogic in orderIndexLogicList:
        # print("orderIndexLogic: ", orderIndexLogic)

        for stage_label, leadIds in orderIndexLogic.items():
            # print(stage_label, ' - ', leadIds)

            # if len(leadIds) > 0:(length already > 0)
            for leadId in leadIds:
                # print("leadId: ", leadId)

                if leadId != '':
                    newLeadObj = leads.filter(id=int(leadId)).first()
                    newStageLabel = newLeadObj.stage.stage_label
                    # print(type(newStageLabel), '-', newStageLabel)

                    columnOrder[newStageLabel].append(newLeadObj)

    # print("columnOrder: ", columnOrder)

    # # to iterate in default dict user dictName.items()
    # for x, y in columnOrder.items():
    #     print(type(x), '-', x)
    #     print(type(y), '-', y)

    context = {
        "loggedInUser": loggedInUser,
        "sortedStages": sortedStages,
        "columnOrder": columnOrder.items(),
    }

    return render(request, 'leads/leads_page.html', context)


@ login_required(login_url='login')
def addLead(request):
    loggedInUser = get_object_or_404(
        UserProfile, user=request.user, is_deleted=False)
    company = loggedInUser.company

    if request.method == 'POST':
        form = AddLeadForm(company, request.POST)
        if form.is_valid():
            newLeadObj = form.save(commit=False)
            newLeadObj.company = company
            newLeadObj.added_by = request.user
            newLeadObj.save()

            # Craete a render logic method for the given stage
            orderIndexLogicObj, created = StageElementIndexLogic.objects.get_or_create(
                company=company, stage=form.cleaned_data.get('stage'))

            # if element_index_logic is empty or created for the first time
            if created or orderIndexLogicObj.element_index_logic == '' or (
                    orderIndexLogicObj.element_index_logic is None):
                orderIndexLogicObj.element_index_logic = str(newLeadObj.id)
            else:
                orderIndexLogicObj.element_index_logic = orderIndexLogicObj.element_index_logic + \
                    ',' + str(newLeadObj.id)
            orderIndexLogicObj.save()

            # messages.success(request, 'Changes successfully saved.')

            return redirect('leads_page')

        else:
            form = AddLeadForm(company=company, initial={
                'stage': request.POST.get('stage'),
                'title': request.POST.get('title'),
                'contact_person': request.POST.get('contact_person'),
                'email': request.POST.get('email'),
                'phone': request.POST.get('phone'),
                'designation': request.POST.get('designation'),
                'source': request.POST.get('source'),
            })

            context = {
                "loggedInUser": loggedInUser,
                "form": form,
                "status": 400,  # for toaster
            }

            messages.add_message(
                request, messages.ERROR, 'Something went wrong.' +
                'Please check all the fields and Try Again.'
            )
            return render(request, 'leads/add_lead.html', context)
    else:
        form = AddLeadForm(company=company)
        context = {
            "loggedInUser": loggedInUser,
            "form": form,
        }
        return render(request, 'leads/add_lead.html', context)


@login_required(login_url='login')
def updateLeadStatus(request):
    if request.method == 'POST':
        loggedInUser = get_object_or_404(
            UserProfile, user=request.user, is_deleted=False)
        data = json.loads(request.body)

        # print("data: ", data)

        lead_pk = data['terget_lead_pk']
        moved_from_stage_pk = data['moved_from_stage'].split('_')[-1]
        moved_to_stage_pk = data['moved_to_stage'].split('_')[-1]
        updatedIndexList = data['updatedIndexList']

        # Updating stage of targeted lead
        moved_to_stage_obj = LeadStage.objects.get(id=moved_to_stage_pk)

        lead = get_object_or_404(Lead, id=lead_pk, is_deleted=False)
        if loggedInUser.company != lead.company:
            return HttpResponseForbidden()

        lead.stage = moved_to_stage_obj
        lead.save()

        # print("Lead stage updated: ", lead.stage)

        # Updating order index of stage, from where the lead is moved
        movedFromStage = StageElementIndexLogic.objects.get(
            stage=moved_from_stage_pk)
        movedFromStage.element_index_logic = updatedIndexList['movedFromStageOrder']
        movedFromStage.save()
        # print("movedFromStage updated: ", movedFromStage.element_index_logic)

        # Updating order index of stage, to where the lead is moved
        movedToStage = StageElementIndexLogic.objects.get(
            stage=moved_to_stage_pk)
        movedToStage.element_index_logic = updatedIndexList['movedToStageOrder']
        movedToStage.save()
        # print("movedToStage updated: ", movedToStage.element_index_logic)

    return JsonResponse({"msg": "stage updated"})


@login_required(login_url='login')
def leadProfile(request, lead_pk):
    loggedInUser = get_object_or_404(
        UserProfile, user=request.user, is_deleted=False,)
    company = loggedInUser.company

    lead = get_object_or_404(Lead, id=lead_pk, is_deleted=False)

    # For displaying stages in sorted order
    stages = LeadStage.objects.filter(company=company)
    orderIndexObj = StageIndexOrder.objects.get(company=company)
    # some operation to sort stages
    orderIndexList = orderIndexObj.reorder_string.split(',')
    sortedStages = sortQueryObj(stages, orderIndexList)

    # If lead doesn't belong to the company. display error forbidden message
    if lead.company != company:
        return HttpResponseForbidden()

    leadLogs = LeadProfileLog.objects.filter(
        lead=lead_pk).order_by('-created_at')
    leadNotes = LeadNote.objects.filter(
        lead=lead_pk, is_deleted=False).order_by('-created_at')
    leadTasks = LeadTask.objects.filter(
        lead=lead_pk, is_deleted=False).order_by('-created_at')

    context = {
        "loggedInUser": loggedInUser,
        "lead": lead,
        "leadLogs": leadLogs,
        "leadNotes": leadNotes,
        "leadTasks": leadTasks,
        "sortedStages": sortedStages,
    }
    return render(request, 'leads/lead_profile.html', context)


@login_required(login_url='login')
def updateLeadProfile(request, lead_pk):
    if request.method == 'POST':
        loggedInUser = get_object_or_404(
            UserProfile, user=request.user, is_deleted=False)

        lead = get_object_or_404(Lead, id=lead_pk, is_deleted=False)

        # If the user does not belong to the same company he is accessing
        if lead.company != loggedInUser.company:
            return HttpResponseForbidden()

        title = request.POST.get('lead_title')
        lead_stage = request.POST.get('stage')
        contact_person = request.POST.get('contact_name')
        contact_email = request.POST.get('contact_email')
        phone = request.POST.get('contact_phone')
        designation = request.POST.get('designation')
        source = request.POST.get('source')

        if title:
            lead.title = title
            # Text for Lead Profile Log
            text = f"<i>{loggedInUser.full_name}</i>, updated the title of lead to <b>{title}</b>"

        elif lead_stage:
            lead.lead_stage = lead_stage
            text = f"<i>{loggedInUser.full_name}</i>, updated the Stage status of the lead contact to <b>{lead_stage}</b>"

        elif contact_person:
            lead.contact_person = contact_person
            text = f"<i>{loggedInUser.full_name}</i>, updated the Name of the lead contact to <b>{contact_person}</b>"

        elif contact_email:
            lead.email = contact_email
            text = f"<i>{loggedInUser.full_name}</i>, updated the Email of contact to <b>{contact_email}</b>"

        elif phone:
            lead.phone = phone
            text = f"<i>{loggedInUser.full_name}</i>, updated the Phone of contact to <b>{phone}</b>"

        elif designation:
            lead.designation = designation
            text = f"<i>{loggedInUser.full_name}</i>, updated the Designation of contact to <b>{designation}</b>"

        elif source:
            lead.source = source
            text = f"<i>{loggedInUser.full_name}</i>, updated the Source of contact to <b>{source}</b>"

        lead.save()
        LeadProfileLog.objects.create(lead=lead, log=text)

    return redirect('lead_profile', lead_pk=lead_pk)


# Lead note post request
@ login_required(login_url='login')
def addLeadNote(request, lead_pk):
    loggedInUser = get_object_or_404(
        UserProfile, user=request.user, is_deleted=False)
    if request.method == 'POST':
        user = request.user
        note_title = request.POST.get('note_title')
        lead_note = request.POST.get('lead_note')

        lead = get_object_or_404(Lead, id=lead_pk, is_deleted=False)
        if lead.company != loggedInUser.company:
            return HttpResponseForbidden()

        LeadNote.objects.create(
            lead=lead,
            title=note_title,
            note=lead_note,
            updated_by=user,
        )
        # Create a log of it
        text = f"<i>{loggedInUser.full_name}</i>, Added a Note with title <b>{note_title}</b>"
        LeadProfileLog.objects.create(lead=lead, log=text)

        return redirect('lead_profile', lead_pk=lead_pk)


@ login_required(login_url='login')
def updateLeadNote(request, lead_note_pk):
    loggedInUser = get_object_or_404(
        UserProfile, user=request.user, is_deleted=False)

    leadNote = get_object_or_404(LeadNote, id=lead_note_pk, is_deleted=False)

    if leadNote.lead.company != loggedInUser.company:
        return HttpResponseForbidden()

    if request.method == 'POST':
        leadNote.title = request.POST['note_title']
        leadNote.note = request.POST['lead_note']
        leadNote.save()
        # Create a log of it
        text = f"<i>{loggedInUser.full_name}</i>, Updated the Note <b>{leadNote.title}</b>"
        LeadProfileLog.objects.create(lead=leadNote.lead, log=text)

        return redirect('lead_profile', lead_pk=leadNote.lead.id)


@ login_required(login_url='login')
def deleteLeadNote(request, lead_note_pk):
    loggedInUser = get_object_or_404(
        UserProfile, user=request.user, is_deleted=False)

    leadNote = get_object_or_404(LeadNote, id=lead_note_pk, is_deleted=False)
    if leadNote.lead.company != loggedInUser.company:
        return HttpResponseForbidden()

    if request.method == 'POST':
        # print("lead_note_pk: ", lead_note_pk)
        leadNote.is_deleted = True
        leadNote.save()
        # Create a log of it
        text = f"<i>{loggedInUser.full_name}</i>, Deleted the Note <b>{leadNote.title}</b>"
        LeadProfileLog.objects.create(lead=leadNote.lead, log=text)

        return redirect('lead_profile', lead_pk=leadNote.lead.id)


# Lead Task post request
@ login_required(login_url='login')
def addLeadTask(request, lead_pk):
    loggedInUser = get_object_or_404(
        UserProfile, user=request.user, is_deleted=False)
    if request.method == 'POST':
        user = request.user
        task_title = request.POST.get('task_title')
        lead_task = request.POST.get('lead_task')

        lead = get_object_or_404(Lead, id=lead_pk, is_deleted=False)
        if lead.company != loggedInUser.company:
            return HttpResponseForbidden()

        LeadTask.objects.create(
            lead=lead,
            title=task_title,
            task=lead_task,
            updated_by=user,
        )
        # Create a log of it
        text = f"<i>{loggedInUser.full_name}</i>, Added a Task with title <b>{task_title}</b>"
        LeadProfileLog.objects.create(lead=lead, log=text)

        return redirect('lead_profile', lead_pk=lead_pk)


@ login_required(login_url='login')
def updateLeadTask(request, lead_task_pk):
    loggedInUser = get_object_or_404(
        UserProfile, user=request.user, is_deleted=False)

    leadTask = get_object_or_404(LeadTask, id=lead_task_pk, is_deleted=False)

    if leadTask.lead.company != loggedInUser.company:
        return HttpResponseForbidden()

    if request.method == 'POST':
        leadTask.title = request.POST.get('task_title')
        leadTask.task = request.POST.get('lead_task')
        leadTask.save()
        # Create a log of it
        text = f"<i>{loggedInUser.full_name}</i>, Updated the task <b>{leadTask.title}</b>"
        LeadProfileLog.objects.create(lead=leadTask.lead, log=text)

        return redirect('lead_profile', lead_pk=leadTask.lead.id)


@ login_required(login_url='login')
def deleteLeadTask(request, lead_task_pk):
    loggedInUser = get_object_or_404(
        UserProfile, user=request.user, is_deleted=False)

    leadTask = get_object_or_404(LeadTask, id=lead_task_pk, is_deleted=False)
    if leadTask.lead.company != loggedInUser.company:
        return HttpResponseForbidden()

    if request.method == 'POST':
        leadTask.is_deleted = True
        leadTask.save()
        # Create a log of it
        text = f"<i>{loggedInUser.full_name}</i>, Deleted the Task <b>{leadTask.title}</b>"
        LeadProfileLog.objects.create(lead=leadTask.lead, log=text)

        return redirect('lead_profile', lead_pk=leadTask.lead.id)
