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
    telefono = models.IntegerField()
    accesibilidad = models.IntegerField()
    def __str__(self):
        return self.nombre

class Usuario(models.Model):
    nombre = models.OneToOneField(User)
    titulo = models.CharField(max_length=256)
    letracolor = models.CharField(max_length=256)
    tamaño = models.CharField(max_length=256)
    fondocolor = models.CharField(max_length=256)
    def __str__(self):
        return self.nombre

class Comentario(models.Model):
    texto = models.TextField()
    museo = models.ForeignKey(Museo)
    usuario = models.ForeignKey(Usuario)

class Seleccion(models.Model):
    museo = models.ForeignKey(Museo)
    usuario = models.ForeignKey(Usuario)
    fecha = models.DateTimeField(default=timezone.now)
