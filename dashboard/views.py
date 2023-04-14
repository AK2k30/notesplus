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
import os


# Create your views here.
def home(request):
    return render(request, 'dashboard/home.html')

def notes(request):
    if request.method == "POST":
        form = NotesForm(request.POST)
        notes = Notes(user=request.user,title=request.POST['title'],description=request.POST['description'])
        notes.save()
        messages.success(request,f"Notes Added from {request.user.username} Successfully!")
    else:
        form = NotesForm()  
    notes = Notes.objects.filter(user=request.user)
    context = {'notes':notes, 'form':form}
    return render(request, 'dashboard/notes.html',context)

def delete_note(request,pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect("notes")

class NotesDetailView(generic.DetailView):
    model = Notes


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

def books(request):
    form = DashboardForm()
    context = {'form':form}
    return render(request, 'dashboard/books.html',context)

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


def dictionary(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/"+text
        r = requests.get(url)
        answer = r.json()
        try:
            phonetics = answer[0]['phonetics'][0]['text']
            audio = answer[0]['phonetics'][0]['audio']
            definition = answer[0]['meanings'][0]['definitions'][0]['definition']
            example = answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms = answer[0]['meanings'][0]['definitions'][0]['synoyms']
            context ={
                'form':form,
                'input':text,
                'phonetics':phonetics,
                'audio':audio,
                'definition':definition,
                'example':example,
                'synonyms':synonyms
            }
        except:
            context = {
                'form':form,
                'input':''
            }
        return render(request, "dashboard/dictionary.html", context)
    else:
        form = DashboardForm()
        context = { 'form': form }
    return render(request, "dashboard/dictionary.html", context)


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

def pdf_viewer(request, pdf_id):
    try:
        pdf_file = PdfFileReader.objects.get(id=pdf_id) # type: ignore
    except PdfFileMerger.DoesNotExist: # type: ignore
        return HttpResponseNotFound('PDF file not found')
    
    path = os.path.join(settings.MEDIA_ROOT, pdf_file.file.name)
    with open(path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(path)
        return response





