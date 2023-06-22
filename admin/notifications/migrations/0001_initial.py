# Generated by Django 3.2 on 2023-06-22 18:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('personal', 'Индивидуальная'), ('group', 'Групповая')], default='group', max_length=50, verbose_name='Тип рассылки')),
            ],
            options={
                'verbose_name': 'Уведомление',
                'verbose_name_plural': 'Уведомления',
            },
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('event_type', models.SlugField(primary_key=True, serialize=False, verbose_name='Тип события')),
                ('title', models.CharField(max_length=250, verbose_name='Заголовок')),
                ('description', models.CharField(max_length=250, verbose_name='Описание шаблона')),
                ('content', models.TextField(help_text='Текст шаблона письма - HTML страница или просто текст.', verbose_name='Контент шаблона')),
            ],
            options={
                'verbose_name': 'Шаблон',
                'verbose_name_plural': 'Шаблоны',
            },
        ),
        migrations.CreateModel(
            name='NotificationToUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('retry_count', models.IntegerField(default=0, verbose_name='Повторных попыток')),
                ('status', models.CharField(choices=[('sent', 'Отправлено'), ('pending', 'В процессе'), ('failed', 'Не отправлено')], default='pending', max_length=10, verbose_name='Статус')),
                ('last_update', models.DateTimeField(auto_now=True, verbose_name='Последнее обновление')),
                ('notification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notifications.notification')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='NotificationToGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
                ('notification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notifications.notification')),
            ],
        ),
        migrations.AddField(
            model_name='notification',
            name='groups',
            field=models.ManyToManyField(related_name='notifications', through='notifications.NotificationToGroup', to='auth.Group'),
        ),
        migrations.AddField(
            model_name='notification',
            name='template',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notifications.template'),
        ),
        migrations.AddField(
            model_name='notification',
            name='users',
            field=models.ManyToManyField(related_name='notifications', through='notifications.NotificationToUser', to=settings.AUTH_USER_MODEL),
        ),
    ]
