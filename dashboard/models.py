from django.db import models
from django.contrib.auth.models import User

    
class ass(models.Model):
    title = models.CharField(max_length=100)
    owner = models.CharField(max_length=100)
    pdf = models.FileField(upload_to='notes/pdfs/')
    url = models.URLField(null=True, blank=True, editable=True)
    cover = models.ImageField(upload_to="notes/covers/", null=True, blank = True)
    
    def __str__(self):
        return self.title
    
    def delete(self, *args,  **kwargs):
        self.pdf.delete()
        self.cover.delete()
        super().delete(*args, **kwargs)
        
class exx(models.Model):
    title = models.CharField(max_length=100)
    owner = models.CharField(max_length=100)
    pdf = models.FileField(upload_to='experi/pdfs/')
    cover = models.ImageField(upload_to="experi/covers/", null=True, blank = True)
    
    def __str__(self):
        return self.title
    
    def delete(self, *args,  **kwargs):
        self.pdf.delete() # type: ignore
        self.cover.delete()
        super().delete(*args, **kwargs)
        
from django import forms



        

    

