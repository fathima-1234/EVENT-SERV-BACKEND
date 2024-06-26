from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from .serializers import UserSerializer
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from base.models import User
from django.http import HttpResponseRedirect
from rest_framework.generics import ListCreateAPIView
from django.shortcuts import reverse
from rest_framework import generics
from django.db.models import Q
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.permissions import IsAdminUser


@api_view(["GET"])
def getRoutes(request):
    routes = [
        "/api/token",
        "/api/token/refresh",
    ]

    return Response(routes)


class AuthView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = response.data["access"]
        response.data["token"] = token
        response.data.pop("access", None)
        response.data.pop("refresh", None)
        email = request.data.get("email")
        user = User.objects.get(email=email)

        response.data["user"] = {
            "email": str(user.email),
            "is_servicer": bool(user.is_servicer),
            "userID": int(user.id),
            "is_active": bool(user.is_active),
            "is_admin": bool(user.is_superadmin),
            "is_staff": bool(user.is_staff),
            "name": str(user.first_name + " " + user.last_name),
        }
        return response
class IsServicerOrAdmin(BasePermission):    
    """
    Custom permission to allow access only to servicers or administrators.   
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_servicer or request.user.is_staff)


class UserRegistration(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            is_superadmin = serializer.validated_data.get('is_superadmin', False)

            # Check if the request is attempting to create a superadmin
            if is_superadmin and not request.user.is_superuser:
                return Response({"msg": "You are not authorized to create a superadmin account."}, 
                                status=status.HTTP_403_FORBIDDEN)

            # Save the user but do not activate it immediately
            user = serializer.save()

            # Generate activation token and URL
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activation_url = reverse("activate", kwargs={"uidb64": uid, "token": token})
            activation_url = request.build_absolute_uri(activation_url)

            # Send email verification
            current_site = get_current_site(request)
            mail_subject = "Please activate your account"
            message = render_to_string(
                "verification_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "activation_url": activation_url,
                },
            )
            to_email = user.email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            return Response({"msg": "Registration Success. Activation email sent to your registered email."})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        print("checked")
        user.is_active = True
        user.save()
        #     return HttpResponse("Success: User is verified")
        # else:
        #     return HttpResponse("token expaired")
        return HttpResponseRedirect(
            "https://event-serv-frondend.vercel.app/login?activation=success&message=Account%20activated.%20You%20can%20now%20log%20in"
        )
    else:
        # Redirect with error message
        return HttpResponseRedirect(
            "https://event-serv-frondend.vercel.app/login?activation=error&message=Activation%20failed.%20Please%20try%20again"
        )


class ServicerRegistration(APIView):
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Generate the activation URL
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activation_url = reverse(
                "activateservicer", kwargs={"uidb64": uid, "token": token}
            )
            activation_url = request.build_absolute_uri(activation_url)

            # Send email verification
            current_site = get_current_site(request)
            mail_subject = "Please activate your account"
            message = render_to_string(
                "verification_email_servicer.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "activation_url": activation_url,
                },
            )
            to_email = user.email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            return Response({"msg": "Registration Success"})

        return Response({"msg": "Registration Failed"})


@api_view(["GET"])
def activateservicer(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        print("Servicer checked")

        user.is_staff = True
        user.save()

        # return HttpResponseRedirect("http://localhost:3000/servicersignin/")
        return HttpResponse(
            "Success: Servicer is verified,Thank you for signup, You can login after the approal of the admin "
        )
    else:
        return HttpResponse("token expaired")


class Listuser(generics.ListCreateAPIView):
    queryset = User.objects.filter(Q(is_admin=False) & Q(is_staff=False))

    serializer_class = UserSerializer
    permission_classes = [IsServicerOrAdmin]

class Listservicer(generics.ListCreateAPIView):
    queryset = User.objects.filter(Q(is_admin=False) & Q(is_staff=True))
    serializer_class = UserSerializer


class BlockUserView(APIView):
    permission_classes = [IsServicerOrAdmin]
    def get(self, request, pk):
        user = User.objects.get(id=pk)
        print(user.is_active)
        user.is_active = not user.is_active
        user.save()
        return Response({"msg": 200})


class Singleuser(APIView):
    def get(self, request, pk):
        query = User.objects.get(id=pk)
        serializer = CarSerializer(query)
        return Response(serializer.data)


class GetProfile(APIView):
    def get(self, request, pk):
        user = User.objects.filter(id=pk)
        print(user)

        serializer = UserSerializer(user, many=True)

        return Response(serializer.data)


class BlockServicerView(APIView):
    def get(self, request, pk):
        user = User.objects.get(id=pk)
        print(user.is_active)
        user.is_active = not user.is_active
        user.is_servicer = not user.is_servicer
        user.save()
        return Response({"msg": 200})
