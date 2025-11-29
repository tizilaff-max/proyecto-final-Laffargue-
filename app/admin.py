# app/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Catalogo, Producto

@admin.register(Catalogo)
class CatalogoAdmin(admin.ModelAdmin):
    list_display = ('titulo',)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'categoria', 'miniatura')
    list_filter = ('categoria',)
    search_fields = ('nombre', 'categoria__titulo')

    def miniatura(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" style="max-height:60px;"/>', obj.imagen.url)
        return "(sin imagen)"
    miniatura.short_description = 'Imagen'
