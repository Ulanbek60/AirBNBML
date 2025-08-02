from django.contrib import admin
from .models import UserProfile, Property, Image, Booking, Review
from modeltranslation.admin import TranslationAdmin

admin.site.register(UserProfile)
admin.site.register(Booking)
admin.site.register(Review)

class PropertyImageInline(admin.TabularInline):
    model = Image
    extra = 1

@admin.register(Property)
class PropertyAdmin(TranslationAdmin):
    inlines = [PropertyImageInline]
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }
