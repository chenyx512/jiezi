import json

from django.utils.html import format_html
from django.contrib import admin

from .models import Record


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'time', 'action', 'reviewable',
                    'get_question', 'get_set_name', 'get_answer')
    list_filter = (
        'action',
        ('user__student__klass', admin.RelatedOnlyFieldListFilter),
        ('learning_process__wordset', admin.RelatedOnlyFieldListFilter),
    )
    search_fields = ('user__username__exact',)
    exclude = ('data', 'question')
    readonly_fields = ('get_data', 'get_question')

    def get_question(self, record):
        if record.question:
            return format_html(
                "<a href={}>{}</a>",
                record.question.get_admin_url(),
                record.question.question_form)
        else:
            return None

    def get_answer(self, record):
        return record.data.get('answer', None)

    def get_data(self, record):
        data = json.dumps(record.data, ensure_ascii=False, indent=4)
        return data

    def get_set_name(self, record):
        try:
            return record.learning_process.wordset.name
        except AttributeError:
            return '--'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
