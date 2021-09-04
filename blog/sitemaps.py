from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from blog.models import Post

class StaticViewSitemap(Sitemap):
    def items(self):
        return ['blogHome']
    
    def location(self, item):
        return reverse(item)

class PostSitemap(Sitemap):
    def items(self):
        return Post.objects.all()
