from django.urls import path
from djangodocker.views import tittle

urlpatterns =[
path('',tittle,name="index")

]

