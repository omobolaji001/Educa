from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from .fields import OrderField
from django.template.loader import render_to_string


class Subject(models.Model):
    """ Represents a Subject """
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        """ Metadata """
        ordering = ['title']

    def __str__(self):
        """ String representation """
        return self.title


class Course(models.Model):
    """ Represents a Course in a subject """
    owner = models.ForeignKey(
        User,
        related_name='courses_created',
        on_delete=models.CASCADE
    )
    subject = models.ForeignKey(
        Subject,
        related_name='courses',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    students = models.ManyToManyField(
        User,
        related_name='courses_joined',
        blank=True
    )

    class Meta:
        """ Metadata """
        ordering = ['-created']

    def __str__(self):
        """ String representation """
        return self.title


class Module(models.Model):
    """ Represents a module in a course """
    course = models.ForeignKey(
        Course,
        related_name='modules',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['course'])

    class Meta:
        """ Metadata """
        ordering = ['order']

    def __str__(self):
        """ String representation of a module """
        return f'{self.order}. {self.title}'


class Content(models.Model):
    """ Represents the module contents and
    define generic relation tp associate any object
    with the content object.
    """
    module = models.ForeignKey(
        Module,
        related_name='contents',
        on_delete=models.CASCADE,
        limit_choices_to={
            'model__in':('text', 'file', 'image', 'video')
        }
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        """ Metadata """
        ordering = ['order']


class ItemBase(models.Model):
    """ Represents base item that other items inherit from
    """
    owner = models.ForeignKey(
        User,
        related_name='%(class)s_related',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        """ Metadata """
        abstract = True

    def __str__(self):
        """ String representation """
        return self.title

    def render(self):
        """ Render a template and return the rendered content as string """
        return render_to_string(
            f'courses/content/{self._meta.model_name}.html',
            {'item': self}
        )


class Text(ItemBase):
    """ Represents text content """
    content = models.TextField()


class File(ItemBase):
    """ Represents file content """
    file = models.FileField(upload_to='files')


class Image(ItemBase):
    """ Represents image content """
    file = models.ImageField(upload_to='images')


class Video(ItemBase):
    """ Represents video content """
    url = models.URLField()
