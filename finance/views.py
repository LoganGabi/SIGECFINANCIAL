from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.forms import inlineformset_factory
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .models import *
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator
import pdb
from django.db import transaction
### CONTAS A PAGAR

@login_required
@transaction.atomic 
def Accounts_Create(request):
    dados = request.session.get('dados_temp')
    plannedAccount = request.GET.get("plannedAccount", 'false')
    verify = 0
    installments = []

    PaymentMethodAccountsFormSet = inlineformset_factory(
        Accounts,
        PaymentMethod_Accounts,
        form=PaymentMethodAccountsForm,
        extra=1, 
        can_delete=True,
    )

    if request.method == "POST":
        post_data = request.POST.copy()
        raw_data_planned_account = post_data.get('plannedAccount')

        if raw_data_planned_account:
            raw_date = post_data.get('date_init')
            if raw_date:
                try:
                    date_obj = datetime.strptime(raw_date, "%m/%Y")
                    completed_date = date_obj.replace(day=1).date()
                    post_data['date_init'] = completed_date.isoformat()
                    form_Accounts = AccountsFormPlannedAccount(post_data)
                except ValueError as e:
                    print("Erro ao tratar date_init", e)
                    form_Accounts = AccountsFormPlannedAccount(post_data)
        else:
            form_Accounts = AccountsForm(post_data)

        PaymentMethod_Accounts_FormSet = PaymentMethodAccountsFormSet(post_data)

        if form_Accounts.is_valid() and PaymentMethod_Accounts_FormSet.is_valid():
            account = form_Accounts.save()
            total_value = float(account.totalValue)

            # Processa cada parcela
            for form in PaymentMethod_Accounts_FormSet:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    parcela = float(form.cleaned_data['value'])
                    form.cleaned_data['value_old'] = parcela
                    verify += parcela
                    instance = form.save(commit=False)
                    instance.conta = account
                    instance.acc = True
                    instance.save()
                    installments.append(instance)

                    # Criar movimentação de caixa se necessário
                    payment = form.cleaned_data['forma_pagamento']
                    if payment.considerInCash and form.cleaned_data['expirationDate'] == today:
                        try:
                            caixa = CaixaDiario.objects.get(usuario_responsavel=request.user, is_Active=True)
                            CashMovement.objects.create(
                                cash=caixa,
                                accounts_in_cash=instance,
                                forma_pagamento=payment,
                                categoria='Saída'
                            )
                        except CaixaDiario.DoesNotExist:
                            form.add_error(None, "Usuário não possui um Caixa Diário ativo.")

            # Verifica se o total das parcelas bate com o valor total
            if verify == total_value:
                messages.success(request, "Conta criada com sucesso.", extra_tags="successAccount")
                return redirect('AccountsPayable')
            else:
                form_Accounts.add_error(None, 
                    f"O valor do somatório das parcelas ({verify}) é diferente do Valor Total ({total_value}).")

        # Se não for válido, exibe erros
        context = {
            'form_Accounts': form_Accounts,
            'form_payment_account': PaymentMethod_Accounts_FormSet,
            'Contas': 'Contas a Pagar',
            'tipo_conta': 'Pagar'
        }
        return render(request, 'finance/AccountsPayform.html', context)

    else:
        # GET request
        initial_data = {}
        referer = request.META.get('HTTP_REFERER', '')
        if dados and 'return_product' in referer:
            initial_data = {
                'description': dados.get('description'),
                'pessoa_id': dados.get('person'),
                'totalValue': dados.get('totalValue')
            }

        if plannedAccount != 'false':
            initial_data['plannedAccount'] = plannedAccount
            form_Accounts = AccountsFormPlannedAccount(initial=initial_data)
        else:
            form_Accounts = AccountsForm(initial=initial_data)

        PaymentMethod_Accounts_FormSet = PaymentMethodAccountsFormSet(queryset=PaymentMethod_Accounts.objects.none())

    context = {
        'form_Accounts': form_Accounts,
        'form_payment_account': PaymentMethod_Accounts_FormSet,
        'Contas': 'Contas a Pagar',
        'tipo_conta': 'Pagar'
    }
    return render(request, 'finance/AccountsPayform.html', context)

# funcionando
@login_required
def AccountsPayable_list(request):
    # Obtenha o termo de pesquisa da requisição
    search_query = request.GET.get('query', '')
 

    # Filtrar os clientes com base no termo de pesquisa
    if search_query:
        account = PaymentMethod_Accounts.objects.filter(
        (   # campo pessoa
           (
                Q(id__icontains=search_query) | 
                Q(conta__pessoa_id__id_FisicPerson_fk__name__icontains=search_query) | 
                Q(conta__pessoa_id__id_LegalPerson_fk__name_foreigner__icontains=search_query) | 
                Q(conta__pessoa_id__id_ForeignPerson_fk__fantasyName__icontains=search_query) | 
                Q(documentNumber__icontains=search_query)
            ) & ( Q(conta__is_active = True))
        ),
        conta__acc = True
       
    ).order_by('id')
    else:
        account = PaymentMethod_Accounts.objects.filter(
            (Q(conta__is_active = True)),
            acc = True).order_by('id') 

    paginator = Paginator(account, 20)  
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'finance/AccountsPay_list.html', {
        'accounts': page,
        'query': search_query,  # Envie o termo de pesquisa para o template
        'ContasP' : 'Contas a Pagar'
    })

# funcionando
@login_required
def get_Accounts(request, id_Accounts):
    paymentMethod_Accounts = PaymentMethod_Accounts.objects.get(id=id_Accounts,acc=True)
    client = {
    'pessoa_id':paymentMethod_Accounts.conta.pessoa_id,
    'chartOfAccounts': paymentMethod_Accounts.conta.chartOfAccounts,
    'documentNumber':paymentMethod_Accounts.conta.documentNumber,
    'date_account':paymentMethod_Accounts.conta.date_account,
    'numberOfInstallments': paymentMethod_Accounts.conta.numberOfInstallments,
    'installment_Range':paymentMethod_Accounts.conta.installment_Range,
    'date_init':paymentMethod_Accounts.conta.date_init,
    'totalValue':paymentMethod_Accounts.conta.totalValue,
    'peopleWatching':paymentMethod_Accounts.conta.peopleWatching,
    'systemWatching':paymentMethod_Accounts.conta.systemWatching,
    'forma_pagamento':paymentMethod_Accounts.forma_pagamento,
    'expirationDate':paymentMethod_Accounts.expirationDate,
    'value':paymentMethod_Accounts.value,
    'value_old':paymentMethod_Accounts.value_old,
    'interest':paymentMethod_Accounts.interest,
    'fine':paymentMethod_Accounts.fine,
    }
        
    return render(request, 'finance/AccountsPay_GET.html', {'client': client})

@login_required
@transaction.atomic 
def update_Accounts(request, id_Accounts):
    payment_instance = get_object_or_404(PaymentMethod_Accounts, id=id_Accounts)
    if payment_instance.conta:
        accounts_instance = get_object_or_404(Accounts, id=payment_instance.conta_id)
        print('accounts_instance', accounts_instance)
        if request.method == "POST":  
            payment_form_instance = PaymentMethodAccountsForm(request.POST, instance=payment_instance)
            accounts_form_instance = AccountsFormUpdate(
                request.POST, 
                instance=accounts_instance,
                initial={
                    'numberOfInstallments': accounts_instance.numberOfInstallments,
                    'installment_Range': accounts_instance.installment_Range,
                    'totalValue': accounts_instance.totalValue,
                    'date_init': accounts_instance.date_init
                }
            )
            for key, value in vars(payment_instance).items(): 
                print(f"{key}: {value}")
            print()
            # for key, value in vars(accounts_instance).items():
            #     print(f"{key}: {value}")
            # print()

            if payment_form_instance.is_valid() and accounts_form_instance.is_valid():
                accounts_form_instance.save()

                payment_instance = payment_form_instance.save(commit=False)

                # Definir None para valores vazios
                if not payment_instance.interest:
                    payment_instance.interest = None
                if not payment_instance.fine:
                    payment_instance.fine = None

                payment_instance.acc = True
                payment_instance.save()
                messages.success(request,"Conta atualizada com sucesso.",extra_tags="successAccount")
                return redirect('AccountsPayable')  # Redirecionar após salvar
            else:
                print("Erros no payment_form_instance:", payment_form_instance.errors)
                print()
                print("Erros no accounts_form_instance:", accounts_form_instance.errors)
                print()


        else:
            accounts_form_instance = AccountsFormUpdate(instance=accounts_instance)
            payment_form_instance = PaymentMethodAccountsFormUpdate(instance=payment_instance)

        context = {
            'form_Accounts': accounts_form_instance,
            'form_paymentMethodAccounts': payment_form_instance,
            'tipo_conta': 'Receber'
        }

        return render(request, 'finance/AccountsPayformUpdate.html', context)


# funcionando
@login_required
@transaction.atomic 
def delete_Accounts(request, id_Accounts):
    # Recupera o accounte com o id fornecido
    account_deleta_pelo_amor_De_Deus = PaymentMethod_Accounts.objects.filter(id=id_Accounts,acc = True).delete()
    messages.success(request,"Conta deletada com sucesso.",extra_tags="successAccount") 
    return redirect('AccountsPayable')

### CONTAS A RECEBER

from datetime import datetime, date
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect

from .models import Accounts, PaymentMethod_Accounts, CaixaDiario, CashMovement, PaymentMethod
from .forms import AccountsForm, AccountsFormPlannedAccount, PaymentMethodAccountsForm

today = date.today()
@login_required
@transaction.atomic
def AccountsReceivable_Create(request):
    plannedAccount = request.GET.get("plannedAccount", 'false')
    verify = 0
    installments = []

    PaymentMethodAccountsFormSet = inlineformset_factory(
        Accounts,
        PaymentMethod_Accounts,
        form=PaymentMethodAccountsForm,
        extra=1,
        can_delete=True
    )

    if request.method == "POST":
        post_data = request.POST.copy()
        raw_data_planned_account = post_data.get('plannedAccount')

        if raw_data_planned_account:
            raw_date = post_data.get('date_init')
            if raw_date:
                try:
                    date_obj = datetime.strptime(raw_date, "%m/%Y")
                    completed_date = date_obj.replace(day=1).date()
                    post_data['date_init'] = completed_date.isoformat()
                    form_Accounts = AccountsFormPlannedAccount(post_data)
                except ValueError as e:
                    print("Erro ao tratar date_init", e)
                    form_Accounts = AccountsFormPlannedAccount(post_data)
        else:
            form_Accounts = AccountsForm(post_data)

        PaymentMethod_Accounts_FormSet = PaymentMethodAccountsFormSet(post_data)

        if form_Accounts.is_valid() and PaymentMethod_Accounts_FormSet.is_valid():
            account = form_Accounts.save()
            total_value = account.totalValue

            for form in PaymentMethod_Accounts_FormSet:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    parcela = form.cleaned_data['value']
                    form.cleaned_data['value_old'] = parcela
                    verify += parcela
                    form_instance = form.save(commit=False)
                    installments.append(form_instance)

                    payment = form.cleaned_data['forma_pagamento']
                    print(form.cleaned_data['expirationDate'])
                    print(today)
                    # Criar movimentação de caixa se necessário
                  
            # Verifica se o total das parcelas bate com o valor total
            if float(verify) == float(total_value):
                for installment in installments:
                    installment.conta = account
                    installment.acc = False
                    installment.save()
                    if payment.considerInCash and installment.expirationDate == today:
                        try:
                            caixa = CaixaDiario.objects.get(usuario_responsavel=request.user, is_Active=True)
                        except CaixaDiario.DoesNotExist:
                            form.add_error(None, "Usuário não possui um Caixa Diário ativo.")
                            continue
                        CashMovement.objects.create(
                            cash=caixa,
                            accounts_in_cash=form_instance,
                            forma_pagamento=payment,
                            categoria='Entrada'
                        )


                messages.success(request, "Conta cadastrada com sucesso.", extra_tags="successAccount")
                return redirect('AccountsReceivable')
            else:
                form_Accounts.add_error(None,
                                        f"O valor do somatório das parcelas ({verify}) é diferente do Valor Total ({total_value}).")
            
        # Caso algum formulário não seja válido, exibir erros
        context = {
            'form_Accounts': form_Accounts,
            'form_payment_account': PaymentMethod_Accounts_FormSet,
            'Contas': 'Contas a Receber',
            'tipo_conta': 'Receber'
        }
        return render(request, 'finance/AccountsPayform.html', context)

    else:
        # GET request
        if plannedAccount == 'false':
            form_Accounts = AccountsForm()
        else:
            initial_data = {'plannedAccount': plannedAccount}
            form_Accounts = AccountsFormPlannedAccount(initial=initial_data)

        PaymentMethod_Accounts_FormSet = PaymentMethodAccountsFormSet(queryset=PaymentMethod_Accounts.objects.none())

    context = {
        'form_Accounts': form_Accounts,
        'form_payment_account': PaymentMethod_Accounts_FormSet,
        'Contas': 'Contas a Receber',
        'tipo_conta': 'Receber'
    }

    return render(request, 'finance/AccountsPayform.html', context)


@login_required
def AccountsReceivable_list(request):
    # Obtenha o termo de pesquisa da requisição
    search_query = request.GET.get('query', '') 

    # Filtrar os accountes com base no termo de pesquisa
    if search_query:
        account = PaymentMethod_Accounts.objects.filter(
        (   # campo pessoa
            (
                Q(id__icontains=search_query) | 
                Q(conta__pessoa_id__id_FisicPerson_fk__name__icontains=search_query) | 
                Q(conta__pessoa_id__id_LegalPerson_fk__name_foreigner__icontains=search_query) | 
                Q(conta__pessoa_id__id_ForeignPerson_fk__fantasyName__icontains=search_query) | 
                Q(documentNumber__icontains=search_query)
            ) & ( Q(conta__is_active=True))     
        ),
        acc = False 
    ).order_by('id')
    else:
        account = PaymentMethod_Accounts.objects.filter(
            (Q(conta__is_active = True)),
            acc = False).order_by('id') 

    # Configure o Paginator com o queryset filtrado
    paginator = Paginator(account, 20) 
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'finance/AccountsPay_list.html', {
        'accounts': page,
        'query': search_query,  # Envie o termo de pesquisa para o template
        'ContasR' : 'Contas a Receber'

    })


# funcionando
@login_required
def get_AccountsReceivable(request, id_Accounts):
    paymentMethod_Accounts = PaymentMethod_Accounts.objects.get(id=id_Accounts,acc=False)
    client = {
    'pessoa_id':paymentMethod_Accounts.conta.pessoa_id,
    'chartOfAccounts': paymentMethod_Accounts.conta.chartOfAccounts,
    'documentNumber':paymentMethod_Accounts.conta.documentNumber,
    'date_account':paymentMethod_Accounts.conta.date_account,
    'numberOfInstallments': paymentMethod_Accounts.conta.numberOfInstallments,
    'installment_Range':paymentMethod_Accounts.conta.installment_Range,
    'date_init':paymentMethod_Accounts.conta.date_init,
    'totalValue':paymentMethod_Accounts.conta.totalValue,
    'peopleWatching':paymentMethod_Accounts.conta.peopleWatching,
    'systemWatching':paymentMethod_Accounts.conta.systemWatching,
    'forma_pagamento':paymentMethod_Accounts.forma_pagamento,
    'expirationDate':paymentMethod_Accounts.expirationDate,
    'value':paymentMethod_Accounts.value,
    'value_old':paymentMethod_Accounts.value_old,
    'interest':paymentMethod_Accounts.interest,
    'fine':paymentMethod_Accounts.fine,
    }
    
        
    return render(request, 'finance/AccountsPay_GET.html', {'client': client})

@login_required
@transaction.atomic 
def update_AccountsReceivable(request, id_Accounts):
    payment_instance = get_object_or_404(PaymentMethod_Accounts, id=id_Accounts)
    if payment_instance.conta:
        accounts_instance = get_object_or_404(Accounts, id=payment_instance.conta_id)
        print('accounts_instance', accounts_instance)
        if request.method == "POST":  
            payment_form_instance = PaymentMethodAccountsForm(request.POST, instance=payment_instance)
            accounts_form_instance = AccountsFormUpdate(
                request.POST, 
                instance=accounts_instance,
                initial={
                    'numberOfInstallments': accounts_instance.numberOfInstallments,
                    'installment_Range': accounts_instance.installment_Range,
                    'totalValue': accounts_instance.totalValue,
                    'date_init': accounts_instance.date_init
                }
            )
            for key, value in vars(payment_instance).items(): 
                print(f"{key}: {value}")

            if payment_form_instance.is_valid() and accounts_form_instance.is_valid():
                accounts_form_instance.save()

                payment_instance = payment_form_instance.save(commit=False)

                # Definir None para valores vazios
                if not payment_instance.interest:
                    payment_instance.interest = None
                if not payment_instance.fine:
                    payment_instance.fine = None


                payment_instance.save()
                messages.success(request,"Conta atualizada com sucesso.",extra_tags="successAccount")
                return redirect('AccountsReceivable')  # Redirecionar após salvar
            else:
                print("Erros no payment_form_instance:", payment_form_instance.errors)
                print()
                print("Erros no accounts_form_instance:", accounts_form_instance.errors)
                print()


        else:
            accounts_form_instance = AccountsFormUpdate(instance=accounts_instance)
            payment_form_instance = PaymentMethodAccountsFormUpdate(instance=payment_instance)

        context = {
            'form_Accounts': accounts_form_instance,
            'form_paymentMethodAccounts': payment_form_instance,
            'tipo_conta': 'Receber'
        }
        return render(request, 'finance/AccountsPayformUpdate.html', context)
# funcionando

@login_required
@transaction.atomic 
def delete_AccountsReceivable(request, id_Accounts):
    # Recupera o accounte com o id fornecido
    messages.success(request,"Conta deletada com sucesso.",extra_tags="successAccount")
    account_deleta_pelo_amor_De_Deus = PaymentMethod_Accounts.objects.filter(id=id_Accounts,acc = False).delete() #filter(acc = False)
    return redirect('AccountsReceivable')




@login_required
@transaction.atomic 
def Accounts_list(request,id_accounts):
   
    conta = Accounts.objects.filter(pessoa_id=id_accounts)
    
    accounts = PaymentMethod_Accounts.objects.filter(
        (Q (conta__in = conta) ) 
        & Q(activeCredit = True) 
        )
    
    return render(request,'finance/ClientAccounts.html',{
        'accounts':accounts
    })
# CreditedClients.html

@login_required
@transaction.atomic
def deletePayment_Accounts(request,id):
    PaymentMethod_Accounts.objects.filter(id=id).delete()
    return JsonResponse({"message": "Pagamento deletado com sucesso!"}, status=200)

@login_required
def Cash_registry(request):
    if request.method == "POST":
        cash = CaixaDiarioForm(request.POST)
        if cash.is_valid():
            bank = cash.cleaned_data['bank']
            user = CaixaDiario.objects.filter(
                usuario_responsavel=request.user,
                is_Active=True,
                bank=bank
            )
            if user.exists():
                messages.error(request, f"Já existe um Caixa aberto para {request.user.username} nesse banco.")
                return redirect('Cash_list')

            caixa = cash.save(commit=False)
            caixa.usuario_responsavel = request.user
            caixa.is_Active = True
            caixa.saldo_final = caixa.saldo_inicial
            caixa.save()

            messages.success(request, 'Caixa aberto com sucesso!')
            return redirect('Cash_list')
    else:
        cash = CaixaDiarioForm()

    context = {
        'cash': cash,
    }
    return render(request, 'finance/cash_form.html', context)


@login_required
def Cash_list(request):
    cash = CaixaDiario.objects.filter(is_Active=1).order_by('-id')

    paginator = Paginator(cash, 20)  
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'cash': page,
    }

    return render(request, 'finance/cash_list.html', context)

@login_required
@transaction.atomic 
def cashFlow(request):
    cashMovement = CashMovement.objects.filter(
        Q(cash__usuario_responsavel=request.user),
        Q(cash__is_Active = 1)
    )
    
    context = {
        'CashMovement': cashMovement
    }
    return render(request, 'finance/cashFlow.html', context)

def cashFlow(request,pk):
    

def cash_close(request,pk):
    cash = get_object_or_404(CaixaDiario,pk = pk)
    cash.is_Active = False
    cash.save()

    return redirect('Cash_list')
