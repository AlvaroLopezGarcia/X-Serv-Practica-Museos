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

FORMULARIO_COMENTARIO = """
    <form action= "/" Method= "POST">
    Comentario:<br>
    <input type="text" name="name" placeholder= "comenta"><br>
    <input type="submit" value="Enviar">
</form>
"""
FORMULARIO_USUARIO = """
    <form action= "" Method= "POST">
  <p>
    Opciones:
    <select name="opcion">
      <option>Titulo</option>
      <option>Tamaño</option>
      <option>Fondo Color</option>
    </select>
  </p>
  <input type="text" name="valor"><br>
  <p><input type="submit" value="Enviar datos"></p>
</form>
"""

museos = {}
#lista = {}


def update(request):
    Museo.objects.all().delete()
    theParser = make_parser()
    theHandler = myContentHandler()
    theParser.setContentHandler(theHandler)
    theParser.parse("https://datos.madrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=201132-0-museos&mgmtid=118f2fdbecc63410VgnVCM1000000b205a0aRCRD&preview=full")
    return HttpResponse('Se han actualizado los museos')


#@csrf_exempt
#def museo(request,numero):
#    if

@csrf_exempt
def museos(request):
    lista = {}
    existe = False
    museos = Museo.objects.all()
    FORMULARIO_DISTRITO = '<form action= "" Method= "POST"><p>Opciones:<select name="opcion">'
    for museo in museos:
        lista[museo.distrito]= 0

    claves=lista.keys()
    for distrito in claves:
        FORMULARIO_DISTRITO +="<option>"+ distrito + "</option>"

    FORMULARIO_DISTRITO+='</select></p><p><input type="submit" value="Enviar datos"></p></form>'
    respuesta = "<ul>"
    if request.method == "POST":
        opcion= request.POST['opcion']
        for museo in museos:
            if museo.distrito==opcion:
                respuesta += '<li><a href= "' + museo.enlace +'">' + museo.nombre + "</a></ul><ul>"
    else:
        for museo in museos:
            respuesta += '<li><a href= "' + museo.enlace +'">' + museo.nombre + "</a></ul><ul>"

    respuesta = FORMULARIO_DISTRITO + respuesta
    return HttpResponse (respuesta)

@csrf_exempt
def usuario(request, numero):
    seleccionados =Seleccion.objects.filter(usuario_id=numero)
    try:
        usuario = Usuario.objects.get(id=str(numero))
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

    if request.user.is_authenticated():
        logged = 'Logged in as ' + request.user.username + '. <a href="/logout">Logout</a></br>'
        if request.user.username == str(usuario.nombre):
            respuesta += '</ul>'+ FORMULARIO_USUARIO + logged
        else:
            respuesta += '</ul>'+ logged
    else:
        logged = 'Not logged in. <a href="/login">Login</a>'
        respuesta += '</ul>'+ logged
    if request.method == "POST":
        print(request.body)
        opcion= request.POST['opcion']
        valor = request.POST['valor']
        if opcion == 'Titulo':
            usuario.titulo = valor
        elif opcion == 'Tamaño':
            usuario.tamaño = valor
        elif opcion == 'Fondo Color':
            usuario.fondocolor = valor

        usuario.save()
    return HttpResponse (respuesta)

@csrf_exempt
def barra(request):
    lista_comentados = []
    lista = {}

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
    respuesta="<ul>"
    if request.method == "POST":
        for element in lista_comentados:
            if element[1] != 0:
                if museos.get(nombre= element[0]).accesibilidad =='1':
                    respuesta += '<li><a href= "' + museos.get(nombre= element[0]).enlace 
                    respuesta += '">' + museos.get(nombre= element[0]).nombre + "</a><ul>"
                    respuesta += '<li type= "circle">Barrio: ' + museos.get(nombre= element[0]).barrio
                    respuesta += '; Distrito: '+ museos.get(nombre= element[0]).distrito
                    respuesta += '<li type= "circle"><a href= "/museos/'
                    respuesta += str(museos.get(nombre= element[0]).id) +'">' + "Más información</a></ul>"
            if(cont==4):
                break
            cont+=1
    else:
        for element in lista_comentados:
            if element[1] != 0:
                respuesta += '<li><a href= "' + museos.get(nombre= element[0]).enlace
                respuesta += '">' + museos.get(nombre= element[0]).nombre + "</a><ul>"
                respuesta += '<li type= "circle">Barrio: ' + museos.get(nombre= element[0]).barrio
                respuesta += '; Distrito: '+ museos.get(nombre= element[0]).distrito
                respuesta += '<li type= "circle"><a href= "/museos/' + str(museos.get(nombre= element[0]).id)
                respuesta += '">' + "Más información</a></ul>"
                if(cont==4):
                    break
                cont+=1
            else:
                break;
#    print (lista_comentados)
    respuesta += '</br></br></br></br></br>'
    for usuario in usuarios:
        respuesta += '<li><a href= "/usuario/' + str(usuario.id) +'">' + str(usuario.nombre)+"</a><ul>"
#Te falta configurar lo del titulo
        respuesta += '<li type= "circle">Titulo: ' + str(usuario.titulo) +"</ul>"

    if request.method == "POST":
        respuesta += '</ul>'+FORMULARIO
    else:
        respuesta += '</ul>'+FORMULARIO_ACCESIBILIDAD

    if request.user.is_authenticated():
        logged = 'Logged in as ' + request.user.username + '. <a href="/logout">Logout</a></br>'
        respuesta += logged
    else:
        logged = 'Not logged in. <a href="/login">Login</a>'
        respuesta += logged

    return HttpResponse (respuesta)
    
