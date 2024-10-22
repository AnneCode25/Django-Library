from django.db import migrations
from django.contrib.contenttypes.models import ContentType


def convert_loans(apps, schema_editor):
    Loan = apps.get_model('shared_models', 'Loan')  # Changé de 'accounts' à 'shared_models'
    Book = apps.get_model('shared_models', 'Book')  # Changé de 'accounts' à 'shared_models'
    ContentType = apps.get_model('contenttypes', 'ContentType')

    book_content_type = ContentType.objects.get_for_model(Book)

    for loan in Loan.objects.all():
        loan.content_type = book_content_type
        loan.object_id = loan.book.id
        loan.save()


class Migration(migrations.Migration):
    dependencies = [
        ('shared_models', '0002_loan_content_type_loan_object_id'),  # Changé de 'accounts' à 'shared_models'
        ('contenttypes', '__latest__'),
    ]

    operations = [
        migrations.RunPython(convert_loans),
    ]