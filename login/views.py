from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.forms import inlineformset_factory
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from finance.models import Accounts, PaymentMethod_Accounts
from .forms import *
from .models import *
from config.models import Log, Info_logs
from datetime import datetime
from django.utils  import timezone
from django.conf import settings
from django.core.paginator import Paginator
from datetime import date, timedelta
from django.db import transaction
from django.forms.models import model_to_dict
from django import forms
from auditlog.models import LogEntry
from django.contrib.contenttypes.models import ContentType
import os
import json
import glob
import logging

def create_log(msg:str ,name:str):
    """
    Parâmetros Para Criar o Log no Sistema

    msg: mensagem que voce quer adicionar ao Log

    name: Nome da Pasta para onde o log será inserido
    """

    date_time = datetime.now().strftime("%d/%m/%Y as %H:%M:%S")

    now = datetime.now()
    year = now.year
    month = now.month

    # Define o semestre
    semestre = 'S1' if month <= 6 else 'S2'

    # Define diretório e nome fixo do arquivo baseado no semestre
    dir = os.path.join('login', 'log', name)
    os.makedirs(dir, exist_ok=True)
    name_arq = f"log_{year}_{semestre}.json"
    caminho_completo = os.path.join(dir, name_arq)
    if not os.path.exists(caminho_completo):
        with open(caminho_completo, "w") as f:
            f.write(f"Arquivo criado em {date_time}\n")

    if os.path.exists(caminho_completo):
        with open(caminho_completo, 'r', encoding='utf-8') as f:
            try:
                dados = json.load(f)
            except json.JSONDecodeError:
                dados = {}
    else:
        dados = {}

    # Determina o próximo número de chave
    proximo_id = len(dados) + 1
    chave = f"{proximo_id}"  # Ex: "01", "02", etc.  "proximo_id:010" deixa 10 digitos no log

    # Adiciona e salva
    dados[chave] = msg

    with open(caminho_completo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def log_db(request, action:str ,type:str):
    """
    type: tipo de modulo ou ação usada numerado entre 1 a 13

    01 : pessoa

    02 : produtos

    03 : compras

    04 : vendas

    05 : ordem de serviço

    06 : contas a pagar

    07 : contas a receber

    08 : formas de pagamento

    09 : situação

    10 : plano de contas

    11 : serviços

    12 : Login

    13 : logout

    action: conjunto de caracteres descrevendo o que foi feito no log

    e : Login

    s : Logout

    c : Create

    r : Read
    
    u : Update
    
    d : Delete
    """
    try:
        with transaction.atomic():
            log = Log.objects.create(
                user=request.user,
                date=timezone.now(),
                action=action,
                type=type
            )
            return log
            
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error("Erro ao salvar log de auditoria", exc_info=True)

def log_create_db(log, info_old:str=''):
    """
    Realiza o registro de atualização de informações no sistema de logs.
     
    É estritamente necessário informar os campos abaixo na ordem correta.

    Args:
        log (Log): Objeto principal do log.null=False
        info_old (str): Informação antiga cadastrada. null=False
    Returns:
        None
    """
    try:
        with transaction.atomic():
            log_info = Info_logs.objects.create(
                log_principal=log,
                info_old=info_old
            )
        return log_info
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error("Erro ao salvar log de auditoria", exc_info=True)

def log_upd_db(log, **kwargs:dict):
    """
    Realiza o registro de atualização de informações no sistema de logs.
     
    É estritamente necessário informar os campos abaixo na ordem correta.

    dicionario contendo as informações abaixo na seguinte estrutura 
    
    { field: {'antes': info_old, 'depois': info_now} }

    Args:
        log (Log): Objeto principal do log.null=False
        info_old (str): Informação antiga cadastrada. null=False
        info_now (str): Informação nova para update. null=True
        field (str or list): Nome do campo (ou campos) que foi modificado. null=False

    Returns:
        None
    """
    try:
        with transaction.atomic():
            for chave, valor in kwargs.items():
                print(f"\n\n\n\n{kwargs}\n\n\n\n")
                
                if kwargs[valor]['depois']:
                    log_info = Info_logs.objects.create(
                        log_principal=log,
                        info_old=kwargs[valor]['antes'],
                        info_now=kwargs[valor]['depois'],
                        field=chave,
                )
                else:
                    log_info = Info_logs.objects.create(
                        log_principal=log,
                        info_old=kwargs[chave]['antes'],
                    )
        return log_info
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error("Erro ao salvar log de auditoria", exc_info=True)

def compair(obj_antigo, obj_novo):
    """
    Compara os campos de dois objetos Django (um antigo e um novo)
    e retorna um dicionário com os campos que foram alterados.

    Args:
        obj_antigo: O objeto Django antes da alteração (estado original do banco de dados).
        obj_novo: O objeto Django com as alterações propostas (ex: vindo de um formulário).

    Returns:
        Um dicionário onde as chaves são os nomes dos campos alterados
        e os valores são dicionários contendo o valor 'antes' e 'depois' da alteração.
        Ex: {'nome_campo': {'antes': 'valor_antigo', 'depois': 'valor_novo'}}
        Retorna um dicionário vazio se não houver alterações.
    """
    # Transforma o objeto antigo em dicionário
    antigo_dict = model_to_dict(obj_antigo)

    # if obj is not None:
    #     pass

    # Detecta o tipo do segundo argumento
    if isinstance(obj_novo, forms.ModelForm) :
        if obj_novo.is_valid():
            novo_dict = obj_novo.cleaned_data
        else:
            raise ValueError(f"Formulário inválido: {obj_novo.errors}")
    else:
        novo_dict = model_to_dict(obj_novo)         # instância do modelo

    campos_alterados = {}

    for campo, valor_antigo in antigo_dict.items():
        if campo == "id":
            continue

        if campo in novo_dict and valor_antigo != novo_dict[campo]:
            campos_alterados[campo] = {
                "antes": valor_antigo,
                "depois": novo_dict[campo],
            }
        elif campo not in novo_dict:
            campos_alterados[campo] = {
                "antes": valor_antigo,
                "depois": "Campo removido",
            }

    return campos_alterados

def my_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            #DADOS PARA ADICIONAR O LOG JONSON
            log = log_db(request, action='e', type='12')
            log_create_db(log, info_old='Entrou no Sistema',)
            return redirect('index')
        
    return render(request, 'login/login.html')

@login_required
def my_logout(request):
    #DADOS PARA ADICIONAR O LOG JSON FIXME
    create_log(
        msg = f'O Usuario {request.user.username} saiu no sistema no dia {datetime.now().strftime("%d/%m/%Y as %H:%M:%S")}',
        name = 'log_entrada')
    log = log_db(request, action='s', type='13')
    log_create_db(log, info_old='Saiu do Sistema',)
    logout(request)
    return redirect('index') 

@login_required
def notifications(request):
    today = date.today()
    results = []
    # print("DIA ATUAL: ",today)
    
    for i in range(0,365):
        target_date = today + timedelta(days=i)
        # print(target_date)
        pagamentos = PaymentMethod_Accounts.objects.filter(expirationDate=target_date)
        for pagamento in pagamentos:
            results.append({
                'date':target_date,
                'remainsDays':i,
                'idPayment':pagamento.id
            })
    return JsonResponse({'notifications':results})

@login_required
def index(request):
    return render(request, 'login/index.html')

#Listagem De Loggs

@login_required
def log_entry(request):
    terms = "alguma coisa"
    if request.method == "POST":
        page_obj = Info_logs.objects.filter(user__icontains=terms)
        pass
    else:
        page_obj = Info_logs.objects.all()
    
    context = {
    'page_obj': page_obj, 
    }
    return render(request, 'login/log_entry.html',context)

@login_required
def log(request):
    terms = ""
    if request.method == "POST":
        page_obj = LogEntry.objects.filter(user__icontains=terms)
        pass
    else:
        page_obj = LogEntry.objects.all()
    
    paginator = Paginator(page_obj, 20)  # 20 itens por página
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    # changeId = page_obj.changes['id'][1]
    # print(changeId)
    # for log in LogEntry.objects.all():
    #     content_type = ContentType.objects.get(id=log.content_type_id)
    #     print(content_type.model)         # Ex: "cliente"
    #     print(content_type.app_label)    # Ex: "meu_app"
    #     print(content_type.model_class())  # Ex: <class 'meu_app.models.Cliente'>
            
    # page_obj = page(request,page_obj)
    
    # 'changes':changeId,
    context = {
    'page_obj': page,
    }
    return render(request, 'login/log_entry.html',context)

@login_required
def log_detailed(request, log_id):
    page_obj = LogEntry.objects.get(id=log_id)
    context = {

    'page_obj': page_obj,
    }
    return render(request, 'login/log_detailed.html',context)

@login_required
def log_service(request):
    
    # Pega todos os arquivos da pasta (ignora subpastas)
    arquivos = glob.glob(os.path.join(settings.BASE_DIR,'login','log','log_ordem_de_servico', '*'))

    # Filtra apenas arquivos (caso tenha pastas)
    arquivos = [f for f in arquivos if os.path.isfile(f)]
    logs = {} 
    if arquivos:
        ultimo_arquivo = max(arquivos, key=os.path.getctime)

        with open(ultimo_arquivo, 'r', encoding='utf-8') as arquivo_json:
            logs = json.load(arquivo_json)

    page_obj = page(request,logs)
    
    context = {
    'page_obj': page_obj,
    }
    return render(request, 'login/log_entry.html',context)

@login_required
def log_accounts(request):
    
    # Pega todos os arquivos da pasta (ignora subpastas)
    arquivos = glob.glob(os.path.join(settings.BASE_DIR,'login','log','log_contas', '*'))

    # Filtra apenas arquivos (caso tenha pastas)
    arquivos = [f for f in arquivos if os.path.isfile(f)]
    logs = {} 
    if arquivos:
        ultimo_arquivo = max(arquivos, key=os.path.getctime)

        with open(ultimo_arquivo, 'r', encoding='utf-8') as arquivo_json:
            logs = json.load(arquivo_json)

    page_obj = page(request,logs)
    
    context = {
    'page_obj': page_obj,
    }
    return render(request, 'login/log_entry.html',context)

@login_required
def log_config(request):
    
    # Pega todos os arquivos da pasta (ignora subpastas)
    arquivos = glob.glob(os.path.join(settings.BASE_DIR,'login','log','log_config', '*'))

    # Filtra apenas arquivos (caso tenha pastas)
    arquivos = [f for f in arquivos if os.path.isfile(f)]
    logs = {} 
    if arquivos:
        ultimo_arquivo = max(arquivos, key=os.path.getctime)

        with open(ultimo_arquivo, 'r', encoding='utf-8') as arquivo_json:
            logs = json.load(arquivo_json)

    page_obj = page(request,logs)
    
    context = {
    'page_obj': page_obj,
    }
    return render(request, 'login/log_entry.html',context)

@login_required
def log_permitions(request):
    
    # Pega todos os arquivos da pasta (ignora subpastas)
    arquivos = glob.glob(os.path.join(settings.BASE_DIR,'login','log','log_permissoes', '*'))

    # Filtra apenas arquivos (caso tenha pastas)
    arquivos = [f for f in arquivos if os.path.isfile(f)]
    logs = {} 
    if arquivos:
        ultimo_arquivo = max(arquivos, key=os.path.getctime)

        with open(ultimo_arquivo, 'r', encoding='utf-8') as arquivo_json:
            logs = json.load(arquivo_json)

    page_obj = page(request,logs)
    
    context = {
    'page_obj': page_obj,
    }
    return render(request, 'login/log_entry.html',context)

@login_required
def log_dlog(request):
    
    # Pega todos os arquivos da pasta (ignora subpastas)
    arquivos = glob.glob(os.path.join(settings.BASE_DIR,'login','log','log_de_log', '*'))

    # Filtra apenas arquivos (caso tenha pastas)
    arquivos = [f for f in arquivos if os.path.isfile(f)]
    logs = {} 
    if arquivos:
        ultimo_arquivo = max(arquivos, key=os.path.getctime)

        with open(ultimo_arquivo, 'r', encoding='utf-8') as arquivo_json:
            logs = json.load(arquivo_json)

    page_obj = page(request,logs)
    
    context = {
    'page_obj': page_obj,
    }
    return render(request, 'login/log_entry.html',context)

def page(request,logs):
    # Converte o dicionário em lista de tuplas
    logs_lista = list(logs.items())  # [('0001', 'desc1'), ('0002', 'desc2'), ...]

    # Cria o paginator — define quantos itens por página (ex.: 10)
    paginator = Paginator(logs_lista, 5)

    # Pega o número da página da URL ?page=2
    page_number = request.GET.get('page')

    # Pega os itens da página atual
    page_obj = paginator.get_page(page_number)
    return page_obj
    