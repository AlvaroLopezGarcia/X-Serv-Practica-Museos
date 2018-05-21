#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Simple XML parser for the RSS channel from BarraPunto
# Jesus M. Gonzalez-Barahona
# jgb @ gsyc.es
# TSAI and SAT subjects (Universidad Rey Juan Carlos)
# September 2009
#
# Just prints the news (and urls) in BarraPunto.com,
#  after reading the corresponding RSS channel.

from xml.sax.handler import ContentHandler
from .models import Museo

class myContentHandler(ContentHandler):

    def __init__ (self):
        self.inItem = False
        self.inContent = False
        self.theContent = ""
        self.inNombre = False
        self.inBarrio = False
        self.inDistrito = False
        self.inDescripcion = False
        self.inEnlace = False
        self.inEmail = False
        self.inFax = False
        self.inTelefono = False
        self.inAccesibilidad = False

        self.atributos = {'Nombre':'','Barrio':'','Distrito':'','Descripcion':'','Enlace':'','Email':'',
                     'Fax':'','Telefono':'','Accesibilidad':''}


    def startElement (self, name, attrs):
        if name == 'atributos':
            self.inItem = True
        elif self.inItem:
            if name == 'atributo':
                if attrs['nombre'] == 'NOMBRE':
                    self.inContent = True
                    self.inNombre = True
                elif attrs['nombre'] == 'BARRIO':
                    self.inContent = True
                    self.inBarrio = True
                elif attrs['nombre'] == 'DISTRITO':
                    self.inContent = True
                    self.inDistrito = True
                elif attrs['nombre'] == 'DESCRIPCION':
                    self.inContent = True
                    self.inDescripcion = True
                elif attrs['nombre'] == 'CONTENT-URL':
                    self.inContent = True
                    self.inEnlace = True
                elif attrs['nombre'] == 'EMAIL':
                    self.inContent = True
                    self.inEmail = True
                elif attrs['nombre'] == 'FAX':
                    self.inContent = True
                    self.inFax = True
                elif attrs['nombre'] == 'TELEFONO':
                    self.inContent = True
                    self.inTelefono = True
                elif attrs['nombre'] == 'ACCESIBILIDAD':
                    self.inContent = True
                    self.inAccesibilidad = True


    def endElement (self, name):
        if name == 'atributos':
            museo = Museo(nombre=self.atributos['Nombre'], barrio=self.atributos['Barrio'],
                            distrito=self.atributos['Distrito'], descripcion=self.atributos['Descripcion'],
                            enlace=self.atributos['Enlace'], email=self.atributos['Email'],
                            fax=self.atributos['Fax'], telefono=self.atributos['Telefono'],
                            accesibilidad=self.atributos['Accesibilidad'])
            museo.save()
            self.inItem = False
            for atributo in self.atributos.keys():
                self.atributos[atributo]= ""

        elif self.inItem:
            if name == 'atributo':
                if self.inNombre:
                    self.atributos['Nombre']= self.theContent
                    self.inNombre = False
                    self.theContent = ""
                    self.inContent = False
                if self.inBarrio:
                    self.atributos['Barrio']= self.theContent
                    self.inBarrio = False
                    self.theContent = ""
                    self.inContent = False
                if self.inDistrito:
                    self.atributos['Distrito']= self.theContent
                    self.inDistrito = False
                    self.theContent = ""
                    self.inContent = False
                if self.inDescripcion:
                    self.atributos['Descripcion']= self.theContent
                    self.inDescripcion = False
                    self.theContent = ""
                    self.inContent = False
                if self.inEnlace:
                    self.atributos['Enlace']= self.theContent
                    self.inEnlace = False
                    self.theContent = ""
                    self.inContent = False
                if self.inEmail:
                    self.atributos['Email']= self.theContent
                    self.inEmail = False
                    self.theContent = ""
                    self.inContent = False
                if self.inFax:
                    self.atributos['Fax']= self.theContent
                    self.inFax = False
                    self.theContent = ""
                    self.inContent = False
                if self.inTelefono:
                    self.atributos['Telefono']= self.theContent
                    self.inTelefono = False
                    self.theContent = ""
                    self.inContent = False
                if self.inAccesibilidad:
                    self.atributos['Accesibilidad']= self.theContent
                    self.inAccesibilidad = False
                    self.theContent = ""
                    self.inContent = False

    def characters (self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars


print ("Parse complete")
