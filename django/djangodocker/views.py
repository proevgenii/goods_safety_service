from django.shortcuts import render


def tittle(request):
    context = dict()
    return render(request, "tittle.html", context)
