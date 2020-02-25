# Generated by Django 2.2.5 on 2020-02-12 08:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('meet_plan', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meetplan',
            name='stu_id1',
        ),
        migrations.RemoveField(
            model_name='meetplan',
            name='stu_id2',
        ),
        migrations.RemoveField(
            model_name='meetplan',
            name='valid1',
        ),
        migrations.RemoveField(
            model_name='meetplan',
            name='valid2',
        ),
        migrations.AlterField(
            model_name='meetplan',
            name='tea_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='tea_id', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='MeetPlanOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('completed', models.BooleanField(default=False)),
                ('meet_plan_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='meet_plan.MeetPlan')),
                ('stu_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '综合指导课预约',
                'verbose_name_plural': '综合指导课预约',
            },
        ),
    ]
