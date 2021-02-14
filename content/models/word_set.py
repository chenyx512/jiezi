from django.db import models
from django.core.exceptions import ValidationError
from django.shortcuts import reverse

from content.models import GeneralContentModel, OrderableMixin


class WordInSet(OrderableMixin):
    word = models.ForeignKey('Word', on_delete=models.CASCADE)
    word_set = models.ForeignKey('WordSet', on_delete=models.CASCADE)

    class Meta:
        ordering = ['order']
        unique_together = ['word', 'word_set', 'order']


class WordSet(GeneralContentModel):
    name = models.CharField(max_length=30, unique=True)
    words = models.ManyToManyField('Word', through='WordInSet',
                                   related_name='word_sets',
                                   related_query_name='word_set')

    class Meta:
        ordering = ['id']

    def clean(self):
        super().clean()
        if self.is_done:
            if not self.words.exists():
                raise ValidationError('cannot be done without any word')
            for w in self.words.all():
                if not w.is_done:
                    raise ValidationError(f"{w} not done")

    def render_all_words(self):
        return ', '.join(w.chinese for w in self.words.all())

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def reset_order(self):
        OrderableMixin.reset_order(self.wordinset_set)

    def get_absolute_url(self):
        return reverse('set_display', args=(self.pk,))

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        id = self.id or -1
        return f'<WS{id}:{self.name}>'
