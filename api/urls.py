from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'profiles', views.UserProfileViewSet, basename='profile')
router.register(r'files', views.FileRecordViewSet, basename='file')
router.register(r'messages', views.ChatMessageViewSet, basename='message')

urlpatterns = [
    # Public endpoints
    path('health/', views.health_check, name='health-check'),

    # Authentication & User Sync
    path('sync-user/', views.sync_user, name='sync-user'),

    # File upload generation
    path('generate-upload-url/', views.generate_upload_url, name='generate-upload-url'),

    # Code execution (placeholder)
    path('execute/', views.execute_code, name='execute-code'),

    # DRF Router endpoints
    path('', include(router.urls)),
]
