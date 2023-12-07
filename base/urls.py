from django.urls import path
from . import views
from .views import (
    AuthView,
    UserRegistration,
    Listuser,
    GetProfile,
    BlockUserView,
    ServicerRegistration,
    Listservicer,
    BlockServicerView,
)

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
    TokenObtainPairView,
)


urlpatterns = [
    path("", views.getRoutes),
    path("auth/", AuthView.as_view(), name="auth"),
    path("api/token/", AuthView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/register/", UserRegistration.as_view()),
    path("api/servicerregister/", ServicerRegistration.as_view()),
    path("activate/<uidb64>/<token>", views.activate, name="activate"),
    path(
        "activateservicer/<uidb64>/<token>", views.activateservicer, name="activateservicer"
    ),
    path("users/", Listuser.as_view(), name="users"),
    path("blockuser/<int:pk>/", BlockUserView.as_view(), name="block-user"),
    path("servicers/", Listservicer.as_view(), name="servicers"),
    path("blockservicer/<int:pk>/", BlockServicerView.as_view(), name="block-user"),
    path("profile/<int:pk>", GetProfile.as_view(), name="profile"),
    path(
        "getSingleUser/<int:id>/", views.GetSingleUser.as_view(), name="getDoctorInHome"
    ),
]