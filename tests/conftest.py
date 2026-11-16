import pytest
from django.core.management import call_command
from django.test.utils import setup_databases, teardown_databases


@pytest.fixture(scope="module")
def portal_database():
    databases = setup_databases(verbosity=0, interactive=False)
    try:
        call_command("import_pr7", verbosity=0)
        yield
    finally:
        teardown_databases(databases, verbosity=0)
