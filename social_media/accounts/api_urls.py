from rest_framework.routers import DefaultRouter
from django.urls import path, re_path, include
from accounts.api_views import user_api, friend_api

router = DefaultRouter()

#router.register("user_register", user_api.UserRegisterView, "user_register",)
router.register("user_list", user_api.UserListView, "user_list",)
router.register("friend_request", friend_api.FriendRequestView, "friend_request",)
router.register("accept_reject", friend_api.FriendAcceptRejectView, "accept_reject",)
router.register("pending_friends", friend_api.PendingListView, "pending_friends",)
router.register("list_friends", friend_api.FriendListView, "list_friends",)
router.register("list_rejected", friend_api.RejectedListView, "list_rejected",)
urlpatterns = [
    re_path(r"^", include(router.urls)),
    path("user_register/", user_api.UserRegisterView.as_view(), name="user_register"),
]
