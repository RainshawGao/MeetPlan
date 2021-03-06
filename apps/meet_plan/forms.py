from django import forms

from db.base_model import Convert
from utils.mixin.form import FormMixin
from .models import MeetPlan, MeetPlanOrder, FeedBack
from ..account_auth.models import User


class MeetPlanForm(forms.ModelForm, FormMixin):
    field_order = ['place', 'start_time', 'end_time', 'allow_other', 'message']

    class Meta:
        model = MeetPlan
        fields = [
            'place', 'start_time', 'end_time', 'allow_other', 'message'
        ]
        labels = {
            'place': '地点',
            'start_time': '开始时间',
            'end_time': '结束时间',
            'allow_other': '允许多人',
            'message': '备注',
        }
        help_texts = {}
        widgets = {
            'place': forms.TextInput(attrs={'class': 'form-control'}),
            'start_time': forms.DateTimeInput(attrs={'class': 'form-control',
                                                     'id': 'starttimepicker',
                                                     'placeholder': 'yyyy/MM/dd HH:mm',
                                                     'readonly': 'readonly'}),
            'end_time': forms.DateTimeInput(attrs={'class': 'form-control',
                                                   'id': 'endtimepicker',
                                                   'placeholder': 'yyyy/MM/dd HH:mm',
                                                   'readonly': 'readonly'}),
            'allow_other': forms.Select(attrs={'class': 'form-control'},
                                        choices=MeetPlan.AllowOtherChoices),
            'message': forms.Textarea(attrs={'class': 'form-control',
                                             'row': '5',
                                             'placeholder': 'Enter...'})
        }


class MeetPlanFastCreateForm(forms.Form, FormMixin):
    LONG_CHOICES = (
        (1, '半小时'),
        (2, '一小时'),
        (3, '一个半小时'),
        (4, '两个小时')
    )
    EVERY_CHOICES = (
        (1, '否'),
        (2, '是')
    )
    ALLOW_OTHER_CHOICES = (
        (1, '允许'),
        (2, '不允许')
    )
    date = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'id': 'date',
                                                         'readonly': 'readonly'}),
                           label='日期')
    time = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'id': 'time',
                                                         'readonly': 'readonly'}),
                           label='开始时间')
    place = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                            max_length=128)
    long = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                             label='持续时间',
                             help_text='默认一次谈话半小时，选择一小时即在上面所选时间后安排两次谈话',
                             choices=LONG_CHOICES)
    allow_other = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                                    choices=ALLOW_OTHER_CHOICES,
                                    label='允许多人')
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',
                                                           'row': '5',
                                                           'placeholder': 'Enter...'}),
                              label='备注', required=False)
    every_week = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                                   choices=EVERY_CHOICES,
                                   label='每周安排',
                                   help_text='选否则只安排上面所选日期，选是则会自动安排本学期内每周该时间段')

    field_order = [date, time, place, long, allow_other, every_week, message]


class MeetPlanOrderCreateForm(forms.ModelForm, FormMixin):
    class Meta:
        model = MeetPlanOrder
        fields = [
            'message'
        ]
        labels = {
            'message': ''
        }
        help_texts = {
            'message': '填写预计谈话内容，让老师有所准备：（不要超过100字）'
        }
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control',
                                             'row': '5',
                                             'placeholder': 'Enter...'})
        }


class MeetPlanOrderUpdateForm(forms.ModelForm, FormMixin):
    class Meta:
        model = MeetPlanOrder
        fields = [
            'completed'
        ]
        labels = {
            'completed': '是否已经完成交流'
        }


class FeedBackCreateForm(forms.ModelForm, FormMixin):
    class Meta:
        model = FeedBack
        fields = [
            'message'
        ]
        labels = {
            'message': '反馈'
        }
        help_texts = {
            'message': '使用过程中的反馈'
        }

        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control',
                                             'row': '5',
                                             'placeholder': 'Enter...'
                                             }),
        }


class TeacherAddMeetPlanOrderForm(forms.Form, FormMixin):
    from django.core.validators import RegexValidator
    id_regex = RegexValidator(regex=r'^\d{10}$', message="学号格式错误！")
    LONG_CHOICES = (
        (1, '半小时'),
        (2, '一小时'),
    )
    date = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'id': 'date',
                                                         'readonly': 'readonly'}),
                           label='日期')
    time = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'id': 'time',
                                                         'readonly': 'readonly'}),
                           label='开始时间')
    place = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                            max_length=128,
                            label='地点')
    long = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                             label='持续时间',
                             help_text='默认一次谈话半小时，可选择一小时',
                             choices=LONG_CHOICES)
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',
                                                           'row': '5',
                                                           'placeholder': 'Enter...'}),
                              label='备注', required=False)
    stu_id = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                             max_length=20,
                             validators=[id_regex],
                             label='学生学号')

    field_order = [date, time, place, long, stu_id, message]

    def clean(self):
        cleaned_data = super().clean()
        stu_id = cleaned_data.get("stu_id")
        from apps.account_auth.models import User
        student = User.objects.filter(identity_id=stu_id)
        if student.count() != 1:
            msg = "学生学号错误，请再次核对！"
            self.add_error('stu_id', msg)


class StudentAddMeetPlanOrderForm(forms.Form, FormMixin):
    LONG_CHOICES = (
        (1, '半小时'),
        (2, '一小时'),
    )

    teacher = forms.ModelChoiceField(
        queryset=User.objects.filter(is_teacher=True).order_by(Convert('user_name', 'gbk').asc()),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='教师')
    date = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'id': 'date',
                                                         'readonly': 'readonly'}),
                           label='日期')
    time = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'id': 'time',
                                                         'readonly': 'readonly'}),
                           label='开始时间')
    place = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                            max_length=128,
                            label='地点')
    long = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                             label='持续时间',
                             help_text='默认一次谈话半小时，可选择一小时',
                             choices=LONG_CHOICES)
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',
                                                           'row': '5',
                                                           'placeholder': 'Enter...'}),
                              label='备注', required=False)

    field_order = [teacher, date, time, place, long, message]
