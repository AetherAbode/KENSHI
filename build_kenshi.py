import os

# ============================================================
#  THIS SCRIPT CREATES THE ENTIRE DJANGO BACKEND
#  Run it once and your code is ready!
# ============================================================

BASE_DIR = "myclassroom-backend"

files = {
    # Root files
    f"{BASE_DIR}/.gitignore": """# Python
venv/
env/
.venv/
.env
*.pyc
__pycache__/
*.pyo
*.pyd
.Python
pip-log.txt
pip-delete-this-directory.txt
.pytest_cache/
.coverage
htmlcov/
.tox/
.mypy_cache/
.dmypy.json
dmypy.json
*.log

# Database
db.sqlite3
*.db

# Django
*.pot
*.pyc
local_settings.py
static/
staticfiles/
media/
mediafiles/

# IDE
.vscode/
.idea/
*.swp
*.swo
.DS_Store
""",

    f"{BASE_DIR}/.env.example": """DJANGO_SECRET_KEY=your-super-secret-key-change-this-in-production
DEBUG=True

# Supabase (get these from your Supabase Dashboard → Settings → API)
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_ANON_KEY=your-anon-public-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
SUPABASE_JWT_SECRET=your-jwt-secret

# Supabase PostgreSQL Connection String
SUPABASE_DB_URL=postgresql://postgres.xxxx:password@aws-0-region.pooler.supabase.com:6543/postgres

# Frontend URL (your Vercel app)
FRONTEND_URL=http://localhost:3000
""",

    f"{BASE_DIR}/requirements.txt": """Django>=4.2,<5.0
djangorestframework>=3.14.0
django-cors-headers>=4.0.0
psycopg2-binary>=2.9.0
python-dotenv>=1.0.0
gunicorn>=21.0.0
whitenoise>=6.5.0
supabase>=2.0.0
PyJWT>=2.8.0
""",

    f"{BASE_DIR}/runtime.txt": """python-3.11.0
""",

    f"{BASE_DIR}/Procfile": """web: gunicorn myclassroom.wsgi:application
""",

    f"{BASE_DIR}/manage.py": """#!/usr/bin/env python
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myclassroom.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
""",

    # myclassroom folder
    f"{BASE_DIR}/myclassroom/__init__.py": "",
    f"{BASE_DIR}/myclassroom/asgi.py": "",
    f"{BASE_DIR}/myclassroom/wsgi.py": """import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myclassroom.settings')
application = get_wsgi_application()
""",

    f"{BASE_DIR}/myclassroom/urls.py": """from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]
""",

    f"{BASE_DIR}/myclassroom/settings.py": """import os
import dj_database_url
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("DJANGO_SECRET_KEY environment variable is not set!")

DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.onrender.com',
    '.vercel.app',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'api',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:3000')
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://localhost:5173',
    FRONTEND_URL,
]
CORS_ALLOW_CREDENTIALS = True

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('SUPABASE_DB_URL'),
        conn_max_age=600,
        ssl_require=True
    )
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'api.authentication.SupabaseJWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_SERVICE_ROLE_KEY = os.environ.get('SUPABASE_SERVICE_ROLE_KEY')
SUPABASE_ANON_KEY = os.environ.get('SUPABASE_ANON_KEY')
SUPABASE_JWT_SECRET = os.environ.get('SUPABASE_JWT_SECRET')

if not all([SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, SUPABASE_JWT_SECRET]):
    raise ValueError("Missing required Supabase environment variables!")

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}
""",

    # api folder
    f"{BASE_DIR}/api/__init__.py": "",
    f"{BASE_DIR}/api/apps.py": """from django.apps import AppConfig

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
""",

    f"{BASE_DIR}/api/admin.py": """from django.contrib import admin
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
""",

    f"{BASE_DIR}/api/models.py": """from django.db import models

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    ]

    auth_id = models.UUIDField(unique=True, db_index=True)
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
    FILE_TYPES = [
        ('assignment', 'Assignment'),
        ('submission', 'Submission'),
        ('resource', 'Resource'),
    ]

    name = models.CharField(max_length=255)
    file_id = models.CharField(max_length=255, unique=True)
    public_url = models.URLField()
    file_type = models.CharField(max_length=20, choices=FILE_TYPES, default='resource')
    file_size = models.PositiveIntegerField()
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
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='received_messages', null=True, blank=True)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.email} -> {self.content[:30]}"

    class Meta:
        ordering = ['created_at']
""",

    f"{BASE_DIR}/api/authentication.py": """import jwt
from django.conf import settings
from rest_framework import authentication, exceptions
from .models import UserProfile

class SupabaseJWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        try:
            parts = auth_header.split()
            if len(parts) != 2 or parts[0].lower() != 'bearer':
                raise exceptions.AuthenticationFailed('Invalid authorization header format. Use: Bearer <token>')
            token = parts[1]

            try:
                decoded = jwt.decode(
                    token,
                    settings.SUPABASE_JWT_SECRET,
                    algorithms=['HS256'],
                    audience='authenticated'
                )
            except jwt.ExpiredSignatureError:
                raise exceptions.AuthenticationFailed('Token has expired')
            except jwt.InvalidTokenError as e:
                raise exceptions.AuthenticationFailed(f'Invalid token: {str(e)}')

            user_id = decoded.get('sub')
            email = decoded.get('email')

            if not user_id or not email:
                raise exceptions.AuthenticationFailed('Token missing required user data')

            user_profile, created = UserProfile.objects.get_or_create(
                auth_id=user_id,
                defaults={
                    'email': email,
                    'full_name': decoded.get('user_metadata', {}).get('full_name', email.split('@')[0]),
                    'role': decoded.get('user_metadata', {}).get('role', 'student'),
                }
            )

            if not created and user_profile.email != email:
                user_profile.email = email
                user_profile.save(update_fields=['email'])

            return (user_profile, decoded)

        except Exception as e:
            raise exceptions.AuthenticationFailed(f'Authentication failed: {str(e)}')
""",

    f"{BASE_DIR}/api/serializers.py": """from rest_framework import serializers
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
        validated_data['uploaded_by'] = self.context['request'].user
        return super().create(validated_data)


class ChatMessageSerializer(serializers.ModelSerializer):
    sender_email = serializers.EmailField(source='sender.email', read_only=True)
    sender_name = serializers.CharField(source='sender.full_name', read_only=True)

    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'sender_email', 'sender_name', 'recipient', 'content', 'is_read', 'created_at']
        read_only_fields = ['id', 'sender', 'created_at']
""",

    f"{BASE_DIR}/api/views.py": """import logging
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.db import models
from supabase import create_client

from .models import UserProfile, FileRecord, ChatMessage
from .serializers import UserProfileSerializer, FileRecordSerializer, ChatMessageSerializer
from django.conf import settings

logger = logging.getLogger(__name__)

supabase_client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    return Response({
        "status": "ok",
        "message": "KENSHI Classroom Backend is running!",
        "supabase_connected": bool(settings.SUPABASE_URL)
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def sync_user(request):
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


class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'teacher':
            return UserProfile.objects.all()
        return UserProfile.objects.filter(id=user.id)

    def retrieve(self, request, *args, **kwargs):
        if kwargs.get('pk') == 'me':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        return super().retrieve(request, *args, **kwargs)


class FileRecordViewSet(viewsets.ModelViewSet):
    serializer_class = FileRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'teacher':
            return FileRecord.objects.all().order_by('-created_at')
        return FileRecord.objects.filter(uploaded_by=user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_upload_url(request):
    file_name = request.data.get('file_name')
    folder = request.data.get('folder', 'uploads')

    if not file_name:
        return Response({"error": "file_name is required"}, status=status.HTTP_400_BAD_REQUEST)

    import uuid
    unique_id = uuid.uuid4().hex[:8]
    base, ext = file_name.rsplit('.', 1) if '.' in file_name else (file_name, '')
    sanitized_name = f"{base}_{unique_id}.{ext}" if ext else f"{base}_{unique_id}"
    full_path = f"{folder}/{request.user.auth_id}/{sanitized_name}"

    bucket_name = 'assignments'
    public_url = f"{settings.SUPABASE_URL}/storage/v1/object/public/{bucket_name}/{full_path}"

    return Response({
        "upload_path": full_path,
        "public_url": public_url,
        "bucket": bucket_name,
        "message": "Upload this file directly to Supabase Storage using the public URL."
    }, status=status.HTTP_200_OK)


class ChatMessageViewSet(viewsets.ModelViewSet):
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ChatMessage.objects.filter(
            models.Q(sender=user) | models.Q(recipient=user)
        ).order_by('created_at')

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def execute_code(request):
    return Response({
        "message": "Code execution is handled client-side via Pyodide (WebAssembly)."
    }, status=status.HTTP_200_OK)
""",

    f"{BASE_DIR}/api/urls.py": """from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'profiles', views.UserProfileViewSet, basename='profile')
router.register(r'files', views.FileRecordViewSet, basename='file')
router.register(r'messages', views.ChatMessageViewSet, basename='message')

urlpatterns = [
    path('health/', views.health_check, name='health-check'),
    path('sync-user/', views.sync_user, name='sync-user'),
    path('generate-upload-url/', views.generate_upload_url, name='generate-upload-url'),
    path('execute/', views.execute_code, name='execute-code'),
    path('', include(router.urls)),
]
""",
}

# Create all files and folders
for filepath, content in files.items():
    # Create directories if they don't exist
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"✅ Created: {filepath}")

print("\n" + "="*50)
print("🎉 SUCCESS! Your Django backend code is ready!")
print("📁 Folder created: myclassroom-backend/")
print("="*50)
