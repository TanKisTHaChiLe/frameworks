from django.db import models

from courses.models import Course


class Material(models.Model):
    class Category(models.TextChoices):
        LECTURE = "lecture", "Лекция"
        PRACTICE = "practice", "Практическое задание"
        EXAM = "exam", "Подготовка к экзамену"

    course = models.ForeignKey(
        Course, on_delete=models.PROTECT, related_name="materials",
    )
    title = models.CharField(max_length=255, db_index=True)
    category = models.CharField(max_length=8, choices=Category.choices)
    publication_year = models.PositiveSmallIntegerField()
    is_published = models.BooleanField(default=False)
    min_study_year = models.PositiveSmallIntegerField(default=1)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(category__in=("lecture", "practice", "exam")),
                name="material_category_valid",
            ),
            models.CheckConstraint(
                condition=models.Q(publication_year__range=(1900, 2100)),
                name="material_publication_year_valid",
            ),
            models.CheckConstraint(
                condition=models.Q(min_study_year__range=(1, 6)),
                name="material_year_1_6",
            ),
        ]

    def __str__(self):
        return self.title
