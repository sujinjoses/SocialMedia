#from django.contrib.auth.models import User
from accounts.models import User
from rest_framework import viewsets, permissions
from accounts.serializers import UserRegisterSerializer, UserListSerializer
from accounts.utils import StandardResultsSetPagination, IsOwnerOrReadOnly, CreateOnlyPermission
from rest_framework.generics import CreateAPIView
class UserRegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (CreateOnlyPermission,)
    serializer_class = UserRegisterSerializer

class UserListView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly,)
    serializer_class = UserListSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        search_key = self.request.GET.get('search_key', False)
        queryset = self.queryset
        if(search_key):
            queryset = self.queryset.filter(email=search_key)
            if(queryset):
                return queryset
            else:
                queryset = self.queryset.filter(first_name__icontains=search_key)
        return queryset
        