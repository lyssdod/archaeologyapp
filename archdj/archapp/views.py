from django.http import HttpResponse
from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.core.urlresolvers import reverse
from django.views import generic
from .models import Site


def welcomePage(request):
    return render(request, 'archapp/welcome.html')

def newSite(request):
    return render(request, 'archapp/newsite.html')

#def sitePage(generic.DetailView):
#    model = Site
#    template_name = 'archapp/site.html'
    #thesite = get_object_or_404(Site, pk=site_id)
    #return render(request, 'archapp/site.html', {'site': thesite})

def siteEdit(request, site_id):
    thesite = get_object_or_404(Site, pk=site_id)
    return render(request, 'archapp/edit.html', {'site': thesite})

def siteDelete(request, site_id):
    thesite = get_object_or_404(Site, pk=site_id)
    return render(request, 'archapp/delete.html', {'site': thesite})

def allSites(request):
    allsites = Site.objects.all()
    return render(request, 'archapp/all.html', {'allsites': allsites})

def publicQueries(request):
    return HttpResponse("You're viewing public queries.")


def search(request):
    return HttpResponse("Hello, You're viewing search results")

def login(request):
    return render(request, 'archapp/login.html')





