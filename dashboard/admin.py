from django.contrib import admin
from . models import *

# Register your models here.

admin.site.register(ass)
admin.site.register(exx)

class PageVisitAdmin(admin.ModelAdmin):
    list_display = ('user', 'path', 'visit_count', 'last_visit')
    
admin.site.register(PageVisit, PageVisitAdmin)

