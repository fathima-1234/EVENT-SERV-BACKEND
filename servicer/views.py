from django.http import JsonResponse,HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from base.models import User
from rest_framework import generics 
from rest_framework import permissions
from .models import Servicer
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyServicerTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims for renters (sellers)
        token['username'] = user.username
        token['is_tutor'] = user.is_staff
        token['is_admin'] = user.is_superuser
        token['is_servicer'] = True  # Custom claim for renters (sellers)
        # ...

        return token

class MyServicerTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyServicerTokenObtainPairSerializer

class ServicerLoginView(TokenObtainPairView):
    serializer_class = MyServicerTokenObtainPairSerializer


class ServicerRegister(APIView):
    def post(self, request):
        full_name = request.data.get('full_name')
        email = request.data.get('email')
        password = request.data.get('password')
        mobile_no = request.data.get('mobile_no')

        if not full_name or not email or not password or not mobile_no:
            return Response({'message': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

        if Servicer.objects.filter(email=email).exists():
            return Response({'message': 'Email already exists'}, status=status.HTTP_409_CONFLICT)

        if Servicer.objects.filter(mobile_no=mobile_no).exists():
            return Response({'message': 'Phone number already exists'}, status=status.HTTP_409_CONFLICT)

        servicer = Servicer(full_name=full_name, email=email, password=password, mobile_no=mobile_no)
        servicer.save()

        servicer_id = servicer.id
        return Response({'message': 'Servicer registered successfully', 'servicer_id': servicer_id}, status=status.HTTP_201_CREATED)




    



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Servicer

class ServicerLogin(APIView):
    def post(self, request):
        email = request.data.get('email')
        if email is None:
            return Response({'bool': False, 'message': 'Email is missing'} )

        password = request.data.get('password')
        if password is None:
            return Response({'bool': False, 'message': 'Password is missing'})

        servicer = Servicer.objects.filter(email=email, password=password).first()
        if servicer:
            if servicer.is_active:
                return Response({'bool': True, 'servicer_id': servicer.id})
            else:
                return Response({'bool': False, 'message': 'Your account is not active. Please wait for approval.'})
        else:
            return Response({'bool': False, 'message': 'Invalid email or password'})


class BlockServicerView(APIView):
    def get(self, request, pk):
        user = Servicer.objects.get(id=pk)
        print(user.is_active)
        user.is_active = not user.is_active
        user.save()
        return Response({'msg': 200})
    

class UnblockServicerView(APIView):
    def put(self, request, Servicer_id):
        try:
            Servicer = Servicer.objects.get(servicer_id=Servicer_id)
            Servicer.is_active = True
            Servicer.save()
            return Response({'message': 'Servicer unblocked'})
        except Servicer.DoesNotExist:
            return Response({'message': 'Servicer not found'}, status=status.HTTP_404_NOT_FOUND)