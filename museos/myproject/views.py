from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from .models import Museo
from xml.sax import make_parser
from .xmlparser import myContentHandler

def update(request):
    Museo.objects.all().delete()
    theParser = make_parser()
    theHandler = myContentHandler()
    theParser.setContentHandler(theHandler)
    theParser.parse("https://datos.madrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=201132-0-museos&mgmtid=118f2fdbecc63410VgnVCM1000000b205a0aRCRD&preview=full")
    return HttpResponse ("La tabla ha sido actualizada con el contenido de datos.madrid.es")
