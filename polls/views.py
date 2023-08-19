
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from .models import Poll, PollQuestion,  PollParticipant, OneTimePin, PollChoice
from .forms import PollForm, PollQuestionForm, PollChoiceForm


# Homepage
class HomePageView(TemplateView):
    template_name = 'home.html'

def create_poll(request):
    if request.method == 'POST':
        poll_form = PollForm(request.POST)
        if poll_form.is_valid():
            poll = poll_form.save()
            return redirect('add_question', poll_id=poll.id)
    else:
        poll_form = PollForm()
    return render(request, 'create_poll.html', {'poll_form': poll_form})


def add_question(request, poll_id):
    poll = Poll.objects.get(id=poll_id)
    if request.method == 'POST':
        question_form = PollQuestionForm(request.POST)
        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.poll = poll
            question.save()
            return redirect('add_choice', question_id=question.id)
    else:
        question_form = PollQuestionForm()
    return render(request, 'add_question.html', {'question_form': question_form})


def add_choice(request, question_id):
    question = PollQuestion.objects.get(id=question_id)
    if request.method == 'POST':
        choice_form = PollChoiceForm(request.POST)
        if choice_form.is_valid():
            choice = choice_form.save(commit=False)
            choice.question = question
            choice.save()
            return redirect('add_choice', question_id=question.id)
    else:
        choice_form = PollChoiceForm()
    return render(request, 'add_choice.html', {'choice_form': choice_form})


def polls_list(request):
    if request.method == 'POST':
        email = request.POST['email']
        poll_participant, created = PollParticipant.objects.get_or_create(email=email)
        otp = send_otp(email)
        OneTimePin.objects.create(participant=poll_participant, pin=otp)
        return redirect('verify_otp', participant_id=poll_participant.id)
    return render(request, 'polls_list.html')


def send_otp(email):
    otp = get_random_string(length=6, allowed_chars='0123456789')
    send_mail(
        'One Time Pin',
        f'Your One Time Pin: {otp}',
        'sikapa75@gmail.com',
        [email],
        fail_silently=False,
    )
    return otp


def verify_otp(request, participant_id):
    participant = PollParticipant.objects.get(id=participant_id)
    if request.method == 'POST':
        otp = request.POST['otp']
        if OneTimePin.objects.filter(participant=participant, pin=otp).exists():
            participant.has_verified = True
            participant.save()
            return redirect('completion_page', participant_id=participant.id)
    return render(request, 'verify_otp.html', {'participant': participant})


def poll_completion(request, participant_id):
    participant = PollParticipant.objects.get(id=participant_id)
    if not participant.has_verified:
        return redirect('verify_otp', participant_id=participant.id)
    poll = participant.poll
    if request.method == 'POST':
        # Handle user's vote submission
        return redirect('poll_results', poll_id=poll.id)
    return render(request, 'poll_completion.html', {'poll': poll})


# views to display results after inputing data
def poll_results(request, poll_id):
    poll = Poll.objects.get(id=poll_id)
    questions = poll.questions.all()

    results = []
    for question in questions:
        choices = question.choices.all()
        question_results = {'question_text': question.question_text, 'choices': []}
        for choice in choices:
            num_votes = choice.votes.count()
            question_results['choices'].append({'choice_text': choice.choice_text, 'num_votes': num_votes})
        results.append(question_results)

    return render(request, 'poll_results.html', {'poll': poll, 'results': results})
