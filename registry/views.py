from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.forms import inlineformset_factory
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from .forms import *
from .models import *
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Case, When, Value, CharField, F
from operator import attrgetter
from config.models import Log, Info_logs
from datetime import datetime
from login.views import compair, log_db, log_upd_db, log_create_db



### CLIENT

@login_required
@transaction.atomic
def Client_Create(request):
    # import pdb;  pdb.set_trace()

    if request.method == "POST":
        # SALVA O LINK DA PAGINA ANTERIOR
        previous_url = request.session.get('previous_page', '/')

        form_address = AddressForm(request.POST)
        form_fisicPerson = FisicPersonForm(request.POST)
        form_legalPerson = LegalPersonModelForm(request.POST)
        form_foreigner = ForeignerModelForm(request.POST)
        form_Person = PersonForm(request.POST)

        # verificação e validação de endereço
        if form_address.is_valid():
            address = form_address.save()

        #verificação se o cadastro é valido 
        if form_Person.is_valid():
            log = log_db(request, action='c' ,type='01')

            person = form_Person.save(commit=False)
            person.id_address_fk = address
            person.isActive = 1

            # verificação em qual cadastro foi feito    
            if form_fisicPerson.is_valid():
                fisicPerson = form_fisicPerson.save(commit=False)
                # fisicPerson.id_address_fk = address
                fisicPerson = form_fisicPerson.save()

                # person = form_Person.save(commit=False)
                person.id_FisicPerson_fk = fisicPerson
                
                if person.email and person.password: 
                    person.id_user_fk = u
                    u = createUser(person.id_FisicPerson_fk.name, person.email, person.password)
                    log_create_db(log, info_old=f'Cadastrou o Usuario {person.id_FisicPerson_fk.name}')
                else:
                    log_create_db(log, info_old=f'Cadastrou a Pessoa {person.id_FisicPerson_fk.name}')
                
                person.save()

                messages.success(request,"Cliente cadastrado com sucesso.",extra_tags="successClient")
                return redirect(previous_url)

            if form_legalPerson.is_valid():
                legalPerson = form_legalPerson.save(commit=False)
                # legalPerson.id_address_fk = address
                legalPerson = form_legalPerson.save()

                # person = form_Person.save(commit=False)
                person.id_LegalPerson_fk = legalPerson
                if person.email and person.password: 
                    u = createUser(person.id_LegalPerson_fk.fantasyName, person.email, person.password)
                    person.id_user_fk = u
                    log_create_db(log, info_old=f'Cadastrou o Usuario {person.id_LegalPerson_fk.fantasyName}')
                else:
                    log_create_db(log, info_old=f'Cadastrou a Pessoa {person.id_LegalPerson_fk.fantasyName}')
                person.save()

                messages.success(request,"Cliente cadastrado com sucesso.",extra_tags="successClient")
                return redirect(previous_url)

            if form_foreigner.is_valid():
                foreigner = form_foreigner.save(commit=False)
                # foreigner.id_address_fk = address
                foreigner = form_foreigner.save()
                # person = form_Person.save(commit=False)
                person.id_ForeignPerson_fk = foreigner
                if person.email and person.password: 
                    create = createUser(person.id_ForeignPerson_fk.name_foreigner, person.email, person.password,)
                    
                    person.id_user_fk = create
                    log_create_db(log, info_old=f'Cadastrou o Usuario {person.id_ForeignPerson_fk.name_foreigner}')
                else:
                    log_create_db(log, info_old=f'Cadastrou a Pessoa {person.id_ForeignPerson_fk.name_foreigner}')
                    
                person.save()
                    
                messages.success(request,"Cliente cadastrado com sucesso.",extra_tags="successClient")
                return redirect(previous_url)
    else: 
        if 'HTTP_REFERER' in request.META:
            # SALVA A PAGINA ANTERIOR
            request.session['previous_page'] = request.META['HTTP_REFERER']
            print(request.session['previous_page'])
        

        form_address = AddressForm()
        form_fisicPerson = FisicPersonForm()
        form_legalPerson = LegalPersonModelForm()
        form_foreigner = ForeignerModelForm()
        form_Person = PersonForm()
        
    context = {
        'form_address': form_address,
        'form_fisicPerson': form_fisicPerson,
        'form_legalPerson': form_legalPerson,
        'form_foreigner': form_foreigner,
        'form_Person': form_Person,
        'selected_form':'Pessoa Física'
    }
    return render(request, 'registry/Clientform.html', context)

def createUser(*user):
    usuario = User.objects.create_user(
        username=user[0], 
        email=user[1],
        password=user[2],
        first_name=user[0]
        )
    return usuario

def updateUser(user, **form_user): #revisar
    if user:user_compair = compair(user,form_user)
    else:user_compair = {}
    return user_compair

@login_required
def client_list(request):
    # Obtenha o termo de pesquisa da requisição
    search_query = request.GET.get('query', '')
    sort = request.GET.get('sort')
    direction = request.GET.get('dir', 'asc')

    # Filtrar os clientes com base no termo de pesquisa
    
    if search_query:
        clients = Person.objects.annotate(
            nome_cliente = Case(
            When(id_FisicPerson_fk__name__isnull = False,then=F('id_FisicPerson_fk__name')),
            When(id_LegalPerson_fk__isnull=False, then=F('id_LegalPerson_fk__fantasyName')),
            When(id_ForeignPerson_fk__isnull=False, then=F('id_ForeignPerson_fk__name_foreigner')),
            default=Value(''),
            output_field=CharField()
            )
        ).filter(
            (
                Q(id__startswith=search_query) |
                Q(nome_cliente__istartswith=search_query)
            ) &
            Q(isActive = True),
        )
    else:
        clients = Person.objects.annotate(
            nome_cliente = Case(
                When(id_FisicPerson_fk__name__isnull = False,then=F('id_FisicPerson_fk__name')),
                When(id_LegalPerson_fk__isnull=False, then=F('id_LegalPerson_fk__fantasyName')),
                When(id_ForeignPerson_fk__isnull=False, then=F('id_ForeignPerson_fk__name_foreigner')),
                default=Value(''),
                output_field=CharField()
            )).filter(
                Q(isActive = True),
            )
        
    # Configure o Paginator com o queryset filtrado
    paginator = Paginator(clients, 20)  # 20 itens por página
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    page_items = list(page.object_list)

    foreign_keys = {
        'pessoa':'nome_cliente'
    }

    if sort:
        reverse = (direction == 'desc')
        if sort in foreign_keys:
            value = foreign_keys[sort]
            page_items = sorted(page_items,key=attrgetter(value), reverse=reverse)
        else:
            page_items = sorted(page_items,key=attrgetter(sort),reverse=reverse)

    page.object_list = page_items

    colunas = [
        ('id','ID'),
        ('pessoa','Pessoa')
    ]

    return render(request, 'registry/client_list.html', {
        'colunas':colunas,
        'clients': page,
        'query': search_query,  # Envie o termo de pesquisa para o template
        'current_sort':sort,
        'current_dir':direction
    })

@login_required
def buscar_clientes(request):
    # """Busca clientes dinamicamente, retorna dados paginados em JSON."""
    query = request.GET.get('query', '').strip()  # Recebe a entrada do usuário
    page_num = request.GET.get('page', 1)  # Número da página atual

    # Realiza a busca com base no termo de pesquisa
    resultados = Person.objects.filter(
        (
            Q(id__istartswith=query) | 
            Q(id_FisicPerson_fk__name__istartswith=query) | 
            Q(id_ForeignPerson_fk__name_foreigner__istartswith=query) | 
            Q(id_LegalPerson_fk__fantasyName__istartswith=query)
        )
        & Q(isActive = True)
    ).order_by('id')

    # Serializa os resultados em uma lista de dicionários
    clients = [
        {
            'id': cliente.id,
            'name': (
                cliente.id_FisicPerson_fk.name if cliente.id_FisicPerson_fk else 
                (cliente.id_ForeignPerson_fk.name_foreigner if cliente.id_ForeignPerson_fk else 
                (cliente.id_LegalPerson_fk.fantasyName if cliente.id_LegalPerson_fk else 'Nome não disponível'))),
            'WorkPhone': cliente.WorkPhone,
            'PersonalPhone': cliente.PersonalPhone,
        }
        for cliente in resultados
    ]

    # Paginação
    usuario_paginator = Paginator(clients, 2)  # 20 resultados por página
    page = usuario_paginator.get_page(page_num)

    # Constrói a resposta JSON
    response_data = {
        'clientes': list(page.object_list),
        'query':query,
        'pagination': {
            'has_previous': page.has_previous(),
            'previous_page': page.previous_page_number() if page.has_previous() else None,
            'has_next': page.has_next(),
            'next_page': page.next_page_number() if page.has_next() else None,
            'current_page': page.number,
            'total_pages': usuario_paginator.num_pages,
        },
        'message': f"{len(clients)} cliente(s) encontrado(s)" if page.object_list else "Nenhum cliente encontrado."
    }
    return JsonResponse(response_data)



@login_required
@transaction.atomic
def delete_client(request, id_client): #(FUNCIONANDO)
    # Recupera o cliente com o id fornecido
    client = get_object_or_404(Person, id=id_client)
    client.isActive = False
    client.save()
    log = Log.objects.create(
                user=request.user,
                date=datetime.now(),
                action='d',
                type='01'
            )
    if client.id_FisicPerson_fk:
        Info_logs.objects.create(log_principal=log, info_old=f'Inativou a Pessoa {client.id_FisicPerson_fk.name}')
    if client.id_ForeignPerson_fk:
        Info_logs.objects.create(log_principal=log, info_old=f'Inativou a Pessoa {client.id_ForeignPerson_fk.name_foreigner}')
    if client.id_LegalPerson_fk:
        Info_logs.objects.create(log_principal=log, info_old=f'Inativou a Pessoa {client.id_LegalPerson_fk.fantasyName}')
    messages.success(request,"Cliente deletado com sucesso.",extra_tags="successClient")
    return redirect('Client')

