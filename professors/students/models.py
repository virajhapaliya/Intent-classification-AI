from django.db import models
from professors.utils.base_models import BaseModel

# Create your models here.


class Student(BaseModel):
    """
    This model have personal information about the students
    """
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=20, unique=True)  # Assuming student ID is a unique identifier

    def __str__(self):
        return f"{self.first_name} {self.last_name} (ID: {self.student_id})"
    
class Subject(BaseModel):
    """
    Wil store the name of the subject
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Score(models.Model):
    """
    Score will represent the number student have scored for each subject
    It will unique based on student & subject
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)  

    class Meta:
        unique_together = ('student', 'subject')  

    def __str__(self):
        return f"{self.student} - {self.subject}: {self.score}"