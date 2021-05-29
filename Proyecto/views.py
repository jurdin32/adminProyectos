import datetime

from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
from Proyecto.models import Proyecto, Requerimiento, Analisis_Requerimientos, Priorizacion, DiagramaProcesos, \
    ApartadosAplicacion

lista_tipos=[
    'BooleanField',
    'CharField',
    'DateField',
    'DateTimeField',
    'DecimalField',
    'EmailField',
    'FileField',
    'ImageField',
    'IntegerField',
    'GenericIPAddressField',
    'MultipleChoiceField',
    'TypedMultipleChoiceField',
    'NullBooleanField',
    'RegexField',
    'SlugField',
    'TimeField',
    'URLField',
    'UUIDField',
    'ComboField',
    'MultiValueField',
    'SplitDateTimeField',
    'ModelMultipleChoiceField',
    'ModelChoiceField',
    'TextField',
]
#paso 1
def registroProyecto(request):
    if request.POST:
        print(request.POST)
        Proyecto.objects.create(
            fecha_inicio=request.POST.get('fecha'),
            cliente=request.POST.get('cliente'),
            nombre=request.POST.get('nombre'),
            descripcion=request.POST.get('descripcion'),
        ).save()
        messages.add_message(request,messages.INFO,'El registro se ha creado exitosamente..!')

    contexto={
        'fecha':datetime.datetime.now()
    }
    return render(request,'registro_proyecto.html',contexto)

#paso2
def requerimientos(request):
    proyectos=Proyecto.objects.all()
    proy=None
    requerimiento=None
    if request.GET.get('proj'):
        proy=proyectos.get(id=request.GET.get('proj'))
        requerimiento=proy.requerimiento_set.all()
    if request.POST:
        print(request.POST)
        if request.GET.get('proj'):
            Requerimiento.objects.create(
                proyecto_id=request.GET.get('proj'),
                descripcion = request.POST.get('requerimiento'),
            ).save()
            messages.add_message(request,messages.SUCCESS,'El requerimiento fué agregado..!')
        else:
          messages.add_message(request,messages.ERROR, 'No se puede registrar un requerimiento sin seleccionar un proyecto')
    contexto={
        'proyectos':proyectos,
        'proy':proy,
        'requerimientos':requerimiento,
    }
    return render(request,'requerimientos.html',contexto)

def editarRequerimiento(request,id):
    req=Requerimiento.objects.get(id=id)
    if request.POST:
        req.descripcion=request.POST.get('des')
        req.apartado_id= request.POST.get('apartado')
        req.save()
        messages.add_message(request,messages.SUCCESS,'Los cambios se realizarón con exito..!')
    return HttpResponseRedirect("/projects/requirements/?proj=%s" % req.proyecto_id)

def agregarApartado(request,id):
    proy=Proyecto.objects.get(id=id)
    ApartadosAplicacion.objects.create(
        proyecto=proy,
        nombre=request.POST.get('seccion')
    ).save()
    messages.add_message(request, messages.SUCCESS, 'Se ha creado un nuevo proceso..!')
    return HttpResponseRedirect("/projects/requirements/diagrama_process/?type=PROCESOS&proy=%s"%proy.id)

def eliminarRequerimiento(request,id):
    proy=None
    try:
        req=Requerimiento.objects.get(id=id)
        proy=req.proyecto_id
        req.delete()
        messages.add_message(request, messages.SUCCESS, 'El requerimiento fué eliminado con exito..!')
        return HttpResponseRedirect("/projects/requirements/?proj=%s" % proy)
    except:
        messages.add_message(request, messages.ERROR,'Al parecer esta intentando borrar un objeto que no existe..!')
        return HttpResponseRedirect("/projects/requirements/")


#paso 3
def tablas(id):
    tablas= Analisis_Requerimientos.objects.filter(requerimiento__proyecto_id=id)
    lista = []
    tabl =[]
    for t in tablas:
        if not t.nombre_tabla in lista:
            lista.append(t.nombre_tabla)
            tabl.append({'id':t.requerimiento_id,'tabla':t.nombre_tabla,'idT':t.id})
    return tabl


def analisis_requerimientos(request,id):
    proy=Proyecto.objects.get(id=id)
    contexto={
        'proyecto':proy,
        'tablas':tablas(proy.id),
        'lista_tipos':lista_tipos,
        'analisis':Analisis_Requerimientos.objects.filter(requerimiento__proyecto=proy)
    }
    return render(request,'analisis_requerimientos.html',contexto)

def agregarAnalisisTabla(request,id):
    analisis=Analisis_Requerimientos.objects.create(
        requerimiento_id=id,
        nombre_tabla = request.POST.get('tabla'),
        nombre_campo = request.POST.get('campo'),
        tipo = request.POST.get('tipo'),
        descripcion = request.POST.get('des')
    )
    analisis.save()
    print(analisis)
    messages.add_message(request, messages.SUCCESS, 'Se agregó nuevo campo a la tabla seleccionada..!')
    return HttpResponseRedirect('/projects/requirements/analystic/%s/'%analisis.requerimiento.proyecto_id)

def agregarTabla(request):
    analisis=Analisis_Requerimientos.objects.create(
        requerimiento_id=request.POST.get('req'),
        nombre_tabla = request.POST.get('tabla')
    )
    analisis.save()
    print(analisis)
    messages.add_message(request, messages.SUCCESS, 'Se agregó nuevo campo a la tabla seleccionada..!')
    return HttpResponseRedirect('/projects/requirements/?proj=%s'%analisis.requerimiento.proyecto_id)

def eliminarTabla(request,id):
    analisis=Analisis_Requerimientos.objects.get(id=id)
    proy=analisis.requerimiento.proyecto_id
    for an in Analisis_Requerimientos.objects.filter(requerimiento_id=analisis.requerimiento_id):
        an.delete()
    messages.add_message(request, messages.SUCCESS, 'Se han eliminado todos los datos relacionados a la tabla..!')
    return HttpResponseRedirect('/projects/requirements/analystic/%s/' % proy )

def eliminarCampoTabla(request,id):
    analisis=Analisis_Requerimientos.objects.get(id=id)
    proy=analisis.requerimiento.proyecto_id
    analisis.delete()
    messages.add_message(request, messages.SUCCESS, 'Se ha eliminado el campo de datos..!')
    return HttpResponseRedirect('/projects/requirements/analystic/%s/' % proy )

def opcionesMenu(request):
    return ""
#paso 4
def priorizacion_requerimientos(request):
    proyectos = Proyecto.objects.all()
    proy = None
    requerimiento = None
    if request.GET.get('proj'):
        proy = proyectos.get(id=request.GET.get('proj'))
        requerimiento = proy.requerimiento_set.all()
    if request.GET.get('priori'):
        requerimiento = proy.requerimiento_set.filter(prioridad=request.GET.get('priori'))
    if request.POST:
        pass
    contexto = {
        'proyectos': proyectos,
        'proy': proy,
        'requerimientos': requerimiento,
    }
    return render(request,'priorizacion_requerimientos.html',contexto)

def cambiarPrioridad(request,id):
    req=Requerimiento.objects.get(id=id)
    req.prioridad=request.POST.get('prior')
    req.save()
    print(id,request.POST.get('prior'))
    messages.add_message(request, messages.SUCCESS, 'Se ha cambiado la prioridad..!')
    return HttpResponseRedirect("/projects/requirements/priority/?proj=%s#xx%s"%(req.proyecto_id,req.id))

def plan_actividades(request):
    requerimients=None
    proyectos = Proyecto.objects.all()
    proy=None
    if request.GET.get('proy'):
        requerimients=Requerimiento.objects.filter(proyecto_id=request.GET.get('proy'))
        proy=proyectos.get(id=request.GET.get('proy'))

    if request.POST:
        print(request.POST)
        clase=''
        requer=requerimients.get(id=request.POST.get('requerimiento'))
        if requer.prioridad == "ALTA":
            clase='bg-danger'
        elif requer.prioridad == "MEDIA":
            clase='bg-info'
        elif requer.prioridad == "BAJA":
            clase = 'bg-success'
        else:
            clase='bg-warning'

        Priorizacion.objects.create(
            requerimiento= requer,
            fecha_inicio = request.POST.get('f1'),
            fecha_fin = request.POST.get('f2'),
            className = clase
        ).save()
        messages.add_message(request, messages.SUCCESS, 'Se ha creado una entrada..!')
    contexto={
        'proyectos':proyectos,
        'proy':proy,
        'requerimientos':requerimients,
        'priorizaciones':Priorizacion.objects.filter(requerimiento__proyecto_id=request.GET.get('proy')),
        'fecha':datetime.datetime.now().date()
    }
    return render(request,'plan_actividades.html',contexto)

def cambiar_fecha_actividad(request):
    fecha1=datetime.datetime.strptime(request.POST.get('fi'),"%Y-%m-%d").date()
    fecha2=datetime.datetime.strptime(request.POST.get('ff'),"%Y-%m-%d").date()
    id=request.POST.get('idp')
    priory=Priorizacion.objects.get(id=id)
    priory.fecha_inicio=fecha1
    priory.fecha_fin=fecha2
    priory.save()
    messages.add_message(request, messages.SUCCESS, 'Se ha modificado la fecha de la prioridad..!')
    return HttpResponseRedirect("/projects/requirements/planning/?proy=%s"%priory.requerimiento.proyecto_id)

def diagrama_procesos(request):
    proy=None
    diagrama=None
    proyectos=Proyecto.objects.all()
    try:
        diagrama = DiagramaProcesos.objects.filter(tipo=request.GET.get('type'),proyecto_id=request.GET.get('proy')).first()
    except:
        pass
    if request.GET.get('proy'):
        proy=proyectos.get(id=request.GET.get('proy'))
    if request.POST:
        try:
            diagrama.diagrama=request.POST.get('diagrama')
            diagrama.save()
            messages.add_message(request, messages.SUCCESS, 'El diagrama se actualizó..!')
        except:
            DiagramaProcesos.objects.create(
                proyecto_id=proy.id,
                tipo=request.GET.get('type'),
                diagrama=request.POST.get('diagrama')
            ).save()
            messages.add_message(request,messages.SUCCESS,'Los cambios se registraron correctmente..!')
    contexto={
        'proyectos':proyectos,
        'proy':proy,
        'diagrama':diagrama,
    }
    return render(request,'diagrama_procesos.html',contexto)

