from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from product_hunt import settings
from . import views

urlpatterns = [
    path('', views.homePage, name='home_page'),
    path('about/', views.aboutPage, name='about_page'),
    path('contact/', views.contactPage, name='contact_page'),
    path('product/', include('products.urls')),
    path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
