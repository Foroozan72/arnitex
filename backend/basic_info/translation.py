from modeltranslation.translator import register, TranslationOptions
from countries_states_cities.models import Region

@register(Region)
class RegionTranslationOptions(TranslationOptions):
    fields = ('name',)
