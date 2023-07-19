from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .yasg import urlpatterns as swagger_urlpatterns
# Main apps
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("core.urls"), name='core'),
    path("__debug__/", include("debug_toolbar.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# 3th party apps
urlpatterns += [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-auth/', include('rest_framework.urls')),
]

urlpatterns += swagger_urlpatterns
