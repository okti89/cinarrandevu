from django.urls import path, include
from users import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('signup/', views.Signup, name='signup'),
    path('login/', views.Login, name='login'),
    path('logout/', views.Logout, name='account/logout.html'),
    path('userprofile/<username>/', views.UserProfile, name='userprofile'),
    path('editprofile/<username>/', views.EditProfile, name='editprofile'),
    path('telefon_numaraları/', views.PhoneNumberList, name='phonenumbers'),
    path('whatsap/', views.whatsapp, name='whatsapp'),

]
