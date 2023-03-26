from django.shortcuts import render
from django.http import HttpResponse
from api.models import Sondage
# Create your views here.

def index(request):
	return render(request, 'index.html', {})

def sondage(request, slug):
	slug = Sondage.objects.filter(url_slug=slug)
	if len(slug) == 0:
		return render(request, '404.html')
	return render(request, 'index.html', {"sondage": slug.first()})

def sondage_data(request):
	return render(request, 'sondage.html')