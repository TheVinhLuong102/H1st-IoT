from django.db.models import \
    Model, \
    BooleanField, URLField

from django.contrib.postgres.fields import JSONField

from ..util import MAX_CHAR_LEN


class Blueprint(Model):
    url = \
        URLField(
            max_length=MAX_CHAR_LEN,
            blank=False,
            null=False,
            unique=True)

    active = \
        BooleanField(
            blank=False,
            null=False,
            default=True)

    benchmark_metrics = \
        JSONField(
            default=dict,
            encoder=None)

    class Meta:
        ordering = 'url',

    def __unicode__(self):
        return 'Blueprint "{}"'.format(self.url)
