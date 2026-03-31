from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/auth/", include("apps.accounts.urls")),
    path("api/v1/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/v1/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/v1/personas/", include("apps.personas.urls")),
    path("api/v1/chat/", include("apps.chat.urls")),
    path("api/v1/knowledge/", include("apps.knowledge.urls")),
    path("api/v1/voice/", include("apps.voice.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
