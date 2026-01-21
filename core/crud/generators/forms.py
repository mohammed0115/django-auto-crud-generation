from textwrap import dedent


def generate_forms(facade):
    model = facade.model_class_name

    return dedent(f"""
    from django import forms
    from {facade.app_name}.models import {model}


    class {model}Form(forms.ModelForm):
        class Meta:
            model = {model}
            fields = "__all__"
            widgets = {{
                field.name: forms.TextInput(attrs={{
                    "class": "form-control",
                    "placeholder": field.name.replace("_", " ").title(),
                }})
                for field in {model}._meta.fields
            }}
    """)
