from django.shortcuts import render, redirect

# Create your views here.
def transaccionIndex(request):
    data = {}
    #return redirect('transaccionIndex')
    return render(request, 'partida/partida.html', data)