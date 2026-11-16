import sqlite3
from contextlib import closing
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from courses.models import Course, Student
from materials.models import Material


class Command(BaseCommand):
    help = "Перенести курсы, студентов и материалы из SQLite ПР7 по исходным ID."

    def add_arguments(self, parser):
        parser.add_argument(
            "--source", type=Path,
            default=settings.BASE_DIR / "data" / "learning_portal.sqlite",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        uri = options["source"].resolve().as_uri() + "?mode=ro"
        counts = []
        with closing(sqlite3.connect(uri, uri=True)) as source:
            source.row_factory = sqlite3.Row
            source.execute("BEGIN")
            for table, model in [
                ("courses", Course), ("students", Student), ("materials", Material),
            ]:
                fields = [f.attname for f in model._meta.concrete_fields]
                rows = source.execute(f"SELECT {', '.join(fields)} FROM {table}")
                count = 0
                for row in rows:
                    values = dict(row)
                    model.objects.update_or_create(pk=values.pop("id"), defaults=values)
                    count += 1
                counts.append(f"{table}={count}")
        self.stdout.write(", ".join(counts))
