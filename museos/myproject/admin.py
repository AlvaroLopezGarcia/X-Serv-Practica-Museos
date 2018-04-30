from django.contrib import admin
from django.contrib.auth.views import logout, login
# Register your models here.


from .models import Museo
from .models import Usuario
from .models import Comentario
from .models import Seleccion

admin.site.register(Museo)
admin.site.register(Usuario)
admin.site.register(Comentario)
admin.site.register(Seleccion)
