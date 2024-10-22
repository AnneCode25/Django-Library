from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from shared_models.models import Member
from .forms import AddMemberForm, MemberForm

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