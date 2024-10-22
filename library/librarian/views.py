from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone 
from django.contrib.auth.decorators import login_required
from shared_models.models import Member, Media, Book, DVD, CD, Loan
from .forms import AddMemberForm, MemberForm, LoanForm
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse

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
    return render(request, 'librarian/dashboard.html')


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