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