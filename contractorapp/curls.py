from django.urls import path
from . import views

urlpatterns=[

    path('contractordash/',views.contractordash, name='contractordash'),
    path('conLogout/',views.conLogout, name='conLogout'),
    path('conchangepass/',views.conchangepass, name='conchangepass'),
    path('conprofile/',views.conprofile, name='conprofile'),
    path('coneditprofile/',views.coneditprofile, name='coneditprofile'),
    path('cviewprojects/',views.cviewprojects, name='cviewprojects'),
    path('applyproject/<id>',views.applyproject, name='applyproject'),

    path('capplications/',views.capplications,name='capplications'),
    path('assignedprojects/',views.assignedprojects,name='assignedprojects'),
    path('addprogress/<id>',views.addprogress,name='addprogress'),
]