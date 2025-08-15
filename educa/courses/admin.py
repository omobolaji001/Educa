from django.contrib import admin
from .models import Subject, Course, Module


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    """ Registers the Subject class to the admin site """
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}


class ModuleInline(admin.StackedInline):
    """ makes Module an inline
    so we can include it to Course Admin as an inline
    """
    model = Module


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """ Registers the Course model on the admin site """
    list_display = ['title', 'subject', 'created']
    list_filter = ['created', 'subject']
    search_fields = ['title', 'overview']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]
