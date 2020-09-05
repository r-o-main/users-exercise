from django.db import models


class User(models.Model):
    """ User data model.
        NB:
          - an id field is automatically added to the data model.
          - all fields but address are mandatory.
          - email should be unique: only one user with the same email.
          - address is stored as a single text field for simplicity.
            If needed in a real production environment, it could be split into several fields or even a dedicated model.
          - password is not obfuscated nor encrypted. A maximum length is requested by CharField.
    """

    first_name = models.CharField(max_length=70, blank=False)
    last_name = models.CharField(max_length=70, blank=False)
    email = models.EmailField(blank=False, unique=True)
    password = models.CharField(max_length=128, blank=False)
    address = models.TextField(max_length=300)


    def __str__(self):
        return f'{self.first_name} {self.last_name}'


    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['last_name', 'first_name'], name='last_first_name_idx'),
            models.Index(fields=['email'], name='email_idx'),
        ]
        ordering = ('last_name',)
