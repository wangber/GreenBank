from django.urls import path,include
from.api import yuyue,login_up,AuthView,CreateCode
urlpatterns = [
   path('yuyue/',yuyue),
   path('login_up/',login_up),
   path('auth/',AuthView.as_view()),
   path('createcode/',CreateCode.as_view()),

]

