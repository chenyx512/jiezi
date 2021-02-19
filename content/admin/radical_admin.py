from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from content.models import Radical
from content.admin import SpecificContentAdmin, MultiSelectFieldListFilter


@admin.register(Radical)
class RadicalAdmin(SpecificContentAdmin):
    search_fields = ['chinese', 'identifier']
    autocomplete_fields = ['audio']
    list_filter = [
        ('is_done', admin.BooleanFieldListFilter),
        ('character__word__word_set__name', MultiSelectFieldListFilter),
        ('is_learnable', admin.BooleanFieldListFilter),
        ('pinyin', admin.EmptyFieldListFilter),
        ('definition', admin.EmptyFieldListFilter),
    ]
    list_editable = ('is_learnable',)
    list_display = ['id', 'is_done', '__str__', 'pinyin', 'definition',
                    'is_learnable',
                    'get_image_thumbnail', 'get_character_list_display']
    readonly_fields = ('get_character_list_display', 'get_image_preview')

    def get_exclude(self, request, obj=None):
        """
        not show image when creating objects
        """
        exclude = super().get_exclude(request, obj=obj)
        if obj is None:
            exclude = exclude or []
            exclude.append('image')
        return exclude

    def get_character_list_display(self, radical):
        s = ""
        for c in radical.characters.all().distinct():
            s += f"<a href={reverse('admin:content_character_change', args=[c.pk])}>" \
                 f"{c}</a>, "
        return format_html(s[:-2])
    get_character_list_display.short_description = "Used In"

    def get_image_thumbnail(self, radical):
        return format_html('<img src="%s" width="30" height="30" />' % (radical.image.url))
    get_image_thumbnail.short_description = "image thumbnail"

    def get_image_preview(self, radical):
        return format_html('<img src="%s" width="150" height="150" />' % (radical.image.url))

    get_image_preview.short_description = "image preview"
