from django.contrib import admin
from .models import UserProfile, Amenity, Review, Booking,Property, PropertyImage,Rules,City,Country
from modeltranslation.admin import TranslationAdmin


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0


@admin.register(Property)
class PropertyAdmin(TranslationAdmin):
    inlines = [PropertyImageInline, ReviewInline]

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

admin.site.register(Booking)
admin.site.register(UserProfile)
admin.site.register(Amenity)
admin.site.register(Review)
admin.site.register(Rules)
admin.site.register(City)
admin.site.register(Country)