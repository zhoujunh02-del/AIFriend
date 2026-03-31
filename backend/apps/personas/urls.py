from django.urls import path
from .views import PersonaListCreateView, PersonaDetailView

urlpatterns = [
    path("", PersonaListCreateView.as_view(), name="persona-list"),
    path("<uuid:pk>/", PersonaDetailView.as_view(), name="persona-detail"),
]
