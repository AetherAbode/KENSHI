from rest_framework import serializers
from .models import UserProfile, FileRecord, ChatMessage

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'auth_id', 'email', 'full_name', 'role', 'avatar_url', 'created_at']
        read_only_fields = ['id', 'auth_id', 'created_at']


class FileRecordSerializer(serializers.ModelSerializer):
    uploaded_by_email = serializers.EmailField(source='uploaded_by.email', read_only=True)
    uploaded_by_name = serializers.CharField(source='uploaded_by.full_name', read_only=True)

    class Meta:
        model = FileRecord
        fields = [
            'id', 'name', 'file_id', 'public_url', 'file_type',
            'file_size', 'mime_type', 'description',
            'uploaded_by', 'uploaded_by_email', 'uploaded_by_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'uploaded_by', 'created_at', 'updated_at']

    def create(self, validated_data):
        # Automatically set uploaded_by to the current user
        validated_data['uploaded_by'] = self.context['request'].user
        return super().create(validated_data)


class ChatMessageSerializer(serializers.ModelSerializer):
    sender_email = serializers.EmailField(source='sender.email', read_only=True)
    sender_name = serializers.CharField(source='sender.full_name', read_only=True)

    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'sender_email', 'sender_name', 'recipient', 'content', 'is_read', 'created_at']
        read_only_fields = ['id', 'sender', 'created_at']
