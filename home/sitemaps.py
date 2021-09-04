from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from home.models import Portfolio

class StaticViewSitemap(Sitemap):
    def items(self):
        return ['home', 'portfolio']
    
    def location(self, item):
        return reverse(item)

class dispPortfolioSitemap(Sitemap):
    def items(self):
        return Portfolio.objects.all()
