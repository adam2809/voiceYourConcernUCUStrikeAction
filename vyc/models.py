from django.db import models

class QA(models.Model):
    u_id = models.IntegerField()
    question = models.CharField(max_length=50)
    anwser = models.CharField(max_length=50)

    def __str__(self):
        return f'u_id = {self.u_id}\tquestion = {self.question}\tanwser = {self.anwser}\t'

class State(models.Model):
    u_id = models.IntegerField()
    state = models.CharField(max_length=50,default='')

    def __str__(self):
        return f'u_id = {self.u_id}\tstate = {self.state}\t'
