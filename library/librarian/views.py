from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone 
from django.contrib.auth.decorators import login_required
from shared_models.models import Member, Media, Book, DVD, CD, Loan, BoardGame
from .forms import AddMemberForm, MemberForm, LoanForm, BookForm, DVDForm, CDForm, BoardGameForm
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
import logging

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_librarian:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Identifiant ou mot de passe invalide")
    return render(request, 'librarian/login.html')


def user_logout(request):
    logout(request)
    return redirect('home')


@login_required
def dashboard(request):
    # Statistiques générales
    total_members = Member.objects.count()
    active_loans = Loan.objects.filter(return_date__isnull=True)
    overdue_loans = [loan for loan in active_loans if loan.is_overdue()]

    # Statistiques par type de média
    media_stats = {
        'books': {
            'total': Book.objects.count(),
            'available': Book.objects.filter(is_available=True).count(),
            'name': 'Livres'
        },
        'dvds': {
            'total': DVD.objects.count(),
            'available': DVD.objects.filter(is_available=True).count(),
            'name': 'DVDs'
        },
        'cds': {
            'total': CD.objects.count(),
            'available': CD.objects.filter(is_available=True).count(),
            'name': 'CDs'
        }
    }

    context = {
        'total_members': total_members,
        'media_stats': media_stats,
        'current_loans': active_loans,
        'overdue_loans': overdue_loans,
        'total_loans': active_loans.count(),
        'total_overdue': len(overdue_loans)
    }

    return render(request, 'librarian/dashboard.html', context)


@login_required
def member_list(request):
    members = Member.objects.all().order_by('last_name')
    return render(request, 'librarian/member_list.html', {'members': members})


@login_required
def add_member(request):
    if request.method == 'POST':
        form = AddMemberForm(request.POST)
        if form.is_valid():
            member = form.save(commit=False)
            member.save()
            messages.success(request, f"Le membre '{member.last_name}', '{member.first_name}' a été ajouté avec succès!")
            return redirect('dashboard')
    else:
        form = AddMemberForm()

    return render(request, 'librarian/add_member.html', {'form': form})


@login_required
def member_detail(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    if request.method == 'POST':
        if 'update' in request.POST:
            form = MemberForm(request.POST, instance=member)
            if form.is_valid():
                form.save()
                messages.success(request, f"Le membre '{member.last_name}' '{member.first_name}' a été mis à jour avec succès.")
                return redirect('member_detail', member_id=member.id)
        elif 'delete' in request.POST:
            member.delete()
            messages.success(request, f"Le membre '{member.last_name}' '{member.first_name}' a été supprimé avec succès.")
            return redirect('member_list')
    else:
        form = MemberForm(instance=member)

    return render(request, 'librarian/member_detail.html', {'form': form, 'member': member})


@login_required
def borrow_item(request):
    # Si c'est une requête AJAX pour obtenir les items
    if 'item_type' in request.GET:
        item_type = request.GET.get('item_type')
        items = []
        if item_type == 'book':
            items = Book.objects.filter(is_available=True)
        elif item_type == 'dvd':
            items = DVD.objects.filter(is_available=True)
        elif item_type == 'cd':
            items = CD.objects.filter(is_available=True)

        return JsonResponse({
            'items': [{'id': item.id, 'text': str(item)} for item in items]
        })

    # Traitement normal du formulaire
    if request.method == 'POST':
        form = LoanForm(request.POST)
        if form.is_valid():
            member = form.cleaned_data['member']
            item_type = form.cleaned_data['item_type']
            item = form.cleaned_data['item']

            if member.has_overdue_loans():
                messages.error(request,
                               "Ce membre a des emprunts en retard et ne peut pas emprunter de nouveaux items.")
            elif not member.can_borrow():
                messages.error(request, "Ce membre a déjà atteint la limite de 3 emprunts")
            else:
                content_type = ContentType.objects.get_for_model(item.__class__)
                loan = Loan(
                    member=member,
                    content_type=content_type,
                    object_id=item.id
                )
                loan.save()

                item.is_available = False
                item.save()

                messages.success(request, f"Emprunt de '{item}' par {member} enregistré avec succès!")
                return redirect('borrow_item')
    else:
        form = LoanForm()

    context = {
        'form': form,
        'loans': Loan.objects.filter(return_date__isnull=True),
    }
    return render(request, 'librarian/borrow_item.html', context)


@login_required
def return_list(request):
    # Récupérer tous les emprunts non retournés
    active_loans = Loan.objects.filter(return_date__isnull=True)
    context = {
        'loans': active_loans
    }
    return render(request, 'librarian/return_list.html', context)


@login_required
def confirm_return(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id)

    if request.method == 'POST':
        # Marquer l'emprunt comme retourné
        loan.return_date = timezone.now()
        loan.save()

        # Rendre l'item disponible
        item = loan.item
        item.is_available = True
        item.save()

        messages.success(request, f"Retour de '{item}' par {loan.member} enregistré avec succès!")
        return redirect('return_item')

    context = {
        'loan': loan
    }
    return render(request, 'librarian/confirm_return.html', context)


@login_required
def media_list(request, media_type):
    # Mapping des types de médias vers leurs modèles et noms
    media_mapping = {
        'book': {'model': Book, 'name': 'Livres', 'name_singular': 'Livre'},
        'dvd': {'model': DVD, 'name': 'DVDs', 'name_singular': 'DVD'},
        'cd': {'model': CD, 'name': 'CDs', 'name_singular': 'CD'},
    }

    if media_type not in media_mapping:
        messages.error(request, "Type de média non valide.")
        return redirect('dashboard')

    media_info = media_mapping[media_type]
    items = media_info['model'].objects.all().order_by('title')

    context = {
        'items': items,
        'media_type': media_type,
        'media_name': media_info['name'],
        'media_name_singular': media_info['name_singular']
    }

    return render(request, 'librarian/media_list.html', context)


@login_required
def media_add(request, media_type):
    # Mapping des types de médias vers leurs formulaires et noms
    form_mapping = {
        'book': {'form': BookForm, 'name': 'Livre'},
        'dvd': {'form': DVDForm, 'name': 'DVD'},
        'cd': {'form': CDForm, 'name': 'CD'},
    }

    if media_type not in form_mapping:
        messages.error(request, "Type de média non valide.")
        return redirect('dashboard')

    form_info = form_mapping[media_type]

    if request.method == 'POST':
        form = form_info['form'](request.POST)
        if form.is_valid():
            item = form.save()
            messages.success(request, f"Le {form_info['name']} '{item.title}' a été ajouté avec succès!")
            return redirect('media_list', media_type=media_type)
    else:
        form = form_info['form']()

    context = {
        'form': form,
        'media_type': media_type,
        'media_name': form_info['name']
    }

    return render(request, 'librarian/media_add.html', context)


@login_required
def media_detail(request, media_type, item_id):
    # Mapping des types de médias vers leurs modèles, formulaires et noms
    media_mapping = {
        'book': {'model': Book, 'form': BookForm, 'name': 'Livre'},
        'dvd': {'model': DVD, 'form': DVDForm, 'name': 'DVD'},
        'cd': {'model': CD, 'form': CDForm, 'name': 'CD'},
    }

    if media_type not in media_mapping:
        messages.error(request, "Type de média non valide.")
        return redirect('dashboard')

    media_info = media_mapping[media_type]
    item = get_object_or_404(media_info['model'], id=item_id)

    if request.method == 'POST':
        if 'update' in request.POST:
            form = media_info['form'](request.POST, instance=item)
            if form.is_valid():
                form.save()
                messages.success(request, f"Le {media_info['name']} '{item.title}' a été mis à jour avec succès.")
                return redirect('media_detail', media_type=media_type, item_id=item.id)
        elif 'delete' in request.POST:
            title = item.title
            item.delete()
            messages.success(request, f"Le {media_info['name']} '{title}' a été supprimé avec succès.")
            return redirect('media_list', media_type=media_type)
    else:
        form = media_info['form'](instance=item)

    context = {
        'form': form,
        'item': item,
        'media_type': media_type,
        'media_name': media_info['name']
    }

    return render(request, 'librarian/media_detail.html', context)


# Créer un logger pour l'application
logger = logging.getLogger('librarian')

@login_required
def add_member(request):
    if request.method == 'POST':
        form = AddMemberForm(request.POST)
        if form.is_valid():
            member = form.save(commit=False)
            member.save()
            logger.info(f"Nouveau membre créé: {member.last_name}, {member.first_name} par {request.user.username}")
            messages.success(request, f"Le membre '{member.last_name}', '{member.first_name}' a été ajouté avec succès!")
            return redirect('dashboard')
        else:
            logger.warning(f"Tentative échouée de création de membre par {request.user.username}")
    else:
        form = AddMemberForm()

    return render(request, 'librarian/add_member.html', {'form': form})

@login_required
def borrow_item(request):
    if 'item_type' in request.GET:
        item_type = request.GET.get('item_type')
        items = []
        if item_type == 'book':
            items = Book.objects.filter(is_available=True)
        elif item_type == 'dvd':
            items = DVD.objects.filter(is_available=True)
        elif item_type == 'cd':
            items = CD.objects.filter(is_available=True)

        return JsonResponse({
            'items': [{'id': item.id, 'text': str(item)} for item in items]
        })

    if request.method == 'POST':
        form = LoanForm(request.POST)
        if form.is_valid():
            member = form.cleaned_data['member']
            item_type = form.cleaned_data['item_type']
            item = form.cleaned_data['item']

            if member.has_overdue_loans():
                logger.warning(f"Tentative d'emprunt refusée - retards existants: {member}")
                messages.error(request, "Ce membre a des emprunts en retard...")
            elif not member.can_borrow():
                logger.warning(f"Tentative d'emprunt refusée - limite atteinte: {member}")
                messages.error(request, "Ce membre a déjà atteint la limite de 3 emprunts")
            else:
                content_type = ContentType.objects.get_for_model(item.__class__)
                loan = Loan(
                    member=member,
                    content_type=content_type,
                    object_id=item.id
                )
                loan.save()
                item.is_available = False
                item.save()
                logger.info(f"Nouvel emprunt: {item} par {member}")
                messages.success(request, f"Emprunt de '{item}' par {member} enregistré avec succès!")
                return redirect('borrow_item')
    else:
        form = LoanForm()

    context = {
        'form': form,
        'loans': Loan.objects.filter(return_date__isnull=True),
    }
    return render(request, 'librarian/borrow_item.html', context)


@login_required
def boardgame_list(request):
    boardgames = BoardGame.objects.all().order_by('name')
    return render(request, 'librarian/boardgame_list.html', {'boardgames': boardgames})

@login_required
def boardgame_add(request):
    if request.method == 'POST':
        form = BoardGameForm(request.POST)
        if form.is_valid():
            boardgame = form.save()
            messages.success(request, f"Le jeu '{boardgame.name}' a été ajouté avec succès!")
            return redirect('boardgame_list')
    else:
        form = BoardGameForm()
    return render(request, 'librarian/boardgame_add.html', {'form': form})

@login_required
def boardgame_detail(request, boardgame_id):
    boardgame = get_object_or_404(BoardGame, id=boardgame_id)
    if request.method == 'POST':
        if 'update' in request.POST:
            form = BoardGameForm(request.POST, instance=boardgame)
            if form.is_valid():
                form.save()
                messages.success(request, f"Le jeu '{boardgame.name}' a été mis à jour avec succès.")
                return redirect('boardgame_detail', boardgame_id=boardgame.id)
        elif 'delete' in request.POST:
            name = boardgame.name
            boardgame.delete()
            messages.success(request, f"Le jeu '{name}' a été supprimé avec succès.")
            return redirect('boardgame_list')
    else:
        form = BoardGameForm(instance=boardgame)
    return render(request, 'librarian/boardgame_detail.html', {'form': form, 'boardgame': boardgame})