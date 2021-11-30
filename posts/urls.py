from django.urls import path
from posts import views

urlpatterns = [
    path('servisformu/', views.ServiceFormView, name='serviceform'),
    path('servisformu/<id>/', views.ServiceFormEditView, name='serviceeditform'),
    path('servislistesi/', views.ServisList, name='servicelist'),
    path('servisdetay/<id>/', views.ServiceDetail, name='servicedetail'),
    path('servicemission/', views.MissionCompleted, name='mission'),
    path('servicecome/', views.ServiceCome, name='servicecome'),
    path('servicedelete/<id>/', views.ServiceDelete, name='servicedelete'),
    path('servicesearch/', views.ServiceSearch, name='servicesearch'),
    path('delivered/', views.Delivered, name='delivered'),
    path('actionadd/<id>/<action_id>/', views.ActionAdd, name='actionadd'),
    path('actionadd/<id>/<action_id>/', views.ActionAdd, name='actionadd'),
    path('actiondelete/<id>/<action_id>/',
         views.ActionDelete, name='actiondelete'),
    path('processform/<id>/', views.ProcessFormView, name="processform"),
    path('pdf/<pk>/', views.render_pdf_view.as_view(), name='pdf'),
    path('servislistem/<user>/', views.MyServiceList, name='myservicelist'),
    path('myservisdetay/<id>/', views.MyServiceDetail, name='myservicedetail'),
    path('bitenservislistesi/', views.ServisListFinish, name='servicelistfinish'),
    path('bitenservisdetay/<id>/', views.ServiceDetailFinish,
         name='servicedetailfinish'),
    path('devamservislistesi/', views.ServisListContinue,
         name='servicelistcontinue'),
    path('devamservisdetay/<id>/', views.ServiceDetailContinue,
         name='servicedetailcontinue'),

]
