import jwt
import requests
from django.conf import settings
from rest_framework import authentication, exceptions
from .models import UserProfile

class SupabaseJWTAuthentication(authentication.BaseAuthentication):
    """
    Authenticate using a JWT token from Supabase.
    The token is expected in the Authorization header: Bearer <token>
    """
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        try:
            # Extract token
            parts = auth_header.split()
            if len(parts) != 2 or parts[0].lower() != 'bearer':
                raise exceptions.AuthenticationFailed('Invalid authorization header format. Use: Bearer <token>')
            token = parts[1]

            # Decode JWT using Supabase JWT secret
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

            # Extract user info from decoded token
            user_id = decoded.get('sub')
            email = decoded.get('email')

            if not user_id or not email:
                raise exceptions.AuthenticationFailed('Token missing required user data')

            # Get or create UserProfile from the auth_id
            user_profile, created = UserProfile.objects.get_or_create(
                auth_id=user_id,
                defaults={
                    'email': email,
                    'full_name': decoded.get('user_metadata', {}).get('full_name', email.split('@')[0]),
                    'role': decoded.get('user_metadata', {}).get('role', 'student'),
                }
            )

            # Update email if it changed (edge case)
            if not created and user_profile.email != email:
                user_profile.email = email
                user_profile.save(update_fields=['email'])

            # Attach the decoded token and profile to the request for later use
            return (user_profile, decoded)

        except Exception as e:
            raise exceptions.AuthenticationFailed(f'Authentication failed: {str(e)}')
