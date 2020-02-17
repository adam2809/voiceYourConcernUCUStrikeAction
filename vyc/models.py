from django.db import models

class QA(models.Model):
    u_id = models.IntegerField()
    question = models.CharField(max_length=50)
    anwser = models.CharField(max_length=50)


class State(models.Model):
    u_id = models.IntegerField()
    state = models.CharField(max_length=50,default='')
