import datetime

from django.db import models



choicies =(
    ('BooleanField','BooleanField'),
    ( 'CharField', 'CharField'),
    ('DateField','DateField'),
    ('DateTimeField','DateTimeField'),
    ('DecimalField','DecimalField'),
    ('EmailField','EmailField'),
    ('FileField','FileField'),
    ('ImageField','ImageField'),
    ('IntegerField','IntegerField'),
    (' GenericIPAddressField',' GenericIPAddressField'),
    ('MultipleChoiceField','MultipleChoiceField'),
    ('TypedMultipleChoiceField','TypedMultipleChoiceField'),
    ('NullBooleanField','NullBooleanField'),
    ('RegexField','RegexField'),
    ('SlugField','SlugField'),
    ('TimeField','TimeField'),
    ('URLField','URLField'),
    ('UUIDField','UUIDField'),
    ('ComboField','ComboField'),
    ('MultiValueField','MultiValueField'),
    ('SplitDateTimeField','SplitDateTimeField'),
    ('ModelMultipleChoiceField','ModelMultipleChoiceField'),
    ('ModelChoiceField','ModelChoiceField'),
    ('TextField','TextField')
)



# Create your models here.
class Proyecto(models.Model):
    nombre=models.CharField(max_length=50)
    fecha_inicio=models.DateField()
    cliente=models.CharField(max_length=100)
    descripcion=models.TextField()

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural="E1 Especificaiones del Proyecto"

class ApartadosAplicacion(models.Model):
    proyecto=models.ForeignKey(Proyecto,on_delete=models.CASCADE,null=True,blank=True)
    nombre=models.CharField(max_length=50)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        apartados = ApartadosAplicacion.objects.filter(proyecto_id=self.proyecto_id)
        strGANTT = """graph TD\nA[Diagramas del %s]"""%self.proyecto.nombre
        contador=1
        for ap in apartados:
            strGANTT+="\nA-->%s [%s]"%(contador,self.nombre)
            contador+=1
        super(ApartadosAplicacion, self).save()

    class Meta:
        verbose_name_plural="E1.1 Apartados del Proyecto"


class Requerimiento(models.Model):
    proyecto=models.ForeignKey(Proyecto,on_delete=models.CASCADE)
    descripcion=models.TextField()
    prioridad=models.CharField(max_length=30,default="SIN PRIORIDAD")

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name_plural="E2 Requerimientos del Software"


class Analisis_Requerimientos(models.Model):
    requerimiento=models.ForeignKey(Requerimiento,on_delete=models.CASCADE)
    nombre_tabla=models.CharField(max_length=30,default="NOMBRE DEL OBJETO")
    nombre_campo=models.CharField(max_length=30)
    tipo=models.CharField(max_length=30, choices=choicies)
    descripcion=models.TextField()

    def __str__(self):
        return "%s: %s >> %s"%(self.nombre_campo,self.tipo,self.descripcion)


    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.nombre_tabla=str.upper(self.nombre_tabla)
        super(Analisis_Requerimientos, self).save()

    class Meta:
        verbose_name_plural="E3 Analisis de requerimientos"

class Priorizacion(models.Model):
    requerimiento=models.ForeignKey(Requerimiento,on_delete=models.CASCADE)
    fecha_inicio= models.DateField()
    fecha_fin= models.DateField()
    className=models.CharField(max_length=30)
    dias=models.IntegerField(default=1)
    
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        fi= datetime.datetime.strptime(str(self.fecha_inicio), "%Y-%m-%d")
        ff= datetime.datetime.strptime(str(self.fecha_fin), "%Y-%m-%d")
        dias=abs((ff - fi).days)
        if dias==0:
            dias=1
        self.dias=dias
        requerimientos=Priorizacion.objects.filter(requerimiento__proyecto_id=self.requerimiento.proyecto_id)
        strGANTT="""gantt\ntitle Diagrama de tiempos\ndateFormat  YYYY-MM-DD"""

        contador=1
        dias=0
        fecha1=""
        for req in requerimientos:
            strGANTT+='\nRequerimiento [%s]:a1, %s, %sd'%(contador,req.fecha_inicio,req.dias)
            dias+=req.dias
            if contador==1:
                fecha1=req.fecha_inicio
            contador += 1
        strGANTT +='\nRetroalimentación: a1, %s, %sd'%(fecha1,dias)
        try:
            diagrama=DiagramaProcesos.objects.get(proyecto_id=self.requerimiento.proyecto_id,tipo="GANTT")
            diagrama.diagrama=strGANTT
            diagrama.save()
        except:
            DiagramaProcesos.objects.create(
                proyecto_id=self.requerimiento.proyecto_id,
                tipo='GANTT',
                diagrama=strGANTT,

            )
        super(Priorizacion, self).save()

    class Meta:
        verbose_name_plural="E4 Priorización de actividades"

class DiagramaProcesos(models.Model):
    tipo=models.CharField(max_length=30,default="PROCESOS")
    proyecto=models.ForeignKey(Proyecto,on_delete=models.CASCADE)
    diagrama=models.TextField()

    class Meta:
        verbose_name_plural = "E5 Diagrama de procesos"





