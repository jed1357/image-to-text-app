from django.urls import path
from . import views

app_name = 'imgtxt'


urlpatterns = [
	path('', views.image_upload_view, name='home'),
	path('convert', views.convertImage, name='convert'),

]