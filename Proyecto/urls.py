from django.urls import path

from Proyecto.views import *

urlpatterns = [
    path('register/', registroProyecto,name='registroProyecto'),
    path('requirements/', requerimientos,name='requerimientos'),
    path('requirements/remove/<int:id>/', eliminarRequerimiento,name='eliminarRequerimiento'),
    path('requirements/edit/<int:id>/', editarRequerimiento,name='editarRequerimiento'),
    path('requirements/analystic/<int:id>/', analisis_requerimientos,name='analisisRequerimiento'),
    path('requirements/analystic/add/<int:id>/', agregarAnalisisTabla,name='CampoTablaRequerimiento'),
    path('requirements/analystic/table/field/delete/<int:id>/', eliminarCampoTabla,name='eliminarCampoTabla'),
    path('requirements/analystic/table/', agregarTabla,name='agregarTabla'),
    path('requirements/analystic/table/delete/<int:id>/', eliminarTabla,name='eliminarTabla'),

    path('requirements/priority/', priorizacion_requerimientos,name='priorizacion'),
    path('requirements/change/priority/<int:id>/', cambiarPrioridad,name='cambiarPrioridad'),

    path('requirements/planning/', plan_actividades,name='plan_actividades'),
    path('requirements/move_date/', cambiar_fecha_actividad,name='cambiar_fecha_actividad'),
]