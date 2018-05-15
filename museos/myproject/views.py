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
    <form action= "" Method= "POST">
    Comentario:<br>
    <input type="text" name="comentario" placeholder= "comenta"><br>
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

#museos = {}

def update(request):
    Museo.objects.all().delete()
    theParser = make_parser()
    theHandler = myContentHandler()
    theParser.setContentHandler(theHandler)
    theParser.parse("https://datos.madrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=201132-0-museos&mgmtid=118f2fdbecc63410VgnVCM1000000b205a0aRCRD&preview=full")
    return HttpResponse('Se han actualizado los museos')


def cargar_museos(lista):
    museos = Museo.objects.all()
    for museo in museos:
        lista[museo.nombre]= 0

def cargar_comentarios(lista):
    comentarios = Comentario.objects.all()
    claves=lista.keys()
    for comentario in comentarios:
        for clave in claves:
            if clave==comentario.museo.nombre:
                lista[comentario.museo.nombre]+= 1
                break

def cargar_accesibles(lista_comentados):
    cont=0
    museos = Museo.objects.all()
    respuesta="<ul>"
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
    return respuesta

def cargar_comentados(lista_comentados):
    cont=0
    museos = Museo.objects.all()
    respuesta="<ul>"
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
    return respuesta

def add_seleccion(request):
    if request.user.is_authenticated():
        nombre = request.GET.get('like')
        if str(nombre)!='None':
            museo= Museo.objects.get(nombre=nombre)
            usuario=Usuario.objects.get(nombre=request.user)
            seleccion = Seleccion(museo=museo, usuario=usuario)
            seleccion.save()

@csrf_exempt
def museos(request):
    lista = {}
    existe = False
    museos = Museo.objects.all()
    FORMULARIO_DISTRITO = '<form action= "" Method= "POST"><p>Opciones:<select name="opcion">'
    FORMULARIO_LIKE = '<form action= "" Method= "GET"><p>Me gusta: <select name="like">'
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
                FORMULARIO_LIKE+="<option>"+ museo.nombre + "</option>"
    else:
        for museo in museos:
            respuesta += '<li><a href= "' + museo.enlace +'">' + museo.nombre + "</a></ul><ul>"
            FORMULARIO_LIKE+="<option>"+ museo.nombre + "</option>"

    FORMULARIO_LIKE+='</select></p><p><input type="submit" value="Enviar datos"></p></form>'
    respuesta = FORMULARIO_DISTRITO + respuesta
    add_seleccion(request)   
    respuesta += FORMULARIO_LIKE
    return HttpResponse (respuesta)

@csrf_exempt
def museo(request,numero):
    if request.method == "POST":
        comentario = Comentario(texto=request.POST['comentario'], museo=Museo.objects.get(id=int(numero)), usuario=Usuario.objects.get(nombre=request.user))
        comentario.save()
    museo = Museo.objects.get(id=numero)
    respuesta = "Nombre: " + museo.nombre + "</br>"
    respuesta += "Distrito: " + museo.distrito+ "</br>"
    respuesta += "Barrio: " + museo.barrio+ "</br>"
    respuesta += "Descripcion: " + museo.descripcion+ "</br>"
    respuesta += "Enlace: " + museo.enlace+ "</br>"
    respuesta += "Email: " + museo.email+ "</br>"
    respuesta += "Fax: " + museo.fax+ "</br>"
    respuesta += "Telefono: " + museo.telefono+ "</br>"
    respuesta += "Accesibilidad: " + museo.accesibilidad+ "</br>"
    respuesta += "Comentarios:</br>"
    comentarios = Comentario.objects.filter(museo_id=numero)
    for comentario in comentarios:
        respuesta += "<ul><li>Usuario: " + str(comentario.usuario)+ " Fecha: " + str(comentario.fecha)
        respuesta += '<li type= "circle">' + comentario.texto + "</ul>"

    if request.user.is_authenticated():
        respuesta += FORMULARIO_COMENTARIO

    return HttpResponse (respuesta)

def listar_museos(page,seleccionados,numero,usuario):
    respuesta = "<ul>"
    cont=0
    if str(page) == "None":
        page = '0'
        ultimo = 4
        primero = int(page)
    else:
        primero = int(page)*5
        ultimo = primero + 5 - 1

    for element in seleccionados:
        if (cont >= primero):
            if (cont > ultimo):
                cont = int(page)+1
                respuesta+= '<a href= "/usuario/' +  str(usuario.id) + "?page="+ str(cont) + '">' + "Más</a>"
                break
            respuesta += '<li><a href= "' + element.museo.enlace +'">' + element.museo.nombre + "</a><ul>"
            respuesta += '<li type= "circle">Barrio: ' + element.museo.barrio + '; Distrito: '+ element.museo.distrito
            respuesta += '<li type= "circle"><a href= "/museos/' + str(element.museo.id) +'">' + "Más información</a></ul>"
        cont+=1
    if (int(page) > 0):
        cont = int(page) -1
        respuesta += '</br><a href= "/usuario/' +  str(usuario.id) + "?page="+ str(cont) + '">' + "Página anterior</a>"
    return respuesta

@csrf_exempt
def usuario(request, numero):
    respuesta = ""
    seleccionados = Seleccion.objects.filter(usuario_id=numero)
    try:
        usuario = Usuario.objects.get(id=str(numero))
    except Usuario.DoesNotExist:
        return HttpResponseNotFound('<h1>' + numero + ' not found</h1>')

    page = request.GET.get('page')
    respuesta += listar_museos(page,seleccionados,numero,usuario)
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
    respuesta=""
    lista_comentados = []
    lista = {}
    comentarios = Comentario.objects.all()
    usuarios = Usuario.objects.all()
    cargar_museos(lista)
    cargar_comentarios(lista)
    lista_comentados=sorted(lista.items(), key=operator.itemgetter(1))
    lista_comentados.reverse()
    if request.method == "POST":
        respuesta += cargar_accesibles(lista_comentados)
    else:
        respuesta += cargar_comentados(lista_comentados)
    respuesta += "</ul>"
#    print (lista_comentados)
    respuesta += '</br></br></br></br></br>'
    for usuario in usuarios:
        respuesta += '<ul><li type= "circle">Usuario: ' + str(usuario.nombre) +". Título: "
        if str(usuario.titulo)!= "":
            respuesta += '<a href= "/usuario/' + str(usuario.id) +'">' + str(usuario.titulo)+"</a></ul>"
        else:
            respuesta += '<a href= "/usuario/' + str(usuario.id) +'">'+"Página de "+str(usuario.nombre)+"</a></ul>"
#Te falta configurar lo del titulo

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
