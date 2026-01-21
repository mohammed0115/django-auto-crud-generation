from textwrap import dedent


def generate_exports(facade):
    model = facade.model_class_name
    model_lower = facade.model_name

    return dedent(f"""
    import csv
    from django.http import HttpResponse
    from {facade.app_name}.models import {model}


    def export_{model_lower}_csv(request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{model_lower}.csv"'

        writer = csv.writer(response)
        fields = [field.name for field in {model}._meta.fields]
        writer.writerow(fields)

        for obj in {model}.objects.all():
            writer.writerow([getattr(obj, field) for field in fields])

        return response
    """)
