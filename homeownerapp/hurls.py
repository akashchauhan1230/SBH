from django.urls import path
from . import views

urlpatterns=[

    path('homeownerdash/',views.homeownerdash, name='homeownerdash'),
    path('homeLogout/', views.homeLogout,name='homeLogout'),
    path('hchangepass/',views.hchangepass , name='hchangepass'),
    path('homeownerprofile/',views.homeownerprofile , name='homeownerprofile'),
    path('homeowneredit/',views.homeowneredit , name='homeowneredit'),
    path('addproject/',views.addproject , name='addproject'),
    path('hviewproject/',views.hviewproject , name='hviewproject'),
    path('hrunproject/',views.hrunproject , name='hrunproject'),
    path('hcompleteproject/',views.hcompleteproject , name='hcompleteproject'),
    path('hviewapplications/<id>',views.hviewapplications,name='hviewapplications'),
    path('rejectapp/<id>',views.rejectapp,name='rejectapp'),
    path('approveapp/<id>',views.approveapp,name='approveapp'),
    path('viewupdates/<id>',views.viewupdates,name='viewupdates'),
]