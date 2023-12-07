# # chat/urls.py
# from django.urls import path
# from . import views

# urlpatterns = [
#     path('messages/', views.MessageView.as_view(), name='message-list'),
#     # Add more patterns as needed
# ]
# urls.py
from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path("getAdminId/", Adminfetch, name="adminnn"),
    path(
        "user-previous-chats/<int:user1>/<int:user2>/", PreviousMessagesView.as_view()
    ),
]