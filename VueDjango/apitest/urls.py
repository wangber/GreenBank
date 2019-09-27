from django.urls import path,include
from apitest.views import get_user
urlpatterns = [
    path('all_user',get_user),
]

