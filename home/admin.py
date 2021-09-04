from django.contrib import admin
from home.models import Contact, Testimonial, Portfolio, Client, TeamMember, broadcasted_message

# Register your models here.
admin.site.register(Contact)
admin.site.register(Testimonial)
admin.site.register(Portfolio)
admin.site.register(Client)
admin.site.register(TeamMember)
admin.site.register(broadcasted_message)