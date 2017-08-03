from dal import autocomplete
from django.db.models import F, Q
from cities.models import City, AlternativeName
from django.views.generic import DetailView, ListView, RedirectView, UpdateView, CreateView
from hitcount.views import HitCountDetailView
from free_traveler.traveler.models import Travel, Car, Proposal, TravelerCity
from django.contrib.auth.mixins import LoginRequiredMixin
from free_traveler.traveler.forms import RouteCreateForm


class TripDetailView(HitCountDetailView):
    model = Trip
    count_hit = True
    # These next two lines tell the view to index lookups by username
    #slug_field = 'username'
    #slug_url_kwarg = 'username'


'''
class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})
'''

class TripCreateView(LoginRequiredMixin, CreateView):

    model = Trip
    form_class = TripCreateForm
    
    def form_valid(self, form):
        start_city = TravelerCity.objects.get_or_create(city=form.cleaned_data['route_from'].city, start=True)
        end_city = TravelerCity.objects.get_or_create(city=form.cleaned_data['route_to'].city, end=True)
        form.instance.cities.add(start_city, end_city)
        form.instance.user = self.request.user
        return super(TripCreateView, self).form_valid(form)
    
    '''
    # send the user back to their own page after a successful update
    def get_success_url(self):
        print(self.kwargs.id)
        return reverse('traveler:route-detail',
                       kwargs={'id': self.kwargs.id})
    '''
    '''
    def get_object(self):
        # Only get the User record for the user making the request
        return Route.objects.get(username=self.request.user.username)
    '''

class TripUpdateView(LoginRequiredMixin, UpdateView):

    model = Trip
    form_class = TripCreateForm

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)


class TripListView(ListView):
    model = Trip
    # These next two lines tell the view to index lookups by username
    #slug_field = 'username'
    #slug_url_kwarg = 'username'

    def get_queryset(self):
        qs = super(TripListView, self).get_queryset()
        return qs.filter(
            Q(cities__city=self.kwargs['city_from'], cities__start=True) |
            Q(cities__city=self.kwargs['city_to'], cities__start=False)
            )


class CarDetailView(HitCountDetailView):
    model = Car
    count_hit = True
    # These next two lines tell the view to index lookups by username
    #slug_field = 'username'
    #slug_url_kwarg = 'username'


class CarCreateView(LoginRequiredMixin, CreateView):

    model = Car
    
    
class CarUpdateView(LoginRequiredMixin, UpdateView):

    model = Car

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse('traveler:car',
                       kwargs={'id': self.kwargs.id})

    def get_object(self):
        # Only get the User record for the user making the request
        return Car.objects.get(id=self.kwargs.id)


class CityAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return City.objects.none()

        #qs = City.objects.prefetch_related('alt_names').all()
        #qs = AlternativeName.objects.filter(language_code=self.request.LANGUAGE_CODE).all()[:10]
        qs = AlternativeName.objects.filter(language_code=self.request.LANGUAGE_CODE).all()

        if self.q:

        	#qs = qs.filter(alt_names__name__istartswith=self.q, alt_names__language_code=self.request.LANGUAGE_CODE)
        	qs = qs.filter(city__isnull=False, name__istartswith=self.q).all()[:10]
        	print(qs)

        return qs


