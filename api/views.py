from django.db import models 
import logging
from rest_framework import viewsets, status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from supabase import create_client

from .models import UserProfile, FileRecord, ChatMessage
from .serializers import UserProfileSerializer, FileRecordSerializer, ChatMessageSerializer
from django.conf import settings

logger = logging.getLogger(__name__)

# ============================================================
#  Supabase Client (for storage operations)
# ============================================================
supabase_client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)

# ============================================================
#  HEALTH CHECK (Public)
# ============================================================
@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    return Response({
        "status": "ok",
        "message": "Classroom Backend is running!",
        "supabase_connected": bool(settings.SUPABASE_URL)
    })

# ============================================================
#  SYNC USER (Called from frontend after Supabase login)
# ============================================================
@api_view(['POST'])
@permission_classes([AllowAny])  # The request itself carries the JWT, we verify manually or rely on auth if needed.
def sync_user(request):
    """
    Syncs user data from Supabase Auth to Django DB.
    Expects: { "auth_id": "uuid", "email": "user@mail.com", "full_name": "Name", "role": "student" }
    """
    auth_id = request.data.get('auth_id')
    email = request.data.get('email')
    full_name = request.data.get('full_name', email.split('@')[0] if email else 'User')
    role = request.data.get('role', 'student')

    if not auth_id or not email:
        return Response({"error": "auth_id and email are required"}, status=status.HTTP_400_BAD_REQUEST)

    profile, created = UserProfile.objects.update_or_create(
        auth_id=auth_id,
        defaults={
            'email': email,
            'full_name': full_name,
            'role': role,
        }
    )

    serializer = UserProfileSerializer(profile)
    return Response({
        "message": "User synced successfully",
        "created": created,
        "user": serializer.data
    }, status=status.HTTP_200_OK)

# ============================================================
#  USER PROFILE VIEWSET (Read-only for students, full for teachers)
# ============================================================
class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """View and list user profiles."""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Teachers can see all, students can only see themselves
        user = self.request.user
        if user.role == 'teacher':
            return UserProfile.objects.all()
        return UserProfile.objects.filter(id=user.id)

    def retrieve(self, request, *args, **kwargs):
        # Allow users to fetch their own profile with 'me' as the pk
        if kwargs.get('pk') == 'me':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        return super().retrieve(request, *args, **kwargs)

# ============================================================
#  FILE RECORD VIEWSET (Full CRUD)
# ============================================================
class FileRecordViewSet(viewsets.ModelViewSet):
    serializer_class = FileRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Teachers see all files, students see only their own files
        user = self.request.user
        if user.role == 'teacher':
            return FileRecord.objects.all().order_by('-created_at')
        return FileRecord.objects.filter(uploaded_by=user).order_by('-created_at')

    def perform_create(self, serializer):
        # The uploaded_by is set via the serializer's context
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Optional: Delete file from Supabase Storage as well
        # supabase_client.storage.from_('assignments').remove([instance.file_id])
        self.perform_destroy(instance)
        return Response({"message": "File record deleted"}, status=status.HTTP_204_NO_CONTENT)

# ============================================================
#  GENERATE UPLOAD URL (Using Supabase Storage)
# ============================================================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_upload_url(request):
    """
    Generates a public URL path for uploading a file to Supabase Storage.
    Expected: { "file_name": "homework.pdf", "folder": "submissions" }
    Returns: { "upload_path": "submissions/uuid-homework.pdf", "public_url": "https://..." }
    """
    file_name = request.data.get('file_name')
    folder = request.data.get('folder', 'uploads')

    if not file_name:
        return Response({"error": "file_name is required"}, status=status.HTTP_400_BAD_REQUEST)

    # Generate a unique file ID to avoid collisions
    import uuid
    unique_id = uuid.uuid4().hex[:8]
    base, ext = file_name.rsplit('.', 1) if '.' in file_name else (file_name, '')
    sanitized_name = f"{base}_{unique_id}.{ext}" if ext else f"{base}_{unique_id}"
    full_path = f"{folder}/{request.user.auth_id}/{sanitized_name}"

    # Check if bucket exists (we assume 'assignments' bucket is public)
    bucket_name = 'assignments'
    public_url = f"{settings.SUPABASE_URL}/storage/v1/object/public/{bucket_name}/{full_path}"

    return Response({
        "upload_path": full_path,
        "public_url": public_url,
        "bucket": bucket_name,
        "message": "Upload this file directly to Supabase Storage using the public URL.",
        "upload_hint": f"Use Supabase JS client: supabase.storage.from('{bucket_name}').upload('{full_path}', file)"
    }, status=status.HTTP_200_OK)

# ============================================================
#  CHAT MESSAGES (Backup Logging)
# ============================================================
class ChatMessageViewSet(viewsets.ModelViewSet):
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Users can only see messages they sent or received
        user = self.request.user
        return ChatMessage.objects.filter(
            models.Q(sender=user) | models.Q(recipient=user)
        ).order_by('created_at')

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

# ============================================================
#  MOCK CODE EXECUTION (Pyodide handles this on frontend, but we keep a placeholder)
# ============================================================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def execute_code(request):
    """
    Placeholder endpoint – the actual execution is done via Pyodide in the browser.
    This could be used later for sandboxed execution if needed.
    """
    return Response({
        "message": "Code execution is handled client-side via Pyodide (WebAssembly).",
        "hint": "Use the /api/execute endpoint in the future for server-side execution."
    }, status=status.HTTP_200_OK)
