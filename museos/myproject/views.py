from django.shortcuts import render
from django.http import HttpResponse
from operator import itemgetter
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from .models import Museo
from .models import Comentario
from .models import Usuario
from .models import Seleccion
from xml.sax import make_parser
from .xmlparser import myContentHandler
import operator

FORMULARIO = """
    <form action= "/" Method= "GET">
    Filtrar:<br>
    <input type="submit" value="Más comentados">
</form>
"""
FORMULARIO_ACCESIBILIDAD = """
    <form action= "/" Method= "POST">
    Filtrar:<br>
    <input type="submit" value="Accesibles">
</form>
"""

museos = {}

lista = {}

def update(request):
    Museo.objects.all().delete()
    theParser = make_parser()
    theHandler = myContentHandler()
    theParser.setContentHandler(theHandler)
    theParser.parse("https://datos.madrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=201132-0-museos&mgmtid=118f2fdbecc63410VgnVCM1000000b205a0aRCRD&preview=full")
    return HttpResponse('Se han actualizado los museos')

def usuario(request, numero):
    seleccionados =Seleccion.objects.all()
    try:
        usuario = Usuario.objects.get(id=str(numero))
        print(usuario)
    except Usuario.DoesNotExist:
        return HttpResponseNotFound('<h1>' + numero + ' not found</h1>')
    respuesta = "<ul>"
    cont=0
    for element in seleccionados:
        respuesta += '<li><a href= "' + element.museo.enlace +'">' + element.museo.nombre + "</a><ul>"
        respuesta += '<li type= "circle">Barrio: ' + element.museo.barrio + '; Distrito: '+ element.museo.distrito
        respuesta += '<li type= "circle"><a href= "/museos/' + str(numero) +'">' + "Más información</a></ul>"
        if(cont==4):
            respuesta+= '</br></br></br></br></br>'

    respuesta += '</ul>'+FORMULARIO
    return HttpResponse (respuesta)

@csrf_exempt
def barra(request):
    lista_comentados = []

    comentarios = Comentario.objects.all()
    usuarios = Usuario.objects.all()
    museos = Museo.objects.all()
    for museo in museos:
        lista[museo.nombre]= 0
    
    claves=lista.keys()
    for comentario in comentarios:
        for clave in claves:
            if clave==comentario.museo.nombre:
                lista[comentario.museo.nombre]+= 1
                break
    lista_comentados=sorted(lista.items(), key=operator.itemgetter(1))
    lista_comentados.reverse()
    cont=0
    response_post="<ul>"
    if request.method == "POST":
        for element in lista_comentados:
            if element[1] != 0:
                if museos.get(nombre= element[0]).accesibilidad =='1':
                    response_post += '<li><a href= "' + museos.get(nombre= element[0]).enlace +'">' + museos.get(nombre= element[0]).nombre + "</a><ul>"
                    response_post += '<li type= "circle">Barrio: ' + museos.get(nombre= element[0]).barrio + '; Distrito: '+ museos.get(nombre= element[0]).distrito
                    response_post += '<li type= "circle"><a href= "/museos/' + str(museos.get(nombre= element[0]).id) +'">' + "Más información</a></ul>"
            if(cont==4):
                break
            cont+=1

        response_post += '</br></br></br></br></br>'
        for usuario in usuarios:
            response_post += '<li>Nombre: ' + str(usuario.nombre) +"<ul>"
            response_post += '<li type= "circle"><a href= "/' + str(usuario.nombre) +'">' + str(usuario.titulo)+"</a></ul>"

        response_post += '</ul>'+FORMULARIO
        return HttpResponse (response_post)

    response_get = "<ul>"
    print(lista_comentados)
    for element in lista_comentados:
        if element[1] != 0:
            response_get += '<li><a href= "' + museos.get(nombre= element[0]).enlace +'">' + museos.get(nombre= element[0]).nombre + "</a><ul>"
            response_get += '<li type= "circle">Barrio: ' + museos.get(nombre= element[0]).barrio + '; Distrito: '+ museos.get(nombre= element[0]).distrito
            response_get += '<li type= "circle"><a href= "/museos/' + str(museos.get(nombre= element[0]).id) +'">' + "Más información</a></ul>"
            if(cont==4):
                break
            cont+=1
        else:
            break;

    response_get += '</br></br></br></br></br>'
    for usuario in usuarios:
        response_get += '<li>Nombre: ' + str(usuario.nombre) +"<ul>"
        response_get += '<li type= "circle"><a href= "/' + str(usuario.nombre) +'">' + str(usuario.titulo)+"</a></ul>"

    response_get += '</ul>'+FORMULARIO_ACCESIBILIDAD
    return HttpResponse (response_get)
    
