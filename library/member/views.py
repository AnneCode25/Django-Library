from django.shortcuts import render
from shared_models.models import Media, Book, CD, DVD

def available_media(request):
    # Récupérer tous les médias disponibles
    available_books = Book.objects.filter(is_available=True)
    available_dvds = DVD.objects.filter(is_available=True)
    available_cds = CD.objects.filter(is_available=True)

    context = {
        'books': available_books,
        'dvds': available_dvds,
        'cds': available_cds,
    }

    return render(request, 'member/available_media.html', context)
