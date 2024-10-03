from django.apps import AppConfig
from django.db.utils import OperationalError


class StudentsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "students"
    # def ready(self):
    #     from students.models import Subject  # Import your model here
        
    #     try:
    #         if not Subject.objects.exists():  # Check if table is empty
    #             # Populate static table with default data
    #             Subject.objects.bulk_create([
    #                 Subject(name='math'),
    #                 Subject(name='science'),
    #                 Subject(name='history'),
    #                 Subject(name='physics'),
    #                 # Add more default subjects as needed
    #             ])
    #     except OperationalError:
    #         # Handle case where migrations haven't been applied yet
    #         pass