from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from operator import itemgetter
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from .models import Museo
from .models import Comentario
from .models import Usuario
from .models import Seleccion
from xml.sax import make_parser
from .xmlparser import myContentHandler
from django.template import Context
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
    <input type= 'hidden' name='opcion' value='1'>
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
            break
    return respuesta

def add_seleccion(request):
    if request.user.is_authenticated():
        nombre = request.GET.get('like')
        if str(nombre)!='None':
            museo= Museo.objects.get(nombre=nombre)
            usuario=Usuario.objects.get(nombre=request.user)
            seleccion = Seleccion(museo=museo, usuario=usuario)
            seleccion.save()


def selecciona_favorito(usuario, museo):
    seleccionados = Seleccion.objects.all()
    existe = False

    for seleccionado in seleccionados:
        if str(seleccionado.museo.nombre) == str(museo):
            existe = True
            FORMULARIO_LIKE =""
            break
    if not existe:
        FORMULARIO_LIKE = "<form action='/museos/" + str(museo.id) + "' Method='POST'><input type='submit' value='Like'><input type= 'hidden' name='usuario' value= " + usuario + "><input type= 'hidden' name='opcion' value='2'></form>"

    return FORMULARIO_LIKE

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
                respuesta += "<li><a href= /museos/" + str(museo.id)+">" + museo.nombre + "</a></ul><ul>"
    else:
        for museo in museos:
            respuesta += "<li><a href= /museos/" + str(museo.id)+">" + museo.nombre + "</a></ul><ul>"

    respuesta = FORMULARIO_DISTRITO + respuesta
    add_seleccion(request)
    logueo = Login_info(request)
    template = get_template('basic/index.html')
    c = Context({'contenido':respuesta, 'formulario_logueo':logueo})
    return HttpResponse (template.render(c))

@csrf_exempt
def museo(request,numero):
    if request.method == "POST":
         opcion= request.POST['opcion']
         if opcion == "1":
             comentario = Comentario(texto=request.POST['comentario'], museo=Museo.objects.get(id=int(numero)), usuario=Usuario.objects.get(nombre=request.user))
             comentario.save()
             comentario.save()
         elif opcion == "2":
             seleccionado = Seleccion(museo = Museo.objects.get(id=numero), usuario = Usuario.objects.get(nombre = request.user))
             seleccionado.save()

    museo = Museo.objects.get(id=numero)
    respuesta = "Nombre: " + museo.nombre + "</br>"
    respuesta += "Distrito: " + museo.distrito+ "</br>"
    respuesta += "Barrio: " + museo.barrio+ "</br>"
    respuesta += "Descripcion: " + museo.descripcion+ "</br>"
    respuesta += "Enlace: " + "<a href= " + museo.enlace + ">" + museo.enlace + "</a></br>"
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
        respuesta += selecciona_favorito(str(request.user), museo)
    logueo = Login_info(request)
    template = get_template('basic/index.html')
    c = Context({'contenido':respuesta, 'formulario_logueo':logueo})
    return HttpResponse (template.render(c))
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
            respuesta += "; Fecha: " + str(element.fecha)
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
    respuesta += '</ul>'
    logueo = Login_info(request)
    if request.user.is_authenticated():
        if request.user.username == str(usuario.nombre):
            respuesta += FORMULARIO_USUARIO

    if request.method == "POST":
        opcion= request.POST['opcion']
        valor = request.POST['valor']
        if opcion == 'Titulo':
            if valor != "":
                usuario.titulo = valor
            else:
                usuario.titulo = "Página de " + str(request.user)
        elif opcion == 'Tamaño':
            usuario.tamaño = valor
        elif opcion == 'Fondo Color':
            usuario.fondocolor = valor

        usuario.save()
    template = get_template('basic/index.html')
    c = Context({'contenido':respuesta, 'formulario_logueo':logueo})
    return HttpResponse (template.render(c))

@csrf_exempt
def Login(request):
    user = request.POST['user']
    password = request.POST['password']
    user = authenticate(username=user, password=password)
    if user is not None:
        login(request, user)
    return redirect("/")

def Login_info(request):
    if request.user.is_authenticated():
        log = "<p>Logged in as " + request.user.username
        log += "<a href='/logout'> Logout </a></p>"
    else:
        log = "<form action='/login' method='post'>"
        log += "Usuario:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <input type= 'text' name='user'><br>"
        log += "Contraseña: <input type= 'password' name='password'>"
        log += "<input type= 'submit' value='enviar'>"
        log += "</form>"
    return log

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
    lista_usuarios= "Usuarios:</br>"
    for usuario in usuarios:
        lista_usuarios += '<ul><li type= "circle">Usuario: ' + str(usuario.nombre) +". Título: "
        lista_usuarios += '<a href= "/usuario/' + str(usuario.id) +'">' + str(usuario.titulo)+"</a></ul>"

    if request.method == "POST":
        respuesta += '</ul>'+FORMULARIO
    else:
        respuesta += '</ul>'+FORMULARIO_ACCESIBILIDAD

    logueo = Login_info(request)
    template = get_template('basic/index.html')
    c = Context({'contenido':respuesta, 'lista_usuarios':lista_usuarios, 'formulario_logueo':logueo})
    return HttpResponse (template.render(c))

# http://www.forosdelweb.com/f14/como-utilizar-simbolo-xml-sin-morir-intento-686694/
# He usado esta url para evitar que me diera error en el xml con el caracter &
def usuario_xml(request, numero):
    respuesta= """<?xml version="1.0" encoding="utf-8"?>"""
    respuesta += """\n\n<Contenidos>\n"""
    seleccionados = Seleccion.objects.filter(usuario_id=numero)
    for seleccionado in seleccionados:
        respuesta += """\t<contenido>\n"""
        respuesta += """\t\t<atributo nombre="NOMBRE">""" + seleccionado.museo.nombre + """</atributo>\n"""
        respuesta += """\t\t<atributo nombre="DESCRIPCION"><![CDATA[""" + seleccionado.museo.descripcion + """]]></atributo>\n"""
        respuesta += """\t\t<atributo nombre="ACCESIBILIDAD">""" + seleccionado.museo.accesibilidad + """</atributo>\n"""
        respuesta += """\t\t<atributo nombre="CONTENT-URL"><![CDATA[""" + seleccionado.museo.enlace + """]]></atributo>\n"""
        respuesta += """\t\t<atributo nombre="BARRIO">""" + seleccionado.museo.barrio + """</atributo>\n"""
        respuesta += """\t\t<atributo nombre="DISTRITO">""" + seleccionado.museo.distrito + """</atributo>\n"""
        respuesta += """\t\t<atributo nombre="TELEFONO">""" + seleccionado.museo.telefono + """</atributo>\n"""
        respuesta += """\t\t<atributo nombre="FAX">""" + seleccionado.museo.fax + """</atributo>\n"""
        respuesta += """\t\t<atributo nombre="EMAIL">""" + seleccionado.museo.email + """</atributo>\n"""
        respuesta += """\t</contenido>\n"""

    respuesta += """</Contenidos>"""
    return HttpResponse (respuesta,content_type = 'text/xml')

def about(request):
    logueo = Login_info(request)
    respuesta= "Esta página es una servidor web que permite buscar información sobre los museos de la comunidad de Madrid. En caso de ser usuario, tiene a su disposición una serie de recursos como comentar o dar un 'me gusta' a los museos."
    template = get_template('basic/index.html')
    c = Context({'contenido':respuesta, 'formulario_logueo':logueo})
    return HttpResponse (template.render(c))

def css(request):
    if request.user.is_authenticated():
        print("Estoy authenticado")
        fondocolor = Usuario.objects.get(nombre=request.user).fondocolor
        print(fondocolor)
        letra = Usuario.objects.get(nombre=request.user).tamaño
    else:
        print("No estoy authenticado")
        fondocolor="white"
        letra="13"
    template = get_template('basic/styles/layout.css')
    c = Context({'color':fondocolor,'letra':letra})
    return HttpResponse (template.render(c),content_type="text/css")
