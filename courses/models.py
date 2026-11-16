from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.PROTECT, related_name="students",
    )
    name = models.CharField(max_length=255)
    study_year = models.PositiveSmallIntegerField()

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(study_year__range=(1, 6)), name="student_year_1_6",
            ),
        ]

    def __str__(self):
        return self.name
