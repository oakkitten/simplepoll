from django.http import HttpResponse, HttpResponseRedirect
from pollapp.models import Poll, Choice
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views import generic

class IndexView(generic.ListView):
    template_name = 'pollapp/index.html'
    context_object_name = 'latest_poll'
    def get_queryset(self):
        return Poll.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Poll
    template_name = 'pollapp/detail.html'

class ResultsView(generic.DetailView):
    model = Poll
    template_name = 'pollapp/results.html'

def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'pollapp/detail.html', {'poll': p, 'error_message': "You didn't select a choice"})
    else:
        selected_choice.votes += 1
        selected_choice.save()

    return HttpResponseRedirect(reverse('results', args=(p.id,)))
