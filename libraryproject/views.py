from django.shortcuts import render


def developedby(request):
    return render(request, 'developedby.html')