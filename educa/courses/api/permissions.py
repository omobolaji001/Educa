from rest_framework.permissions import BasePermission


class IsEnrolled(BasePermission):
    """ Custom permission """
    def has_object_permission(self, request, view, obj):
        """ Checks if a student is enrolled for a course """
        return obj.students.filter(id=request.user.id).exists()
