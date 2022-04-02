from django.urls import path
from .views import *

app_name = "home_app"

urlpatterns = [
    path('homepage/', HomePage.as_view(), name="panel"),
    path('mixin/', TemplatePruebaMixin.as_view(), name="mixin"),
]