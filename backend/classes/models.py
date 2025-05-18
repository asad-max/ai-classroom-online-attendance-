from django.db import models
from accounts.models import CustomUser
import uuid
def generate_join_code():
    import uuid
    return uuid.uuid4().hex[:8].upper()

class ClassRoom(models.Model):
    name = models.CharField(max_length=100)
    subject_code = models.CharField(max_length=20)
    instructor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_classes')
    students = models.ManyToManyField(CustomUser, related_name='joined_classes', blank=True)
    join_code = models.CharField(max_length=20, unique=True, default=generate_join_code)
    is_live = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject_code}"

