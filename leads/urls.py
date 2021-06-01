from django.urls import path
from . import views

urlpatterns = [
    path('leads/', views.leadPage, name="leads_page"),
    path('lead/add/', views.addLead, name="add_lead"),
    path('lead/indexing/status/update/',
         views.updateLeadStatus, name="update_lead_status"),

    path('lead/<int:lead_pk>/', views.leadProfile, name="lead_profile"),
    path('lead/<int:lead_pk>/update/',
         views.updateLeadProfile, name="update_lead_profile"),

    path('lead/<int:lead_pk>/note/add/',
         views.addLeadNote, name="add_lead_note"),
    path('lead/<int:lead_pk>/task/add/',
         views.addLeadTask, name="add_lead_task"),

    path('lead/note/<int:lead_note_pk>/update/',
         views.updateLeadNote, name="update_lead_note"),
    path('lead/task/<int:lead_task_pk>/update/',
         views.updateLeadTask, name="update_lead_task"),

    path('lead/note/<int:lead_note_pk>/delete/',
         views.deleteLeadNote, name="delete_lead_note"),
    path('lead/task/<int:lead_task_pk>/delete/',
         views.deleteLeadTask, name="delete_lead_task"),

]
