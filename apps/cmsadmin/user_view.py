from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views.generic import DetailView
from django.views.generic.base import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from utils.mixin.permission import AdminRequiredMixin
from utils.mixin.view import FileUploadViewMixin
from . import urls
from .forms import UserForm, GradeForm, DepartmentForm, MajorForm
from .tasks import account_create_many_user
from ..account_auth.forms import BaseProfileForm, StudentProfileForm, TeacherProfileForm
from ..account_auth.models import User, BaseProfile, StudentProfile, TeacherProfile, Major, Department, Grade
from ..account_auth.tasks import send_account_register_email


class TeacherListView(AdminRequiredMixin, ListView):
    model = User
    template_name = 'cmsadmin/user/teacher_all.html'
    context_object_name = 'user_list'

    def get_queryset(self):
        return super().get_queryset().filter(is_teacher=True).order_by('-identity_id')


class StudentListView(AdminRequiredMixin, ListView):
    model = User
    template_name = 'cmsadmin/user/student_all.html'
    context_object_name = 'user_list'

    def get_queryset(self):
        return super().get_queryset().filter(is_teacher=False).order_by('-identity_id')


class UserCreateView(AdminRequiredMixin, CreateView):
    model = User
    template_name = 'cmsadmin/user/user_create.html'
    form_class = UserForm

    def get_success_url(self):
        if self.object.is_teacher:
            return reverse('cmsadmin:user_teacher_all')
        else:
            return reverse('cmsadmin:user_student_all')

    def form_valid(self, form):
        response = super().form_valid(form)
        # 发邮件
        send_account_register_email.delay(self.object.identity_id)
        return response


class CreateManyUserView(AdminRequiredMixin, FileUploadViewMixin):
    template_name = 'cmsadmin/user/user_create_many.html'

    def get_success_url(self):
        return reverse('cmsadmin:index')

    def form_valid(self, form):
        form.instance.app = urls.app_name
        response = super().form_valid(form)
        # 创建任务
        account_create_many_user.delay(self.object.id)
        return response


class UserDetailView(AdminRequiredMixin, DetailView):
    model = User
    template_name = 'cmsadmin/user/user_detail.html'
    context_object_name = 'user_detail'


class UpdateUserView(AdminRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'cmsadmin/user/user_update.html'

    def get_success_url(self):
        if self.object.is_teacher:
            return reverse('cmsadmin:user_teacher_all')
        else:
            return reverse('cmsadmin:user_student_all')


class UserDeleteView(AdminRequiredMixin, DeleteView):
    model = User
    template_name = 'cmsadmin/user/user_confirm_delete.html'

    def get_success_url(self):
        if self.object.is_teacher:
            return reverse('cmsadmin:user_teacher_all')
        else:
            return reverse('cmsadmin:user_student_all')


class RecoveryUserView(AdminRequiredMixin, View):

    def get(self, request, pk):
        user = User.objects.get_queryset(is_delete=True).get(pk=pk)
        user.is_delete = False
        user.save()
        return HttpResponseRedirect(reverse('cmsadmin:user_delete_list'))


class DeletedUserListView(AdminRequiredMixin, ListView):
    template_name = 'cmsadmin/user/user_deletelist.html'
    paginate_by = 50
    context_object_name = 'user_list'

    def get_queryset(self):
        return User.objects.get_queryset(is_delete=True).order_by('-update_time')


class BaseProfileUpdateView(AdminRequiredMixin, UpdateView):
    model = BaseProfile
    form_class = BaseProfileForm
    template_name = 'cmsadmin/user/base_profile_update.html'

    def get_success_url(self):
        return reverse('cmsadmin:user-detail', kwargs={'pk': self.object.user_id})


class StudentProfileUpdateView(AdminRequiredMixin, UpdateView):
    model = StudentProfile
    form_class = StudentProfileForm
    template_name = 'cmsadmin/user/student_profile_update.html'

    def get_success_url(self):
        return reverse('cmsadmin:user-detail', kwargs={'pk': self.object.user_id})


class TeacherProfileUpdateView(AdminRequiredMixin, UpdateView):
    model = TeacherProfile
    form_class = TeacherProfileForm
    template_name = 'cmsadmin/user/teacher_profile_update.html'

    def get_success_url(self):
        return reverse('cmsadmin:user-detail', kwargs={'pk': self.object.user_id})


class OtherManagementView(AdminRequiredMixin, View):
    def get(self, request):
        context = {
            'total_department_num': Department.objects.all().count(),
            'total_major_num': Major.objects.all().count(),
            'total_grade_num': Grade.objects.all().count(),
        }
        return TemplateResponse(request, template='cmsadmin/user/other_management.html', context=context)


class GradeListView(AdminRequiredMixin, ListView):
    model = Grade
    template_name = 'cmsadmin/user/grade_all.html'
    context_object_name = 'grade_list'


class GradeCreateView(AdminRequiredMixin, CreateView):
    model = Grade
    template_name = 'cmsadmin/user/grade_create.html'
    form_class = GradeForm

    def get_success_url(self):
        return reverse('cmsadmin:user-grade-all')


class GradeUpdateView(AdminRequiredMixin, UpdateView):
    model = Grade
    template_name = 'cmsadmin/user/grade_update.html'
    form_class = GradeForm

    def get_success_url(self):
        return reverse('cmsadmin:user-grade-all')


class GradeDeleteView(AdminRequiredMixin, DeleteView):
    model = Grade
    template_name = 'cmsadmin/user/grade_delete.html'

    def get_success_url(self):
        return reverse('cmsadmin:user-grade-all')


class DepartmentListView(AdminRequiredMixin, ListView):
    model = Department
    template_name = 'cmsadmin/user/department_all.html'
    context_object_name = 'department_list'


class DepartmentCreateView(AdminRequiredMixin, CreateView):
    model = Department
    template_name = 'cmsadmin/user/department_create.html'
    form_class = DepartmentForm

    def get_success_url(self):
        return reverse('cmsadmin:user-department-all')


class DepartmentUpdateView(AdminRequiredMixin, UpdateView):
    model = Department
    template_name = 'cmsadmin/user/department_update.html'
    form_class = DepartmentForm

    def get_success_url(self):
        return reverse('cmsadmin:user-department-all')


class DepartmentDeleteView(AdminRequiredMixin, DeleteView):
    model = Department
    template_name = 'cmsadmin/user/department_delete.html'

    def get_success_url(self):
        return reverse('cmsadmin:user-department-all')


class MajorListView(AdminRequiredMixin, ListView):
    model = Major
    template_name = 'cmsadmin/user/major_all.html'
    context_object_name = 'major_list'


class MajorCreateView(AdminRequiredMixin, CreateView):
    model = Major
    template_name = 'cmsadmin/user/major_create.html'
    form_class = MajorForm

    def get_success_url(self):
        return reverse('cmsadmin:user-major-all')


class MajorUpdateView(AdminRequiredMixin, UpdateView):
    model = Major
    template_name = 'cmsadmin/user/major_update.html'
    form_class = MajorForm

    def get_success_url(self):
        return reverse('cmsadmin:user-major-all')


class MajorDeleteView(AdminRequiredMixin, DeleteView):
    model = Major
    template_name = 'cmsadmin/user/major_delete.html'

    def get_success_url(self):
        return reverse('cmsadmin:user-major-all')
