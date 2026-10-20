#!/usr/bin/env python3
"""Командная строка Django-проекта."""

import os
import sys


def main():
    """Запустить административную команду Django."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "learning_portal.settings")
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
