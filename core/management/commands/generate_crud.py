import os
from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
from core.crud.facade import CRUDFacade

class Command(BaseCommand):
    help = "Generate full CRUD (Web + API + Templates + Exports + Permissions) for a model"

    def add_arguments(self, parser):
        parser.add_argument("app_name", type=str, help="Django app containing the model")
        parser.add_argument("model_name", type=str, help="Model to generate CRUD for")
        parser.add_argument(
            "--template",
            type=str,
            default="bootstrap",
            choices=["bootstrap", "tailwind"],
            help="CSS framework for templates (default: bootstrap)"
        )

    def handle(self, *args, **options):
        app_name = options["app_name"]
        model_name = options["model_name"]
        template = options["template"]

        # جلب الموديل
        try:
            model = apps.get_model(app_name, model_name)
        except LookupError:
            raise CommandError(f"❌ Model '{model_name}' not found in app '{app_name}'.")

        # تهيئة Facade
        try:
            facade = CRUDFacade(model, app_name, template)
            generated = facade.generate_all()

            base_path = os.path.join(app_name, "generated", model_name.lower())
            os.makedirs(base_path, exist_ok=True)

            # حفظ الملفات
            for key, content in generated.items():
                if isinstance(content, dict):  # Templates
                    template_dir = os.path.join(base_path, "templates")
                    os.makedirs(template_dir, exist_ok=True)
                    for filename, filecontent in content.items():
                        with open(os.path.join(template_dir, filename), "w", encoding="utf-8") as f:
                            f.write(filecontent)
                else:
                    with open(os.path.join(base_path, f"{key}.py"), "w", encoding="utf-8") as f:
                        f.write(content)

            self.stdout.write(self.style.SUCCESS(f"\n✅ CRUD generated successfully for '{model_name}'!"))
            self._print_summary(model_name, template)

        except Exception as e:
            raise CommandError(f"❌ Error generating CRUD: {str(e)}")

    def _print_summary(self, model_name, template):
        """عرض ملخص جميل بعد التوليد"""
        self.stdout.write("\n" + "="*60)
        self.stdout.write(self.style.SUCCESS(f"CRUD for '{model_name}' includes:"))
        self.stdout.write(f"  ✓ Web Views (List, Create, Update, Delete, Detail)")
        self.stdout.write(f"  ✓ Forms with {template} styling")
        self.stdout.write(f"  ✓ Templates (list, form, detail, confirm_delete)")
        self.stdout.write(f"  ✓ Web URL patterns")
        self.stdout.write(f"  ✓ REST API Serializer & ViewSet")
        self.stdout.write(f"  ✓ API URL patterns")
        self.stdout.write(f"  ✓ Permissions (Add, Change, Delete, View)")
        self.stdout.write(f"  ✓ Export functions (CSV, Excel optional)")
        self.stdout.write("="*60 + "\n")
