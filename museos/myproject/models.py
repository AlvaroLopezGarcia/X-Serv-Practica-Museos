from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class Museo(models.Model):
    nombre = models.CharField(max_length=256)
    distrito = models.CharField(max_length=256)
    barrio = models.CharField(max_length=256)
    descripcion = models.TextField()
    enlace = models.TextField()
    email = models.TextField()
    fax = models.TextField()
    telefono = models.TextField()
    accesibilidad = models.TextField()
    def __str__(self):
        return self.nombre

class Usuario(models.Model):
    nombre = models.OneToOneField(User)
    titulo = models.CharField(max_length=256)
    tamaño = models.CharField(max_length=256)
    fondocolor = models.CharField(max_length=256)
    def __str__(self):
        return self.nombre.username

class Comentario(models.Model):
    texto = models.TextField()
    museo = models.ForeignKey(Museo)
    usuario = models.ForeignKey(Usuario)
    fecha = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.museo.nombre

class Seleccion(models.Model):
    museo = models.ForeignKey(Museo)
    usuario = models.ForeignKey(Usuario)
    fecha = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.usuario.nombre.username
