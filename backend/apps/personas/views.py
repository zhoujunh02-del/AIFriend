from rest_framework import generics, permissions
from django.db import models
from .models import Persona
from .serializers import PersonaSerializer

class IsCreatorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.creator == request.user

class PersonaListCreateView(generics.ListCreateAPIView):
    serializer_class = PersonaSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Persona.objects.filter(is_active=True).filter(
                models.Q(is_public=True) | models.Q(creator=user)
            )
        return Persona.objects.filter(is_active=True, is_public=True)


class PersonaDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PersonaSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsCreatorOrReadOnly)

    def get_queryset(self):
        return Persona.objects.filter(is_active=True)
