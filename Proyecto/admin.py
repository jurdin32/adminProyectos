from django.contrib import admin

# Register your models here.
from Proyecto.models import *
from adminProyectos.snniperModelAdmin import Attr



class RequerimientosInline(admin.StackedInline):
    model = Requerimiento
    extra = 0

@admin.register(Proyecto)
class AdminProyecto(admin.ModelAdmin):
    list_display = Attr(Proyecto)
    list_display_links = Attr(Proyecto)
    inlines = [RequerimientosInline]


class AnalisisRequerimientoInline(admin.StackedInline):
    model = Analisis_Requerimientos
    extra = 0

@admin.register(Requerimiento)
class AdminRequerimiento(admin.ModelAdmin):
    list_display = Attr(Requerimiento)
    list_display_links = Attr(Requerimiento)
    inlines = [AnalisisRequerimientoInline]

@admin.register(Analisis_Requerimientos)
class AdminAnalisis_Requerimientos(admin.ModelAdmin):
    list_display = Attr(Analisis_Requerimientos)
    list_display_links = Attr(Analisis_Requerimientos)

@admin.register(Priorizacion)
class AdminPriorizacion(admin.ModelAdmin):
    list_display = Attr(Priorizacion)
    list_display_links = Attr(Priorizacion)

@admin.register(DiagramaProcesos)
class AdminDiagramaProcesos(admin.ModelAdmin):
    list_display = Attr(DiagramaProcesos)
    list_display_links = Attr(DiagramaProcesos)