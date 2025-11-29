
from django.conf.urls.static import static
from django.urls import include, path
from . import views, admin
from django.conf import settings


urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('categorias/', views.categorias, name='categorias'),
    path('productos/', views.ProductoListView.as_view(), name='lista_productos'),
    path('productos/<str:nombre_categoria>/', views.productos_por_categoria, name='productos_por_categoria'),
    path('producto/detalle/<int:pk>/', views.detalle_producto, name='detalle_producto'),
    path('producto/editar/<int:pk>/', views.editar_producto, name='editar_producto'),
    path('producto/borrar/<int:pk>/', views.borrar_producto, name='borrar_producto'),
    path('producto/crear/', views.crear_producto, name='crear_producto'),
    path('catalogo/crear/', views.CatalogoCreateView.as_view(), name='crear_catalogo'),
    path('about/', views.about, name='about'),
    path('cuentas/', include('cuentas.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
