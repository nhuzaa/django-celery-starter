from django.middleware.csrf import get_token
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import CustomUser
from .permissions import IsAdminUser

# @api_view(['GET'])
# @permission_classes([AllowAny])
# def get_csrf_token(request):
#     token = get_token(request)
#     return JsonResponse({'csrfToken': token}) 

class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing users. Only accessible by admin users.
    """
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    
    def get_serializer_class(self):
        if self.action == 'create':
            from .serializers import UserCreateSerializer
            return UserCreateSerializer
        return UserSerializer
    
    def list(self, request, *args, **kwargs):
        """
        List all users. Only accessible by admin users.
        """
        users = self.get_queryset()
        data = [{
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.get_role_display(),
            'is_active': user.is_active,
            'date_joined': user.date_joined
        } for user in users]
        return Response(data)
    
    def create(self, request, *args, **kwargs):
        """
        Create a new user. Only accessible by admin users.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.get_role_display(),
            'is_active': user.is_active
        }, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        """
        Update a user. Only accessible by admin users.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.get_role_display(),
            'is_active': user.is_active
        })
    
    def destroy(self, request, *args, **kwargs):
        """
        Delete a user. Only accessible by admin users.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT) 