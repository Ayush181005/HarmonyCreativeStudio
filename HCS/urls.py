"""HCS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from home.sitemaps import StaticViewSitemap as homeSitemap, dispPortfolioSitemap
from blog.sitemaps import StaticViewSitemap as blogSitemap, PostSitemap

sitemaps = {
    'homeSitemap': homeSitemap,
    'blogSitemap': blogSitemap,
    'dispPortfolio': dispPortfolioSitemap,
    'postSitemap': PostSitemap,
}

handler404 = 'home.views.page_not_found_view'
handler500 = 'home.views.internal_server_error_view'

admin.site.site_header = "HCS Admin"
admin.site.site_title = "HarmonyCreativeStudio"
admin.site.index_title = "Welcome to HCS Administration"

urlpatterns = [
    path('hcs-admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps':sitemaps}),
    path('', include('home.urls')),
    path('blog/', include('blog.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
