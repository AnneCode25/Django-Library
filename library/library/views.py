from django.shortcuts import render

def handler404(request, exception):
    context = {
        'message': "Désolé, cette page n'existe pas !",
        'title': "Page non trouvée"
    }
    return render(request, 'errors/404.html', context, status=404)