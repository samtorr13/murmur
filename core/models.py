from django.db import models
import uuid

class GlobalPostIdentifier(models.Model):
    """
    Genera un identificador global compartido por Posts y Comments.
    """
    general_pid = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"GlobalPID {self.general_pid}"