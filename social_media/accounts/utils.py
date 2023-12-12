from rest_framework.pagination import PageNumberPagination
from rest_framework import permissions
from accounts.models import User, Friend
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = "page_size"

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.id == request.user
    
class CreateOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if(request.method == "POST"):
            return True
        return True #False
    
def FindFriends(user, status_type):
    queryset1 = Friend.objects.filter(requester=user, status_type=status_type).values_list('requestee', flat=True)
    qs_array1 = [str(i) for i in queryset1]
    queryset2 = Friend.objects.filter(requestee=user, status_type=status_type).values_list('requester', flat=True)
    qs_array2 = [str(i) for i in queryset2]
    qs_array = qs_array1 + qs_array2
    #print ("Printing QS 1-> ", queryset1, "Printing QS 2-> ", queryset2, "Printing QS-> ", qs_array)
    return qs_array