from django.contrib import admin
from.models import Recipe
from django_summernote.admin import SummernoteModelAdmin

@admin.register(Recipe)
class RecipeAdmin(SummernoteModelAdmin):


    list_display = ('title', 'cuisine', 'created_on')
    search_fields = ['cuisine', 'title', 'author']
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('cuisine', 'created_on',)
    summernote_fields = ('content')


