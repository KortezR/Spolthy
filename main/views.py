from django.shortcuts import render


# Create your views here.
def main_page(request):
    return render(request, 'index.html')


def catalog(request):
    return render(request, 'catalog.html')
