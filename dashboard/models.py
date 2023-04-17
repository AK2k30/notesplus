from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.db import models


    
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
    

from django.db import models
from django.contrib.auth.models import User
class PageVisit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    path = models.CharField(max_length=255)
    visit_count = models.PositiveIntegerField(default=0)
    last_visit = models.DateTimeField(null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    current_time = models.DateTimeField(null=True, blank=True)
    time_spent = models.PositiveIntegerField(default=0)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    time_spent_minutes = models.PositiveIntegerField(default=0)
    

    class Meta:
        unique_together = ('user', 'path')







        

    

