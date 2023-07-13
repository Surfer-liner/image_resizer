from django.db import models
import hashlib


class ResizedImage(models.Model):
    """
    Модель для хранения информации о измененных изображениях.
    """
    file_path = models.CharField(max_length=255)
    file_hash = models.CharField(max_length=32, unique=True)
    size = models.PositiveIntegerField()
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """
        Переопределение метода save для вычисления хеша файла перед сохранением.

        Args:
            *args: Позиционные аргументы.
            **kwargs: Именованные аргументы.

        Returns:
            None
        """
        file_hash = hashlib.md5(self.file_path.encode()).hexdigest()
        self.file_hash = file_hash

        super().save(*args, **kwargs)
