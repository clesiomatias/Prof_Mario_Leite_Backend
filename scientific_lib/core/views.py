from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import ArquivoForm
from .models import Arquivos


@login_required
def upload_arquivo(request):
    if request.method == 'POST':
        form = ArquivoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(
                "upload_sucesso"
            )  # Redirecione para a página de sucesso após o upload
    else:
        form = ArquivoForm()
    return render(request, 'upload_arquivo.html', {'form': form})

@login_required
def upload_sucesso(request):
    return render(request, "upload_sucesso.html")

def Home_View(request):    
    arquivos = Arquivos.objects.all()
    return render(request, 'home.html', {'arquivos': arquivos})


@login_required
def enviar_email_suporte(request):
    if request.method == "POST":        
        assunto = "Solicitação de Suporte"
        mensagem = "Por favor, descreva o problema ou a solicitação de suporte aqui."
        remetente = "seu@email.com"
        destinatario = ["clesiofmatias@email.com"]
        send_mail(assunto, mensagem, remetente, destinatario)
        return HttpResponseRedirect(reverse("pagina_sucesso"))
    else:
        return HttpResponseRedirect(reverse("pagina_erro"))
