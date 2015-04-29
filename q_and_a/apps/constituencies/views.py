from urllib2 import urlopen, HTTPError, URLError
import json

from django.views.generic import ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404

from constituencies.models import Constituency
from candidates.models import Candidate
from questions.models import Answer

def ynmp_get_constituency_from_postcode(postcode):
    postcode = postcode.replace(' ', '').lower()
    url = 'http://mapit.mysociety.org/postcode/%s' % postcode
    wmc_id = None
    wmc_name = None
    try:
        response = urlopen(url)
        status_code = response.getcode()
        page_data = response.read()
        json_data = json.loads(page_data)
        wmc_id = json_data['shortcuts']['WMC']
        wmc_name = json_data['areas'][str(wmc_id)]['name']
    except HTTPError as e:
        status_code = e.code
    return({
        'status_code': status_code,
        'constituency_id': wmc_id,
        'name': wmc_name,
    })

def HomePageView(request):
    if request.method == 'POST':
        postcode = request.POST['postcode']
        wmc_data = ynmp_get_constituency_from_postcode(postcode)
        if wmc_data['status_code'] == 200:
            wmc, wmc_created = Constituency.objects.get_or_create(
                constituency_id=wmc_data['constituency_id'],
                defaults={
                    'name': wmc_data['name']
                }
            )
            return redirect('/constituencies/%d/' % (wmc.constituency_id,))
        else:
            raise Http404("Constituency not found")

    candidates_involved = Candidate.objects.filter(answer__completed=True).distinct().count()
    questions_answered = Answer.objects.filter(completed=True).count()

    return render(request, 'home.html', {
        'candidates_involved': candidates_involved,
        'questions_answered': questions_answered,
    })


class ConstituencyView(ListView):
    model = Candidate
    template_name = 'constituency_list.html'

    def get_queryset(self, **kwargs):
        return Candidate.objects.filter(constituency_id=self.args[0])

    def get_context_data(self, **kwargs):
        context = super(ConstituencyView, self).get_context_data(**kwargs)
	try:
            context['constituency'] = Constituency.objects.get(constituency_id=self.args[0]).name
        except Constituency.DoesNotExist:
            try:
                context['constituency'] = context.first().constituency_name
	    except AttributeError:
                raise Http404("Constituency not found")
        return context
