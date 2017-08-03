from django.apps import AppConfig


class TravelerConfig(AppConfig):
    name = 'free_traveler.traveler'
    verbose_name = "Traveler"

    def ready(self):
        pass
