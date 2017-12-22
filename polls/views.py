from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from django.urls import reverse
from django.views import generic
from .models import Question, Choice
# Create your views here.

class IndexView(generic.ListView):
    template_name = 'polls/index2.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail1.html'

class ResultView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html.html'



def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')
    template = loader.get_template('polls/index2.html')
    context = RequestContext(request, {
        'lastest_question_list': latest_question_list
    })
    #output = ', '.join([p.question_text for p in latest_question_list])
    return HttpResponse(template.render({'latest_question_list':latest_question_list}))

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail1.html', {'question':question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question':question})


def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail1.html', {
            'question':p,
            'error_message':"You didn't select a choice",
        })
    else:
        selected_choice.votes += 1;
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))


