from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CourseEnrollForm
from courses.models import Course


class StudentRegistrationView(CreateView):
    """ Handles student's registration """
    template_name = 'students/student/registration.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('student_course_list')

    def form_valid(self, form):
        result = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['username'], password=cd['password1'])
        login(self.request, user)

        return result


class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    """ Handles the student's course enrollment """
    course = None
    form_class = CourseEnrollForm

    def form_valid(self, form):
        self.course = form.cleaned_data['course']
        self.course.students.add(self.request.user)

        return super().form_valid(form)

    def get_success_url(self):
        """ Redirects user after successful course enrollment """
        return reverse_lazy('student_course_detail', args=[self.course.id])


class StudentCourseListView(LoginRequiredMixin, ListView):
    """ returns the courses that students are enrolled in """
    model = Course
    template_name = 'students/course/list.html'

    def get_queryset(self):
        """ Returns the queryset """
        qs = super().get_queryset()

        return qs.filter(students__in=[self.request.user])


class StudentCourseDetailView(LoginRequiredMixin, DetailView):
    """ Returns the detail of a course for the current student """
    model = Course
    template_name = 'students/course/detail.html'

    def get_queryset(self):
        """ Returns filtered queryset """
        qs = super().get_queryset()

        return qs.filter(students__in=[self.request.user])

    def get_context_data(self, **kwargs):
        """ overrides the built-in get_context_data method
        to set a module in the context if 
        the module_id url parameter is given.
        """
        context = super().get_context_data(**kwargs)
        course = self.get_object()

        if 'module_id' in self.kwargs:
            context['module'] = course.modules.get(id=self.kwargs['module_id'])
        else:
            context['module'] = course.modules.all()[0]

        return context
