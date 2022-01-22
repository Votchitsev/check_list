from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=30, null=False)

    def __str__(self):
        return self.name


class Object(models.Model):
    name = models.CharField(max_length=30, null=False)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


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
    date = models.DateField()
    object = models.OneToOneField(Object, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date} {self.object}"


class Result(models.Model):
    control_event = models.ForeignKey(ControlEvent, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)

    class Meta:
        unique_together = [['control_event', 'question', 'grade']]