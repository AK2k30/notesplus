import contextlib
from pyexpat.errors import messages
from PyPDF2 import PdfFileMerger, PdfFileReader
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render, redirect

from . forms import *
from django.contrib import messages
from django.views import generic
from youtubesearchpython import VideosSearch
import requests 
from django.conf import settings
from isodate import parse_duration
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from .forms import AssignForm
from .models import ass
from .models import exx
from .forms import ExpForm
from django.contrib.auth import authenticate, login
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

from django.shortcuts import render
from django.conf import settings
import io
from django.http import FileResponse
from django.shortcuts import render
from PyPDF2 import PdfReader
from io import BytesIO

from .forms import UploadFileForm
import os


# Create your views here.
def home(request):
    return render(request, 'dashboard/home.html')

class Home(TemplateView):
    template_name = 'house.html'

def upload(request):
    context = {}
    if request.method == 'POST':
        upload_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(upload_file.name, upload_file)
        context['url'] = fs.url(name)
    return render(request, 'dashboard/upload.html', context)

@login_required
def assig_list(request):
    assig = ass.objects.all()
    return render(request, 'dashboard/assig_list.html',{
        'assig':assig
    })

@login_required    
def view_url(request, id):
    ass_instance = ass.objects.get(id=id)
    return redirect(ass_instance.url)

@login_required
def upload_assig(request):
    if request.method == 'POST':
        form = AssignForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('assignment')
    else:
        form = AssignForm()
    return render(request, 'dashboard/upload_assig.html',{
        'form': form
    })

def delete_assign(request, pk):
    if request.method == 'POST':
        exp = ass.objects.get(pk=pk)
        exp.delete()
    return redirect('assignment')

def notes_adder(request):
    return render(request, 'dashboard/notes_adder.html')


def experiment(request):
    return render(request, 'dashboard/experiment.html')



def upload_experiment(request):
    context = {}
    if request.method == 'POST':
        upload_files = request.FILES['document']
        fss = FileSystemStorage()
        name = fss.save(upload_files.name, upload_files)
        context['url'] = fss.url(name)
    return render(request, 'dashboard/upload_exp.html', context)

@login_required
def exp_list(request):
    ex = exx.objects.all()
    return render(request, 'dashboard/exp_list.html',{
        'ex':ex
    })

def upload_exp(request):
    if request.method == 'POST':
        form1 = ExpForm(request.POST, request.FILES)
        if form1.is_valid():
            form1.save()
            return redirect('experiment')
    else:
        form1 = ExpForm()
    return render(request, 'dashboard/upload_exp.html',{
        'form': form1
    })

def delete_exp(request, pk):
    if request.method == 'POST':
        exp = exx.objects.get(pk=pk)
        exp.delete()
    return redirect('experiment')


def register(request):
    if request.user.is_authenticated:
        # Redirect the user to their profile page if they're already authenticated
        return redirect('assg_page')
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            new_user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, new_user)
            return redirect('assg_page')
    else:
        form = SignUpForm()
    context = {
        'form':form
    }
    return render(request, 'dashboard/register.html', context)
        
def profile(request):
    return render(request, 'dashboard/profile.html')

def sem(request):
    return render(request, 'dashboard/sem_select.html')

def homepage(request):
    return render(request, 'dashboard/homepage.html')

@login_required
def assg_page(request):
    return render(request, 'dashboard/assg_page.html')

@login_required
def exp1(request):
    return render(request, 'dashboard/exp1.html')


def pdf(request):
    return render(request, 'dashboard/pdf_view.html')

def pdf_save(request):
    return render(request, 'dashboard/pdf_save.html')


# def pdf_viewer(request):
#     if request.method == 'POST' and request.FILES['pdf_file']:
#         # Save the uploaded PDF file to the server
#         pdf_file = request.FILES['pdf_file']
#         fs = FileSystemStorage()
#         filename = fs.save(pdf_file.name, pdf_file)

#         # Get the URL of the uploaded file
#         uploaded_file_url = fs.url(filename)

#         # Render the PDF viewer template with the uploaded file URL
#         return render(request, 'dashboard/assig_list.html', {
#             'uploaded_file_url': uploaded_file_url
#         })

#     return render(request, 'dashboard/pdf_view.html')
@login_required
def pdf1(request):
    return render(request, 'dashboard/pdf_view1.html')

@login_required
def pdf2(request):
    return render(request, 'dashboard/pdf_view2.html')

@login_required
def pdf3(request):
    return render(request, 'dashboard/pdf_view3.html')

@login_required
def pdf4(request):
    return render(request, 'dashboard/pdf_view4.html')

@login_required
def pdf5(request):
    return render(request, 'dashboard/pdf_view5.html')

@login_required
def pdf6(request):
    return render(request, 'dashboard/pdf_view6.html')
@login_required
def pdf7(request):
    return render(request, 'dashboard/pdf_view7.html')

@login_required
def pdf8(request):
    return render(request, 'dashboard/pdf_view8.html')

@login_required
def pdf9(request):
    return render(request, 'dashboard/pdf_view9.html')

@login_required
def pdf10(request):
    return render(request, 'dashboard/pdf_view10.html')
@login_required
def pdf11(request):
    return render(request, 'dashboard/pdf_view11.html')

@login_required
def pdf12(request):
    return render(request, 'dashboard/pdf_view12.html')

@login_required
def pdf13(request):
    return render(request, 'dashboard/pdf_view13.html')
@login_required
def pdf14(request):
    return render(request, 'dashboard/pdf_view14.html')

@login_required
def pdf15(request):
    return render(request, 'dashboard/pdf_view15.html')

@login_required
def pdf16(request):
    return render(request, 'dashboard/pdf_view16.html')

@login_required
def pdf17(request):
    return render(request, 'dashboard/pdf_view17.html')
@login_required
def pdf18(request):
    return render(request, 'dashboard/pdf_view18.html')

@login_required
def pdf19(request):
    return render(request, 'dashboard/pdf_view19.html')

@login_required
def pdf20(request):
    return render(request, 'dashboard/pdf_view20.html')

@login_required
def pdfDBMS(request):
    return render(request, 'dashboard/pdf_viewDBMS.html')


@login_required
def pdfAOA(request):
    return render(request, 'dashboard/pdf_viewAOA.html')


@login_required
def pdfMaths(request):
    return render(request, 'dashboard/pdf_viewMaths.html')




