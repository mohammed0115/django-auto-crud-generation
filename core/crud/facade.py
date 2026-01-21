from .generators.views import generate_views
from .generators.serializers import generate_serializers
from .generators.urls import generate_urls
from .generators.forms import generate_forms
from .generators.templates import generate_templates
from .generators.permissions import generate_permissions
from .generators.exports import generate_exports


class CRUDFacade:
    def __init__(self, model, app_name):
        self.model = model
        self.app_name = app_name
        self.model_name = model.__name__.lower()
        self.model_class_name = model.__name__

    def generate_all(self):
        return {
            "serializers": generate_serializers(self),
            "views": generate_views(self),
            "urls": generate_urls(self),
            "forms": generate_forms(self),
            "templates": generate_templates(self),
            "permissions": generate_permissions(self),
            "exports": generate_exports(self),
        }
