from django.contrib import admin
from .models import UserProfile, FileRecord, ChatMessage

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('auth_id', 'email', 'full_name', 'role', 'created_at')
    search_fields = ('email', 'full_name')

@admin.register(FileRecord)
class FileRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'uploaded_by', 'file_size', 'file_type', 'created_at')
    list_filter = ('file_type', 'uploaded_by')

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'content_preview', 'created_at')
    list_filter = ('sender',)

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Message Preview'
