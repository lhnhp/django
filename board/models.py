from django.db import models
from acc.models import User
# Create your models here.

class Board(models.Model):
    subject = models.CharField(max_length=100)
    writer = models.ForeignKey(User, on_delete=models.CASCADE , related_name="writer" ,blank=True)
    content = models.TextField()
    likey = models.ManyToManyField(User, related_name="likey",blank=True)
    #User 값이 위와 겹쳐서 relatedname을사용해 이름을 넣어줘야함
    pubdate = models.DateTimeField()

    def __str__(self):
        return f"{self.subject}"
    
    def summary(self):
        if len(self.content) > 30:
            return f"{self.content[:30]} +..."
        return f"{self.content}"
    
class Reply(models.Model):
    b = models.ForeignKey(Board, on_delete=models.CASCADE)
    replyer = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    pubdate = models.DateTimeField()
    
    def __str__(self):
        return f"{self.b}_{self.replyer}"