from django.db import models

class Catalogo(models.Model):
    titulo = models.CharField(max_length=100)

    def __str__(self):
        return self.titulo

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    categoria = models.ForeignKey(Catalogo, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
 
    def __str__(self):
        return self.nombre
