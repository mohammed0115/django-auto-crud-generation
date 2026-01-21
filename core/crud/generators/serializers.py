from textwrap import dedent


def generate_serializers(facade):
    return dedent(f"""
    from rest_framework import serializers
    from {facade.app_name}.models import {facade.model_class_name}


    class {facade.model_class_name}Serializer(serializers.ModelSerializer):
        class Meta:
            model = {facade.model_class_name}
            fields = "__all__"
    """)
