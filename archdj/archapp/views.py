from django.http import HttpResponse
from .models import Site


def welcomePage(request):
    return HttpResponse("Hello, world. You're at the arch index.")

def newSite(request):
    return HttpResponse("New site.")

def sitePage(request, site_id):
    thesite = Site.objects.get(pk=site_id)
    return HttpResponse(thesite)

def siteEdit(request, site_id):
    response = "Hello, you are editing the site %s."
    return HttpResponse(response % site_id)

def siteDelete(request, site_id):
    response = "Hello, you are deleting the site %s."
    return HttpResponse(response % site_id)

def allSites(request):
    allsites = Site.objects.all()
    return HttpResponse(allsites)

def publicQueries(request):
    return HttpResponse("You're viewing public queries.")


def search(request):
    return HttpResponse("Hello, You're viewing search results")



