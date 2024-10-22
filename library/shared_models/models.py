from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    is_librarian = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Member(models.Model):
    first_name = models.CharField(max_length=100, null=False, default="Prénom")
    last_name = models.CharField(max_length=100, null=False, default="Nom")

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'

    def can_borrow(self):
        """
        Vérifie si le membre peut emprunter un nouveau livre.
        Retourne True si le membre a moins de 3 emprunts en cours, False sinon.
        """
        current_loans = self.loans.filter(return_date__isnull=True).count()
        return current_loans < 3

    def has_overdue_loans(self):
        current_date = timezone.now().date()
        overdue_loans = [
            loan for loan in self.loans.filter(return_date__isnull=True)
            if (current_date - loan.loan_date).days > 7
        ]
        return len(overdue_loans) > 0

    class Meta:
        ordering = ['last_name', 'first_name']


class Media(models.Model):
    title = models.CharField(max_length=200)
    is_available = models.BooleanField(default=True)

    class Meta:
        abstract:True

    def __str__(self):
        return self.title

class Book(Media):
    author = models.CharField(max_length=200)

class DVD(Media):
    director = models.CharField(max_length=200)

class CD(Media):
    artist = models.CharField(max_length=200)


class BoardGame(models.Model):
    name = models.CharField(max_length=200)
    creator = models.CharField(max_length=200)


class Loan(models.Model):
    member = models.ForeignKey('Member', on_delete=models.CASCADE, related_name='loans')
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='loans')
    loan_date = models.DateField(default=timezone.now)
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.member} a emprunté {self.book}"

    def due_date(self):
        return self.loan_date + timezone.timedelta(days=7)

    def is_overdue(self):
        return timezone.now().date() > self.due_date() \
            if not self.return_date \
            else False

    class Meta:
        ordering = ['-loan_date']