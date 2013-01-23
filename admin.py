from django.contrib import admin
from lp_parkrun.models import User, Event


class UserAdmin(admin.ModelAdmin):
    list_display = ('first_names', 'last_names', 'barcode')

class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'identifier', 'number','has_twitter_id', 'has_postcode', 'twitter')


admin.site.register(Event,EventAdmin)
admin.site.register(User,UserAdmin)

