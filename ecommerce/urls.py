
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.conf.urls.static import static
from django.conf import settings

from core import views
from catalog import views as views_catalog

urlpatterns = [
	url(r'^$', views.index,  name='index'),
	url(r'^contato/$', views.contact, name='contact'),
	#url(r'^produtodetalhe/$', views.product_detail, name='product_detail'),
	
    url(r'^catalogo/', include('catalog.urls', namespace='catalog')),
    url(r'^carrinho/$', views.chart, name='chart'),
    url(r'^logar/$', login, {'template_name': 'login.html'}, name='login'),
    url(r'^conta/', include('accounts.urls', namespace='accounts')),
    url(r'^sair/$', logout, {'next_page': 'index'}, name='logout'),
    url(r'^checkout/$', views.checkout, name='checkout'),
    url(r'^compras/', include('checkout.urls', namespace='checkout')),
    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )