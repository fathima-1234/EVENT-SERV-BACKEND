# # chat/views.py
# from rest_framework import generics
# from .models import Message
# from .serializers import MessageSerializer

# # chat/views.py
# from rest_framework import generics
# from .models import Message
# from .serializers import MessageSerializer

# class MessageView(generics.CreateAPIView):
#     queryset = Message.objects.all()
#     serializer_class = MessageSerializer

    # def perform_create(self, serializer):
    #     # Check if the user is authenticated
    #     if self.request.user.is_authenticated:
    #         # If authenticated, associate the message with the authenticated user
    #         serializer.save(sender=self.request.user)
    #     else:
    #         # If not authenticated, you can set sender to None or a default user ID
    #         # serializer.save(sender=None)  # Or specify a default user ID
    #         pass  # Adjust this part based on your requirements
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from base.models import *
from base.serializers import *
from rest_framework.views import APIView
from .serializers import *
from .models import *
from rest_framework.generics import *


@api_view(["GET"])
def Adminfetch(request):
    try:
        admin = User.objects.get(is_superuser=True)
        adminId = admin.id
        return Response({"admin_id": adminId}, status=status.HTTP_200_OK)
    except Employee.DoesNotExist:
        return Response(
            {"message": "Admin not found"}, status=status.HTTP_404_NOT_FOUND
        )


class PreviousMessagesView(ListAPIView):
    serializer_class = ChatSerializer

    def get_queryset(self):
        user1 = int(self.kwargs["user1"])
        user2 = int(self.kwargs["user2"])

        thread_suffix = f"{user1}_{user2}" if user1 > user2 else f"{user2}_{user1}"
        thread_name = "chat_" + thread_suffix
        queryset = Chat.objects.filter(thread_name=thread_name)
        return queryset