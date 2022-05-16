from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=30, null=False, verbose_name='Наименование района', unique=True)

    def __str__(self):
        return self.name


class Object(models.Model):
    name = models.CharField(max_length=30, null=False)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='location')

    def __str__(self):
        return f"{self.name} {self.location}"


class Question(models.Model):
    text = models.TextField(null=False)
    significance_score = models.IntegerField(null=False)

    def __str__(self):
        return self.text


class Grade(models.Model):
    name = models.CharField(max_length=5, null=False)

    def __str__(self):
        return self.name


class ControlEvent(models.Model):
    date = models.DateField(verbose_name='Дата проверки')
    object = models.ForeignKey(Object, on_delete=models.CASCADE, verbose_name='Объект')

    def __str__(self):
        return f"{self.date} {self.object}"


class Result(models.Model):
    control_event = models.ForeignKey(ControlEvent, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос')
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, verbose_name='Оценка')

    class Meta:
        unique_together = [['control_event', 'question', 'grade']]


class CorrectionReport(models.Model):
    control_event = models.ForeignKey(ControlEvent, on_delete=models.CASCADE)
    has_given = models.BooleanField(verbose_name='Отчет представлен')
    has_completed = models.BooleanField(verbose_name='Отчёт отработан')


class CorrectionReportComment(models.Model):
    correction_report = models.ForeignKey(CorrectionReport, on_delete=models.CASCADE)
    comment = models.TextField(null=False)
