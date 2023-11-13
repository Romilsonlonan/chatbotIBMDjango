import django.http
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import auth

def register(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/chatbot')
        return render(request, "bases/register.html")
    elif request.method == 'POST':
        # Obtém os dados do formulário
        username = request.POST.get('username')
        email = request.POST.get('email')
        contatos = request.POST.get('contatos')

        """
        esse código garante que todos os campos (username, email e contatos) sejam preenchidos 
        antes de prosseguir com o processamento dos dados. Se algum deles estiver vazio, o 
        usuário receberá uma mensagem de erro e será redirecionado de volta para a página 
        de registro para corrigir o problema.
        """
        if username is not None and email is not None and contatos is not None:
            if len(username.strip()) == 0 or len(email.strip()) == 0 or len(contatos.strip()) == 0:
                messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
                return redirect("/auth/register")
        else:
            messages.add_message(request, constants.ERROR, 'Erro nos dados recebidos')
            return redirect("/auth/register")

        usuario = User.objects.filter(username = username)

        try:
            # Cria um novo usuário
            novo_usuario = User.objects.create_user(
                username=username,
                email=email,
        
            )

            # Adiciona os contatos (se necessário)
            novo_usuario.contatos = contatos
            novo_usuario.save()
        
            # Mensagem de sucesso
            messages.add_message(request, constants.SUCCESS, 'Obrigado por interagir conosco! ') 
            return redirect("/auth/chatbot")  # Substitua pelo username da sua rota do chatbot

        except Exception as e:
            # Mensagem de erro
            messages.add_message(request, constants.ERROR, 'Erro interno, repita novamente!')
            return render(request, '/auth/register')
        else:
            auth.chatbot(request, usuario)
    return redirect("/auth/chatbot")





