from django.contrib import admin
from chat.models import Message

# Register your models here.
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """ Include Message model to the admin site """
    list_display = ['sent_on', 'user', 'course', 'content']
    list_filter = ['sent_on', 'course']
    search_fields = ['content']
    # raw_id_fields = ['user', 'content']
