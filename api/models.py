from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """Links a Supabase auth user to a Django profile."""
    ROLE_CHOICES = [
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    ]

    auth_id = models.UUIDField(unique=True, db_index=True, help_text="Supabase auth.users id")
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    avatar_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.email} ({self.role})"

    class Meta:
        ordering = ['-created_at']


class FileRecord(models.Model):
    """Tracks files uploaded to Supabase Storage."""
    FILE_TYPES = [
        ('assignment', 'Assignment'),
        ('submission', 'Submission'),
        ('resource', 'Resource'),
    ]

    name = models.CharField(max_length=255)
    file_id = models.CharField(max_length=255, unique=True, help_text="Unique identifier from Supabase Storage")
    public_url = models.URLField(help_text="Public or signed URL to access the file")
    file_type = models.CharField(max_length=20, choices=FILE_TYPES, default='resource')
    file_size = models.PositiveIntegerField(help_text="File size in bytes")
    mime_type = models.CharField(max_length=100, blank=True, null=True)

    uploaded_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='files')
    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.uploaded_by.email})"

    class Meta:
        ordering = ['-created_at']


class ChatMessage(models.Model):
    """Backup logging of chat messages (frontend uses Supabase Realtime)."""
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='received_messages', null=True, blank=True)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.email} -> {self.content[:30]}"

    class Meta:
        ordering = ['created_at']
