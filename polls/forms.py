from django import forms
from .models import Poll, PollQuestion, PollChoice

class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['title', 'creator_email']

class PollQuestionForm(forms.ModelForm):
    class Meta:
        model = PollQuestion
        fields = ['question_text']

class PollChoiceForm(forms.ModelForm):
    class Meta:
        model = PollChoice
        fields = ['choice_text']
