from django.urls import path

from .views import Home_View, upload_arquivo, upload_sucesso

urlpatterns = [
    path('', Home_View, name='home'),
    path('upload/', upload_arquivo, name='upload_arquivo'),
    path('upload_sucesso/', upload_sucesso, name='upload_sucesso'),
    
]



