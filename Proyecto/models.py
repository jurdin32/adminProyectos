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

    class Meta:
        verbose_name_plural="E4 Priorización de actividades"





