from django.db import models
# django  has inbuilt user model which helps in authentication alse
from django.contrib.auth.models import User

# Create your models here.
# classname is tablename
class Task(models.Model):
    # we want one(user) to many(tasks) relationship
    user = models.ForeignKey(User,
            on_delete=models.CASCADE,   # if user is deleted then his tasks also get deleted
            null=True,  #in database,this value could be null or not
            blank=True  #allowing form values to be null or not
                             )
    
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True  #means add time automatically when task is created
    )

    def __str__(self):
        return self.title
        
    class Meta:
        ordering = ['complete']  #sort using complete
    
    
