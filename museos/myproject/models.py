from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone.now
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

class Usuario(models.model):
    nombre = models.models.OneToOneField(User)
    titulo = models.CharField(max_length=256)
    letracolor = models.CharField(max_length=256)
    tamaño = models.CharField(max_length=256)
    fondocolor = models.CharField(max_length=256)
    def __str__(self):
        return self.nombre

class Comentario(models.model):
    texto = models.TextField()
    museo = models.ForeignKey(Museo)
    usuario = models.ForeignKey(Usuario)

class Seleccion():
    museo = models.ForeignKey(Museo)
    usuario = models.ForeignKey(Usuario)
    fecha = models.DateTimeField(default=timezone.now)
