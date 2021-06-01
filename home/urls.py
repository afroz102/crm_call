from django.urls import path
from . import views

urlpatterns = [
    path('', views.homePage, name="home"),
    path('setting/', views.companySetting, name="company_setting"),
    path('stage/add/', views.addStage, name="add_new_satge_for_leads"),
    path('stage/delete/<int:stage_pk>/', views.deleteStage,
         name="delete_stage"),
    path('stage-order/update/', views.updateStageOrder,
         name="update_stage_order"),
    path('move-stage-lead/', views.moveStageLead, name="move_stage_lead"),
]
