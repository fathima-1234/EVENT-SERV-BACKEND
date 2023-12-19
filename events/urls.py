from django.urls import path
from base.views import Singleuser
from .views import (
    EventCategoryListCreateView,
    SingleEventDetailView,
    EventListCreateView,
    HomeListEvent,
    HomeListLocation,
    EventDeleteView,
    EventUpdateView,
    CreateEvent,
    CreateEventMenu,
    CreateEventCategory,
    CategoryDeleteView,
    CategoryUpdateView,
    MenuListCreateView,
    CreateEventMenu,
    MenuDeleteView,
    MenuUpdateView,
    ApproveEvent,
    BlockEvent,
    MyEvents,
    CategoryView,
    EventListView,
    LocationListView,
    EventDetailView,
    CategoryView,
    AddCategoryView,
    CategoryListCreateView,
    CategoryUpdateDeleteView,
    EventSlotsListView,
    SingleEventSlotDetailView,
)
from . import views

urlpatterns = [
    path(
        "event-category/", EventCategoryListCreateView.as_view(), name="event-category"
    ),
    path("event/", EventListCreateView.as_view(), name="event-list-create"),
    path("home-list-event/", HomeListEvent.as_view(), name="home-list-event"),
    path(
        "home-list-locations/", HomeListLocation.as_view(), name="home-list-locations"
    ),
    path(
        "delete-event/<int:event_id>/", EventDeleteView.as_view(), name="event-delete"
    ),
    path(
        "update-event/<int:event_id>/", EventUpdateView.as_view(), name="event-update"
    ),
    path("create-event/", CreateEvent.as_view(), name="event-create"),
    path(
        "create-event-category/",
        CreateEventCategory.as_view(),
        name="event-category-create",
    ),
    path("create-event-menu/", CreateEventMenu.as_view(), name="event-menu-create"),
    path(
        "delete-event-category/<int:cat_id>/",
        CategoryDeleteView.as_view(),
        name="event-category-delete",
    ),
    path(
        "update-event-category/<int:cat_id>/",
        CategoryUpdateView.as_view(),
        name="event-category-update",
    ),
    path("approve-event/<int:event_id>/", ApproveEvent.as_view(), name="event-approve"),
    # path("reject-event/<int:event_id>/", RejectEvent.as_view(), name="event-reject"),
    path("block-event/<int:event_id>/", BlockEvent.as_view(), name="event-block"),
    path("my-events/<int:user_id>/", MyEvents.as_view(), name="my-events"),
    path(
        "get-events-by-servicer/",
        views.get_events_by_servicer,
        name="get-events-by-servicer",
    ),
    path(
        "single-event/<int:id>/",
        SingleEventDetailView.as_view(),
        name="single_event_detail",
    ),
    path("singleuser/<int:pk>", Singleuser.as_view(), name="singleuser"),
    path("categories/", CategoryView.as_view(), name="categories"),
    path("user-events/", EventListView.as_view(), name="events"),
    path("user-locations/", LocationListView.as_view(), name="locations"),
    path("user-events/<int:id>/", EventDetailView.as_view(), name="event-detail"),
    path("categories/", CategoryView.as_view(), name="categories"),
    path("add-category/", AddCategoryView.as_view(), name="add-category"),
    path("categories1/", CategoryListCreateView.as_view(), name="category-list-create"),
    path(
        "categories/<int:category_id>/",
        CategoryUpdateDeleteView.as_view(),
        name="category-update-delete",
    ),
    path("test/", views.test, name="test"),
    path("sendmail/", views.send_mail_to_all, name="sendmail"),
    path("schedulemail/", views.schedule_mail, name="schedulemail"),
    path("menu/", MenuListCreateView.as_view(), name="menu-list-create"),
    path("create-event-menu/", CreateEventMenu.as_view(), name="event-menu-create"),
    path(
        "delete-event-menu/<int:menu_id>/",
        MenuDeleteView.as_view(),
        name="event-menu-delete",
    ),
    path(
        "update-event-menu/<int:menu_id>/",
        MenuUpdateView.as_view(),
        name="event-menu-update",
    ),
    path("createslots/", views.SlotCreateAPIView.as_view(), name="createslots"),
    path(
        "getslots/<int:event_id>/",
        views.GetEventSlots.as_view(),
        name="getEventSlotsInHome",
    ),
    path(
        "single-slot/<int:event_id>/",
        SingleEventSlotDetailView.as_view(),
        name="single_event_detail",
    ),
    path("slots/<int:id>/", EventSlotsListView.as_view(), name="event_slots_list"),
]
