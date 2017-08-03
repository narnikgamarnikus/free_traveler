from dal import autocomplete
from django import forms
from free_traveler.traveler.models import Route, TravelerCity
from django.forms import formset_factory

class TravelerCity(forms.ModelForm):
	class Meta:
		model = TravelerCity
		exclude = ['is_removed', 'created_at', 'modifed_at']


class TripCreateForm(forms.ModelForm):
	class Meta:
		model = Route
		exclude = ['is_removed', 'created_at', 'modifed_at', 'state']
		widgets = {
			'city_from': autocomplete.ModelSelect2(url='traveler:city-autocomplete'),
			'city_to': autocomplete.ModelSelect2(url='traveler:city-autocomplete')
		}