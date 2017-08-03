from django.conf.urls import include, url
from .views import CityAutocomplete, RouteListView, RouteDetailView, RouteCreateView

urlpatterns = [
	url(
        regex=r'^trip/~create/$',
        view=TripCreateView.as_view(),
        name='trip-create',
    ),
	url(
        regex=r'^trip/(?P<city_from>[\w.@+-]+)/(?P<city_to>[\w.@+-]+)/$',
        view=TripListView.as_view(),
        name='trip-list',
    ),
    url(
        regex=r'^trip/detail/(?P<id>[\w.@+-]+)$',
        view=TripDetailView.as_view(),
        name='trip-detail',
    ),

	url(
        regex=r'^car/~create/$',
        view=CarCreateView.as_view(),
        name='car-create',
    ),
    url(
        regex=r'^car/detail(?P<id>[\w.@+-]+)/$',
        view=CarDetailView.as_view(),
        name='car-detail',
    ),
    url(
        regex=r'^car/update/(?P<id>[\w.@+-]+)$',
        view=CarUpdateView.as_view(),
        name='car-update',
    ),

	url(
        regex=r'^proposal/~create/$',
        view=ProposalCreateView.as_view(),
        name='proposal-create',
    ),
    url(
        regex=r'^proposal/detail(?P<id>[\w.@+-]+)/$',
        view=ProposalDetailView.as_view(),
        name='proposal-detail',
    ),
    url(
        regex=r'^proposal/update/(?P<id>[\w.@+-]+)$',
        view=ProposalUpdateView.as_view(),
        name='proposal-update',
    ),

    url(
        regex=r'^city-autocomplete/$',
        view=CityAutocomplete.as_view(),
        name='city-autocomplete',
    ),


    
]
