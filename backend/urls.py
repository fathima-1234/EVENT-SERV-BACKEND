from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
import os

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("base.urls")),
    path("api-servicer/", include("servicer.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("events/", include("events.urls")),
    path("user/", include("user.urls")),
    path("api/stripe/", include("payment.urls")),
    path("chat/", include("chatapp.urls")),
   
   

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
