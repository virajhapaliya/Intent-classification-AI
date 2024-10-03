from rest_framework import serializers
from django.db import models
from django.db.models import QuerySet
from typing import List, Any


def get_response_serializer(
    model: models.Model, fields: List[str] = [], exclude_fields: List[str] = []
):
    if not any([fields, exclude_fields]):
        raise ValueError("Please provide either of fields : fields or exclude fields")

    # if  all(fields and exclude_fields):
    if fields and exclude_fields:
        raise ValueError(
            "Please only provide either of fields : fields or exclude fields"
        )

    class ResponseSerializer(serializers.ModelSerializer):
        class Meta:
            pass

    ResponseSerializer.Meta.model = model
    if fields:
        ResponseSerializer.Meta.fields = fields
    else:
        ResponseSerializer.Meta.exclude = exclude_fields

    return ResponseSerializer


class BaseModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(BaseModelSerializer, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.error_messages = get_error_messages_code(field_name)


def get_crud_serializer(model: models.Model, fields: list = [], update=True):

    if not fields:
        raise ValueError("Please provide fields to edit.")
    if not model:
        raise ValueError("Please provide model for the serializer")

    class BaseCrudSerializer(BaseModelSerializer):
        def __init__(self, *args, **kwargs):
            if update:
                pk_field = self.Meta.model._meta.pk.name
                self.fields[pk_field] = serializers.PrimaryKeyRelatedField(
                    queryset=self.Meta.model.objects.dfilter(),
                    required=True,
                )
            super(BaseCrudSerializer, self).__init__(*args, **kwargs)

            for field_name, field in self.fields.items():
                field.required = True

        class Meta:
            pass

    BaseCrudSerializer.Meta.model = model

    BaseCrudSerializer.Meta.fields = fields

    return BaseCrudSerializer


class BaseSerializerSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super(BaseSerializerSerializer, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.error_messages = get_error_messages_code(field_name)


def get_error_messages_code(field_name: str = None, extra_kwargs_fields: list = None):
    if field_name:
        return {
            "null": f"{field_name}_null",
            "required": f"{field_name}_required",
            "blank": f"{field_name}_blank",
            "invalid": f"{field_name}_invalid",
            "does_not_exist": f"{field_name}_does_not_exist",
            "incorrect_type": f"{field_name}_invalid",
            "min_value": f"{field_name}_min_value",
            "max_value": f"{field_name}_max_value",
            "max_length": f"{field_name}_max_length",
            "does_not_exist": f"{field_name}_does_not_exist",
        }
    elif extra_kwargs_fields:
        return {
            field_name: {
                "error_messages": get_error_messages_code(field_name=field_name)
            }
            for field_name in extra_kwargs_fields
        }


def get_full_error_messages(field_name, field_error):
    _base_messages_dict = {
        f"{field_name}_null": f"{field_name} should not be null.",
        f"{field_name}_required": f"Key : {field_name} is missing.",
        f"{field_name}_blank": f"Please enter value for {field_name}.",
        f"{field_name}_invalid": f"Please enter a valid value for Field : {field_name}.",
        f"{field_name}_does_not_exist": "No record found.",
        f"{field_name}_incorrect_type": f"Please enter a valid value for Field : {field_name}.",
        f"{field_name}_min_value": f"Please enter a value greater than min value.",
        f"{field_name}_max_value": f"You have exceeded the maximum value for {field_name}",
        f"{field_name}_max_length": f"You have exceeded the maximum length for {field_name}",
    }

    return _base_messages_dict[field_error]


def get_error_message(serializer_errors, error_messages_dict) -> tuple:

    error_field = list(serializer_errors.keys())[0]

    for field_error in serializer_errors.values():
        if error_field == "non_field_errors":
            return field_error[0], error_messages_dict[field_error[0]]

        else:
            return (
                field_error[0],
                get_full_error_messages(
                    field_name=error_field, field_error=field_error[0]
                ),
            )
