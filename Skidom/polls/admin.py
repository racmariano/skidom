# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Choice, Question

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 5

# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [ (None, {'fields': ['question_text']}),
                  ('Date information', {'fields': ['pub_date']}),]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'recently_published')
    list_filter = ['pub_date']
    search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)
