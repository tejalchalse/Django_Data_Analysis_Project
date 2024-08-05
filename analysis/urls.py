from django.urls import path
from .views import upload_file
from . import views

urlpatterns = [
    path('', upload_file, name='upload_file'),
]
