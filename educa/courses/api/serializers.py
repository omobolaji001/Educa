from rest_framework import serializers
from courses.models import Subject, Course, Module, Content
from django.db.models import Count


class SubjectSerializer(serializers.ModelSerializer):
    """ Serializes the Subject model """
    total_courses = serializers.IntegerField()
    popular_courses = serializers.SerializerMethodField()

    class Meta:
        """ metadata """
        model = Subject
        fields = ['id', 'title', 'slug', 'total_courses', 'popular_courses']

    def get_popular_courses(self, obj):
        """ Retrieve popular courses
        based on the number of students that registered.
        """
        courses = obj.courses.annotate(
            total_students=Count('students')
        ).order_by('-total_students')[:3]

        return [f'{c.title} ({c.total_students})' for c in courses]


class ModuleSerializer(serializers.ModelSerializer):
    """ Serializes the Module model """
    class Meta:
        """ Metadata """
        model = Module
        fields = ['order', 'title', 'description']


class CourseSerializer(serializers.ModelSerializer):
    """ Serializes the Course model """
    modules = ModuleSerializer(many=True, read_only=True)

    class Meta:
        """ Metadata """
        model = Course
        fields = [
            'id', 'subject', 'title', 'slug',
            'overview', 'created', 'owner', 'modules'
        ]


class ItemRelatedField(serializers.RelatedField):
    """ Item related field """
    def to_representation(self, value):
        """ Returns the render method of the item """
        return value.render()


class ContentSerializer(serializers.ModelSerializer):
    """ Serializes the Content model """
    item = ItemRelatedField(read_only=True)

    class Meta:
        model = Content
        fields = ['order', 'item']


class ModuleWithContentsSerializer(serializers.ModelSerializer):
    """ Serializes the Module with the contents """
    contents = ContentSerializer(many=True)

    class Meta:
        """ Metadata """
        model = Module
        fields = ['order', 'title', 'description', 'contents']


class CourseWithContentsSerializer(serializers.ModelSerializer):
    """ Serializes the Course with the contents included """
    modules = ModuleWithContentsSerializer(many=True)

    class Meta:
        """ Metadata """
        model = Course
        fields = [
            'id', 'subject', 'title', 'slug',
            'overview', 'created', 'owner', 'modules'
        ]
