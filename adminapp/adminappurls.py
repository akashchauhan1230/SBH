from django.urls import path

from . import views

urlpatterns = [

    path('admindash/', views.admindash ,name='admindash'),
    path('adminlogout/', views.adminlogout ,name='adminlogout'), #path for admin logout without page creation..
    path('viewenq/',views.viewenq,name='viewenq'),
    path('delenq/<id>',views.delenq ,name='delenq'),  #path for delenq views without page creation..
    path('adminchangepass/',views.adminchangepass ,name='adminchangepass'),
    path('managecontractors/',views.managecontractors, name='managecontractors'),
    path('managehomeowners/',views.managehomeowners, name='managehomeowners'),
    path('block/<id>',views.block, name='block'),
    path('unblock/<id>',views.unblock, name='unblock'),
]