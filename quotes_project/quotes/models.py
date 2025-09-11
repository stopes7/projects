from django.db import models
from django.core.exceptions import ValidationError

class Quote(models.Model):
    text = models.TextField(unique=True)
    source = models.CharField(max_length=255)
    weight = models.PositiveIntegerField(default=1)
    views = models.PositiveIntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def clean(self):
        # Уникальность текста: TextField(unique=True) уже накладывает DB/Model ограничение,
        # но мы также защищаем ограничение по количеству цитат у источника.
        if Quote.objects.filter(source=self.source).exclude(pk=self.pk).count() >= 3:
            raise ValidationError({"source": "У одного источника не может быть больше 3 цитат."})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.text[:50]}... ({self.source})"