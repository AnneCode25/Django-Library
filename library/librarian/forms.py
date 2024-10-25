from django import forms
from shared_models.models import Loan, Book, Member

class AddMemberForm(forms.ModelForm):
    class Meta :
        model = Member
        fields = ['first_name', 'last_name']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['first_name', 'last_name']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


from django import forms
from shared_models.models import Member, Book, DVD, CD

class LoanForm(forms.Form):
    member = forms.ModelChoiceField(
        queryset=Member.objects.all(),
        label="Membre"
    )
    item_type = forms.ChoiceField(
        choices=[
            ('', '---'),
            ('book', 'Livre'),
            ('dvd', 'DVD'),
            ('cd', 'CD')
        ],
        label="Type de média"
    )
    item = forms.ModelChoiceField(
        queryset=None,  # On va le définir dynamiquement
        label="Item",
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si le formulaire est soumis avec un type de média
        if 'item_type' in self.data:
            try:
                item_type = self.data.get('item_type')
                if item_type == 'book':
                    self.fields['item'].queryset = Book.objects.filter(is_available=True)
                elif item_type == 'dvd':
                    self.fields['item'].queryset = DVD.objects.filter(is_available=True)
                elif item_type == 'cd':
                    self.fields['item'].queryset = CD.objects.filter(is_available=True)
            except (ValueError, TypeError):
                pass
        else:
            self.fields['item'].queryset = Book.objects.none()  # Champ vide par défaut


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'is_available']
        labels = {
            'title': 'Titre',
            'author': 'Auteur',
            'is_available': 'Disponible'
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

class DVDForm(forms.ModelForm):
    class Meta:
        model = DVD
        fields = ['title', 'director', 'is_available']
        labels = {
            'title': 'Titre',
            'director': 'Directeur',
            'is_available': 'Disponible'
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'director': forms.TextInput(attrs={'class': 'form-control'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

class CDForm(forms.ModelForm):
    class Meta:
        model = CD
        fields = ['title', 'artist', 'is_available']
        labels = {
            'title': 'Titre',
            'artist': 'Artiste',
            'is_available': 'Disponible'
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'artist': forms.TextInput(attrs={'class': 'form-control'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }