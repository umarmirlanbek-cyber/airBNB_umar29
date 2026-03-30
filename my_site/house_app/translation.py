from .models import Country, City, Property, Amenity
from modeltranslation.translator import TranslationOptions,register

@register(Property)
class PropertyTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

@register(Amenity)
class AmenityTranslationOptions(TranslationOptions):
    fields = ('name', )

@register(Country)
class CountryTranslationOptions(TranslationOptions):
    fields = ('country_name', )

@register(City)
class CityTranslationOptions(TranslationOptions):
    fields = ('city_name', )