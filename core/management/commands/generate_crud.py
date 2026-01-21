import os
from django.core.management.base import BaseCommand
from django.apps import apps
from core.crud.facade import CRUDFacade


class Command(BaseCommand):
    help = "Generate full CRUD (API + Web + Export + Permissions) for a model"

    def add_arguments(self, parser):
        parser.add_argument("app_name", type=str)
        parser.add_argument("model_name", type=str)

    def handle(self, *args, **options):
        app_name = options["app_name"]
        model_name = options["model_name"]

        model = apps.get_model(app_name, model_name)
        facade = CRUDFacade(model, app_name)
        result = facade.generate_all()

        base_path = os.path.join(app_name, "generated", model_name.lower())
        os.makedirs(base_path, exist_ok=True)

        for key, content in result.items():
            if isinstance(content, dict):  # templates
                template_dir = os.path.join(base_path, "templates")
                os.makedirs(template_dir, exist_ok=True)
                for filename, filecontent in content.items():
                    with open(os.path.join(template_dir, filename), "w", encoding="utf-8") as f:
                        f.write(filecontent)
            else:
                with open(os.path.join(base_path, f"{key}.py"), "w", encoding="utf-8") as f:
                    f.write(content)

        self.stdout.write(self.style.SUCCESS("CRUD generated successfully!"))
