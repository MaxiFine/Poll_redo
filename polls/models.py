from django.db import models
from django.urls import reverse


class Poll(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    is_closed = models.BooleanField(default=False)
    creator_email = models.EmailField()

    def __str__(self):
        return self.title


class PollQuestion(models.Model):
    poll = models.ForeignKey(Poll, related_name='questions', on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)

    def __str__(self):
        return self.question_text

class PollChoice(models.Model):
    question = models.ForeignKey(PollQuestion, related_name='choices', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=100)

    def __str__(self):
        return self.choice_text

class PollParticipant(models.Model):
    poll = models.ForeignKey(Poll, related_name='participants', on_delete=models.CASCADE)
    email = models.EmailField()
    has_voted = models.BooleanField(default=False)


    def __str__(self):
        return self.email
    
    def vote_status(self):
        return self.has_voted == True


class OneTimePin(models.Model):
    participant = models.ForeignKey(PollParticipant, on_delete=models.CASCADE)
    pin = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
