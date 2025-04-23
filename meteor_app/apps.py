from django.apps import AppConfig



# meteor_app/apps.py
from django.apps import AppConfig

class MeteorAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'meteor_app'

    def ready(self):
        import meteor_app.signals