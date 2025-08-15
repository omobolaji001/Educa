from rest_framework import viewsets
from courses.api.serializers import (
    SubjectSerializer, CourseSerializer, CourseWithContentsSerializer
)
from courses.models import Subject, Course
from django.db.models import Count
from courses.api.pagination import StandardPagination
from rest_framework.decorators import action
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from  rest_framework.response import Response
from courses.api.permissions import IsEnrolled


class SubjectViewSet(viewsets.ReadOnlyModelViewSet):
    """ Provides read-only actions
    to list objects or retrieve an object.
    """
    queryset = Subject.objects.annotate(total_courses=Count('courses'))
    serializer_class = SubjectSerializer
    pagination_class = StandardPagination


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    """ Provides read-only actions
    to list objects or retrieve an object.
    """
    queryset = Course.objects.prefetch_related('modules')
    serializer_class = CourseSerializer
    pagination_class = StandardPagination

    @action(
        detail=True,
        methods=['post'],
        authentication_classes=[BasicAuthentication],
        permission_classes=[IsAuthenticated]
    )
    def enroll(self, request, *args, **kwargs):
        """ Enrolls a student to a particular course """
        course = self.get_object()
        course.students.add(request.user)

        return Response({'enrolled': True})

    @action(
        detail=True,
        methods=['get'],
        serializer_class=CourseWithContentsSerializer,
        authentication_classes=[BasicAuthentication],
        permission_classes=[IsAuthenticated, IsEnrolled]
    )
    def contents(self, request, *args, **kwargs):
        """ Retrieves the contents of a course """
        return self.retrieve(request, *args, **kwargs)
