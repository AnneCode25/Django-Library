from django.contrib import admin
from django.urls import path, include

handler404 = 'library.views.handler404'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('member/', include('member.urls')),
    path('librarian/', include('librarian.urls')),
]