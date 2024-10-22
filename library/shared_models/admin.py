from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Member, Book, DVD, CD, Loan


UserAdmin.list_display += ('is_librarian',)
UserAdmin.list_filter += ('is_librarian',)
UserAdmin.fieldsets += (('Library Status', {'fields': ('is_librarian',)}),)

admin.site.register(User, UserAdmin)
admin.site.register(Member)
admin.site.register(Book)
admin.site.register(DVD)
admin.site.register(CD)
admin.site.register(Loan)