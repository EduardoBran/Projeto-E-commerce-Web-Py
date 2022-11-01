from django.shortcuts import render


def page_error_404(request, exception):
    return render(request, '404.html', status=404)


def page_error_500(request):
    return render(request, '500.html', status=500)


def page_error_503(request, exception):
    return render(request, '503.html', status=503)
