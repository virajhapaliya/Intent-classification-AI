from django.db import models


class Manager(models.Manager):
    """
    Custom manager class that extends Django's default manager and provides additional filtering functionality.

    Methods:
        dfilter(*args, **kwargs): Returns a QuerySet with an added filter condition to exclude soft-deleted instances.

    Usage:
        The `Manager` class should be used as the manager for models that inherit from `BaseModel` to enable the
        additional filtering functionality.

    Example:
        class MyModel(BaseModel):
            objects = Manager()
            # Additional fields and methods specific to MyModel
    """

    def dfilter(self, *args, **kwargs):
        """
        Returns a QuerySet with an added filter condition to exclude soft-deleted instances.

        Arguments:
            *args: Variable-length positional arguments for additional filter conditions.
            **kwargs: Keyword arguments for additional filter conditions.

        Returns:
            QuerySet: A filtered QuerySet that excludes soft-deleted instances.

        Usage:
            my_model_objects = MyModel.objects.dfilter(field1=value1, field2=value2, ...)
        """
        return self.filter(is_deleted=False, **kwargs)


class BaseModel(models.Model):
    """
    Abstract base model class representing a basic model with common fields and functionality.

    Fields:
        created_at (DateTimeField): A field that stores the date and time when the model instance was created.
        updated_at (DateTimeField): A field that stores the date and time when the model instance was last updated.
        is_deleted (BooleanField): A field that indicates whether the model instance has been soft-deleted or not.

    Managers:
        objects (Manager): A custom manager that provides additional query functionality, such as filtering out
                           soft-deleted instances.

    Methods:
        delete(): Marks the model instance as deleted by setting the `is_deleted` field to True and saving
                  the instance.

    Usage:
        The `BaseModel` class should be used as a parent class for other model classes that require common
        fields and functionality such as soft deletion.

    Example:
        class MyModel(BaseModel):
            # Additional fields and methods specific to MyModel
    """

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False, db_index=True)

    objects = Manager()

    def delete(self):
        self.is_deleted = True
        self.save(update_fields=["is_deleted"])

    class Meta:
        abstract = True
        ordering = ["-created_on"]