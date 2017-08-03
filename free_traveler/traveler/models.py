import uuid
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from image_cropping import ImageRatioField
from cities.models import City
from geoposition.fields import GeopositionField
from django.core.exceptions import ValidationError
from model_utils.models import SoftDeletableModel, TimeStampedModel
from model_utils import FieldTracker
from django_fsm import ConcurrentTransitionMixin, FSMField, transition
from free_traveler.users.models import User
from django_prices.models import PriceField
import googlemaps


@python_2_unicode_compatible
class State(object):
    '''
    Constants to represent the `state`s of the Servuces Models
    '''
    NEW = 'new'              
    ACCEPTED = 'accepted'
    IN_PROGRESS = 'in_progress'
    SUSPENDED = 'suspended'
    RESUMED = 'resumed'
    COMPLETE = 'complete'
    WITHDRAWN = 'withdrawn'
    REJECTED = 'rejected'
    ARRIVED = 'arrived'
    ACCEPT_ARRIVED = 'accept_arrived'
    RECRUITMENT_ON = 'recruitment_on'
    RECRUITMENT_OFF = 'recruitment_off'
    IN = 'in'
    OUT = 'out'

    PROPOSAL_STATES = (
    	(NEW, _('New')),
    	(ACCEPTED, _('Accepted')),
    	(ARRIVED, = _('I\'m arrived at the place')),
    	(ACCEPT_ARRIVED, = _('Accepted arrived'))
    	(REJECTED, _('Rejected')),

    )

    TRAVEL_STATES = (
    	(RECRUITMENT_ON, _('Recruitment available')),
    	(SUSPENDED, _('Recruitment suspended')),
    	(RESUMED, _('Recruitment resumed')),
    	(RECRUITMENT_OFF, _('Recruitment complete')),
    	(IN_PROGRESS, _('Travel in progress')),
    	(COMPLETE, _('Travel complete')),
    )
    
    '''
    TRAVEL_STATES = (
    	(IN_PROGRESS, _('In progress')),
    	(COMPLETE, _('Complete'))
    )
	'''

@python_2_unicode_compatible
class Base(SoftDeletableModel, TimeStampedModel):
    tracker = FieldTracker()
    
    class Meta:
        abstract = True


@python_2_unicode_compatible
class Image(Base):
	image = models.ImageField(null=True, blank=True)
	alt = models.CharField(max_length=255, null=True, blank=True)
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')
	cropping = ImageRatioField('image', '1200x960', free_crop=True)
	#tags = TaggableManager()

	#class Meta:
	#	verbose_name = "Картинка"
	#	verbose_name_plural = "Картинки"

	def __str__(self):
		return self.alt

@python_2_unicode_compatible
class TravelerCity(Base):
	city = models.ForeignKey(City)
	start = models.BooleanField(default=False)
	end = models.BooleanField(default=True)
	date = models.DateTimeField()

	def __str__(self):
		return self.city.name


@python_2_unicode_compatible
class Car(Base):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	number = models.CharField(max_length=25)
	photoes = GenericRelation(Image)

	class Meta:
		unique_together = (("user", "number"),)

	def __str__(self):
		return '{} {}'.format(self.user, self.number)


@python_2_unicode_compatible
class Trip(ConcurrentTransitionMixin, Base):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

	state = FSMField(
		default=State.RECRUITMENT_ON,
		choices=State.TRAVEL,
		protected=True,
    )

	user = models.ForeignKey(User)
	car = models.ForeignKey(Car)
	
	price = PriceField('Price', currency='USD', max_digits=4, decimal_places=2)

	free_places = models.PositiveSmallIntegerField(
		default=0, 
		validators=[MinValueValidator(
			1, 
			_('The number of travelers can not be less than 1'))
		])
	
	#route_from = models.ForeignKey(City, related_name='route_from')
	
	cities = models.ManyToManyField(TravelerCity)

	#route_to = models.ForeignKey(City, related_name='route_to')

	current_city = models.ForeignKey(City)
	
	start_date = models.DateTimeField()
	end_date = models.DateTimeField()

	travelers = ManyToManyField(User, related_name='travelers')

	origin = GeopositionField()
	destination = GeopositionField()


	def clean(self):
		if self.car.user is not self.user:
			raise ValidationError(_('This car does not belong to this user'))

		if self.cities.objects.count() < 1:
			raise ValidationError(_('You can not create a route without the start and end points'))

		elif self.cities.objects.count() < 2:
			raise ValidationError(_('Specify an endpoint'))

		if travelers.objects.count() > travelers:
			raise ValidationError(_('Free places can not be more than the number of travelers'))

		travels = Travel.objects.filter(user=self.user).exclude(state=State.COMPLETE).count()

		if travels > 1:
			raise ValidationError(_('Complete the last travel before starting a new two'))

	def save(self):
		if self.cities.objects.count >= 2 and self.start_date:
			gmaps = googlemaps.Client(client_id=settings.GEOPOSITION_GOOGLE_MAPS_API_KEY)
			'''
			directions_result = gmaps.directions(
				'{}{}'.format(
				self.cities.objects.first().location.x, 
				self.cities.objects.first().location.y
				),
               	'{}{}'.format(
				self.cities.objects.last().location.x, 
				self.cities.objects.last().location.y
               	),
               	mode="transit",
               	departure_time=self.start_date)
            '''
			directions_result = gmaps.directions(
				self.cities.objects.first(),
				self.cities.objects.last(),
               	mode="transit",
               	departure_time=self.start_date)

	def __str__(self):
		return str(self.id)


@python_2_unicode_compatible
class Proposal(ConcurrentTransitionMixin, Base):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

	state = FSMField(
		default=State.NEW,
		choices=State.PROPOSAL_STATES,
		protected=True,
    )

	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	travel = models.ForeignKey(Travel)
	description = models.CharField(max_length=255)

	class Meta:
		unique_together = (("user", "route"),)

	def save(self, *args, **kwargs):
		if self.ACCEPT_ARRIVED

	def __str__(self):
		return str(self.id)

'''
class Travel(ConcurrentTransitionMixin, Base):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

	state = FSMField(
		default=State.IN_PROGRESS,
		choices=State.TRAVEL_STATES,
		protected=True,
	)
	user = models.ForeignKey(User)
	route = models.ForeignKey(Route)

	current_city = models.ForeignKey(City)

	class Meta:
		unique_together = (("user", "route"),)

	def save(self, *args, **kwargs):
		if not self.id:
			travels = Travel.objects.filter(user=self.user).exclude(state=State.COMPLETE).count()
			if travels > 0:
				raise ValidationError(_('Complete the last travel before starting a new one'))
'''