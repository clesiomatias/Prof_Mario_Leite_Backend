from django.db import models


class Arquivos(models.Model):     
    TIPO_ARQUIVO = [
        ('A', 'Arquivo'),
        ('T', 'Texto'),
     ] 
       
    name = models.CharField(max_length=50, unique=True)
    tipo = models.CharField(max_length=1, choices=TIPO_ARQUIVO, default = "A")
    register_date = models.DateField(auto_now_add=True)
    data = models.FileField(upload_to="uploads/")
    
    def __str__(self):
            return self.name


