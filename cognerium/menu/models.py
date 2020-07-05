from django.db import models

# Create your models here.


class CogneriumModelManager(models.Manager):
    '''
    This should be the model manager for all models in the project
    '''

    def get_active_objects(self):
        '''
        This will return only active object of the model
        '''
        return super(CogneriumAbstractModel, self).get_queryset().filter(is_active=True)

    def get_inactive_objects(self):
        '''
        This will return only active object of the model
        '''
        return super(CogneriumAbstractModel, self).get_queryset().filter(is_active=False)


class CogneriumAbstractModel(models.Model):

    created_date = models.DateTimeField(
        auto_now_add=True,
        help_text='This field is from CogneriumAbstractModel abstract class'
    )
    upated_date = models.DateTimeField(
        auto_now=True,
        help_text='This field is from CogneriumAbstractModel abstract class'
    )
    is_active = models.BooleanField(
        default=False,
        help_text='This field is from CogneriumAbstractModel abstract class'
    )

    class Meta:
        abstract = True
