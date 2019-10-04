from django.urls import path,include
from apitest.views import AuthView,CreateCode
urlpatterns = [
    path('auth',AuthView.as_view()),
    path('getcode',CreateCode.as_view()),
]

