from accounts.models import Friend, User
from accounts.serializers import FriendRequestSerializer, FriendAcceptRejectSerializer, UserListSerializer
from rest_framework import permissions, viewsets
from accounts.utils import IsOwnerOrReadOnly
from django.db import IntegrityError
from rest_framework.serializers import ValidationError
from accounts.utils import FindFriends
from rest_framework.throttling import UserRateThrottle


class FriendRequestView(viewsets.ModelViewSet):
    queryset = Friend.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly,)
    serializer_class = FriendRequestSerializer
    throttle_classes = [UserRateThrottle]
    def perform_create(self, serializer):
        requester = self.request.user
        try:
            serializer.save(requester=requester, status_type=1)
        except IntegrityError:
            raise ValidationError('Request already exists')


class FriendAcceptRejectView(viewsets.ModelViewSet):
    queryset = Friend.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FriendAcceptRejectSerializer
    #pagination_class = StandardResultsSetPagination
    def get_queryset(self):
        queryset = self.queryset.filter(requester = self.request.user, status_type=1)
        return queryset
    
class PendingListView(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserListSerializer

    def get_queryset(self):
        friends = FindFriends(self.request.user,1)
        print("Friends->> ",friends)
        queryset = self.queryset.filter(id__in = friends)
        return queryset
    
class FriendListView(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserListSerializer

    def get_queryset(self):
        friends = FindFriends(self.request.user,2)
        print("Friends->> ",friends)
        queryset = self.queryset.filter(id__in = friends)
        return queryset
    
    
class RejectedListView(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserListSerializer

    def get_queryset(self):
        friends = FindFriends(self.request.user,3)
        print("Friends->> ",friends)
        queryset = self.queryset.filter(id__in = friends)
        return queryset