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



def index(request):
    videos = []
    
    if request.method == 'POST':
        search_url = "https://www.googleapis.com/youtube/v3/search"
        video_url = "https://www.googleapis.com/youtube/v3/videos"
        
        search_params = {
            'part': 'snippet',
            'q' : request.POST['search'],
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'maxResults' : 100,
            'type': 'video'
        }
        
        r = requests.get(search_url, params=search_params)
        results = r.json()['items']
        
        
        video_ids = []
        for result in results:
            video_ids.append(result['id']['videoId'])
        
        if request.POST['search'] == 'lucky':
            return redirect(f'https://www.youtube.com/watch?v={ video_ids[0] }')
            
            
        video_params = {
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'part':'snippet,contentDetails',
            'id' : ','.join(video_ids),
            'maxResults' : 100,
        }
        
        r = requests.get(video_url, params=video_params) 
        results = r.json()['items']
        
        for result in results:
            
            video_data = {
                'title' : result['snippet']['title'],
                'id' : result['id'],
                'url' : f'https://www.youtube.com/watch?v={ result["id"] }',
                'duration' : int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
                'thumbnail' : result['snippet']['thumbnails']['high']['url']      
            }
        
            videos.append(video_data)
        
    context = {'videos':videos}
        
    return render(request, 'dashboard/index.html',context)

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


def assig_list(request):
    assig = ass.objects.all()
    return render(request, 'dashboard/assig_list.html',{
        'assig':assig
    })
    
def view_url(request, id):
    ass_instance = ass.objects.get(id=id)
    return redirect(ass_instance.url)

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


def assg_page(request):
    return render(request, 'dashboard/assg_page.html')


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

def pdf1(request):
    return render(request, 'dashboard/pdf_view1.html')

def pdf2(request):
    return render(request, 'dashboard/pdf_view2.html')

def pdf3(request):
    return render(request, 'dashboard/pdf_view3.html')

def pdf4(request):
    return render(request, 'dashboard/pdf_view4.html')

def pdf5(request):
    return render(request, 'dashboard/pdf_view5.html')

def pdf6(request):
    return render(request, 'dashboard/pdf_view6.html')

def pdf7(request):
    return render(request, 'dashboard/pdf_view7.html')

def pdf8(request):
    return render(request, 'dashboard/pdf_view8.html')

def pdf9(request):
    return render(request, 'dashboard/pdf_view9.html')

def pdf10(request):
    return render(request, 'dashboard/pdf_view10.html')

def pdf11(request):
    return render(request, 'dashboard/pdf_view11.html')

def pdf12(request):
    return render(request, 'dashboard/pdf_view12.html')

def pdf13(request):
    return render(request, 'dashboard/pdf_view13.html')

def pdf14(request):
    return render(request, 'dashboard/pdf_view14.html')

def pdf15(request):
    return render(request, 'dashboard/pdf_view15.html')

def pdf16(request):
    return render(request, 'dashboard/pdf_view16.html')

def pdf17(request):
    return render(request, 'dashboard/pdf_view17.html')

def pdf18(request):
    return render(request, 'dashboard/pdf_view18.html')

def pdf19(request):
    return render(request, 'dashboard/pdf_view19.html')

def pdf20(request):
    return render(request, 'dashboard/pdf_view20.html')

def pdfDBMS(request):
    return render(request, 'dashboard/pdf_viewDBMS.html')








