from django.db import models


class Template(models.Model):
    title = models.CharField('Заголовок', max_length=250)
    description = models.CharField('Описание шаблона', max_length=250)
    content = models.TextField('Контекст шаблона')

    def __str__(self):
        return f'Шаблон: {self.title}'

    class Meta:
        verbose_name = 'Шаблон'
        verbose_name_plural = 'Шаблоны'


class Notification(models.Model):
    template = models.ForeignKey('Template', on_delete=models.CASCADE)


    def __str__(self):
        return f'Уведомление: {self.id}'

    class Meta:
        verbose_name = 'Нотификация'
        verbose_name_plural = 'Нотификации'