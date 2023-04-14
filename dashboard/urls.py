from django.conf import Settings, settings
from django.conf.urls.static import static
from django.urls import path
from.import views
from django.contrib.auth import views as auth_views
from .views import assig_list, view_url

urlpatterns = [
    path('',views.homepage, name='homepage'),
    path('index',views.index,name="index"),
    path('upload',views.upload, name="upload"),
    path('assignment/',views.assig_list, name="assignment"),
    path('view_url/<int:id>/', view_url, name='view_url'),
    path('assignment/upload/', views.upload_assig, name="upload_assig"),
    path('assignment/<int:pk>/', views.delete_assign, name="delete_assign"),
    path('notes_adder',views.notes_adder, name="notesadder"),
    path('experiment',views.experiment, name="experiments"),
    path('exp/',views.exp_list,name="experiment"),
    path('exp/upload/', views.upload_exp, name="upload_exp"),
    path('exp/<int:pk>/', views.delete_exp, name="delete_exp"),
    path('upload exx',views.upload_experiment, name="upload exx"),
    path('register', views.register, name="register"),
    path('assg_page',views.assg_page,name="assg_page"),
    path('exp1',views.exp1,name="exp1"),
    path('pdf_view',views.pdf, name="pdf_view"),
    path('pdf_view1',views.pdf1, name="pdf_view1"),
    path('pdf_view2',views.pdf2, name="pdf_view2"),
    path('pdf_view3',views.pdf3, name="pdf_view3"),
    path('pdf_view4',views.pdf4, name="pdf_view4"),
    path('pdf_view5',views.pdf5, name="pdf_view5"),
    path('pdf_view6',views.pdf6, name="pdf_view6"),
    path('pdf_view7',views.pdf7, name="pdf_view7"),
    path('pdf_view8',views.pdf8, name="pdf_view8"),
    path('pdf_view9',views.pdf9, name="pdf_view9"),
    path('pdf_view10',views.pdf10, name="pdf_view10"),
    path('pdf_view11',views.pdf11, name="pdf_view11"),
    path('pdf_view12',views.pdf12, name="pdf_view12"),
    path('view_pdf',views.view_pdf, name="view_pdf"),
]   

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


