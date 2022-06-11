import os

from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model

try:
    get_user_model().objects.create_superuser(os.getenv("ADMIN_NAME"), os.getenv("ADMIN_EMAIL"),
                                              os.getenv("ADMIN_PASSWORD"))
except IntegrityError:
    pass
