from django.core.management.base import BaseCommand
from learning.models import Radical, Character
import jiezi.settings as settings
import os
import PIL.Image

class Command(BaseCommand):
    help = 'update media'

    def handle(self, *args, **kwargs):
        for radical in Radical.objects.all():
            name = 'radical_mnemonic/R%04d.png'%radical.pk
            path = os.path.join(settings.MEDIA_ROOT, name)
            if os.path.isfile(path) :
                img = PIL.Image.open(path)
                img = img.resize((600, 600), PIL.Image.ANTIALIAS)
                img.save(os.path.join(settings.MEDIA_ROOT, name), optimize=True, quality=80)
                radical.mnemonic_image.name=name
                radical.save()
            else:
                print(f'not found {radical}s radical_mnemonic png')
        print('finish radicals')
        for character in Character.objects.all():
            name = 'animated_stroke_order/C%04d.gif' % character.pk
            path = os.path.join(settings.MEDIA_ROOT, name)
            if os.path.isfile(path):
                character.stroke_order_image.name = name
                character.save()
            else:
                print(f'not found {character}‘s animated_stroke_order gif')
        print('characters 50%')
        for character in Character.objects.all():
            name = 'color_coded_characters/C%04d.png' % character.pk
            path = os.path.join(settings.MEDIA_ROOT, name)
            if os.path.isfile(path):
                character.color_coded_image = name
                character.save()
            else:
                print(f'not found {character}‘s color_coded_characters png')
        print('media updated')