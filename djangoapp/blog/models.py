from django.db import models
from utils.rands import slugify_new


class Tag(models.Model):
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    name = models.CharField(max_length=30)
    slug = models.SlugField(
        unique=True, default=None, null=True, blank=True,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.name)
        return super().save(*args, **kwargs)
