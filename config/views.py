from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.forms import inlineformset_factory
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .models import *
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from .forms import PermissionMultipleSelectForm
from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin # Para segurança


### PAYMENT METHOD
@login_required
def paymentMethod(request):
    context = {
        'PaymentMethods': PaymentMethod.objects.filter(is_Active=True)
    }
    return render(request, 'config/PaymentMethod.html', context)

@login_required
@transaction.atomic
def PaymentMethodForm(request):
    if request.method == "GET":
        if 'HTTP_REFERER' in request.META:
            request.session['previous_page'] = request.META['HTTP_REFERER']
        paymentMethodForm = PaymentMethodModelForm()
        context = {
            'paymentMethod' : paymentMethodForm
        }
        return render(request, 'config/PaymentMethodForm.html', context)
    else:
        paymentMethodForm = PaymentMethodModelForm(request.POST)
         # SALVA O LINK DA PAGINA ANTERIOR
        previous_url = request.session.get('previous_page','/')
        if paymentMethodForm.is_valid():
            paymentMethodForm.save()
            messages.success(request, "Forma de Pagamento cadastrada com sucesso.",extra_tags="successPayment")
            return redirect(previous_url)
    context = {
        'paymentMethod' : paymentMethodForm
    }
    return render(request, 'config/PaymentMethod.html', context)

@login_required  
@transaction.atomic  
def updatePaymentMethod(request, id_paymentMethod):
    paymentMethod = get_object_or_404(PaymentMethod, id=id_paymentMethod)
    if request.method == "GET":
        paymentMethodForm = PaymentMethodModelForm(instance=paymentMethod)

        context = {
            'PaymentMethod': paymentMethod,
            'paymentMethod': paymentMethodForm
        }
        return render(request, 'config/PaymentMethodForm.html',context)
    elif request.method == "POST":
        paymentMethodForm = PaymentMethodModelForm(request.POST, instance=paymentMethod)
        if paymentMethodForm.is_valid():
            paymentMethodForm.save()
            messages.success(request, "Forma de Pagamento atualizada com sucesso.",extra_tags="successPayment")
            return redirect('PaymentMethod')
    context = {
        'PaymentMethod' : paymentMethodForm
    }
    return render(request, 'config/PaymentMethod.html', context)

@login_required
@transaction.atomic
def deletePaymentMethod(request, id_paymentMethod):
    paymentMethod = get_object_or_404(PaymentMethod, id=id_paymentMethod)
    if request.method == "POST":
        paymentMethod.is_Active = False
        paymentMethod.save()
        messages.success(request, "Forma de Pagamento deletada com sucesso.",extra_tags="successPayment")
        return redirect('PaymentMethod')  
    context = {
        'paymentMethod': paymentMethod
    }

    return render(request, 'config/PaymentMethod.html', context)

### POSITION
@login_required
def position(request):
    context = {
        'Positions': Position.objects.filter(is_Active=True)
    }
    return render(request, 'config/Position.html', context)


@login_required
@transaction.atomic
def PositionForm(request):
    if request.method == "GET":
        PositionForm = PositionModelForm()
        context = {
            'Position' : PositionForm
        }
        return render(request, 'config/PositionForm.html', context)
    else:
        PositionForm = PositionModelForm(request.POST)
        if PositionForm.is_valid():
            PositionForm.save()
            messages.success(request, "Cargo cadastrado com sucesso.",extra_tags='successPosition')
            return redirect('Position')
    context = {
        'Position' : PositionForm
    }
    return render(request, 'config/Position.html', context)

@login_required
@transaction.atomic
def updatePosition(request, id_position):
    position = get_object_or_404(Position, id=id_position)
    if request.method == "GET":
        positionForm = PositionModelForm(instance=position)

        context = {
            'position': position,
            'Position': positionForm
        }
        return render(request, 'config/PositionForm.html',context)
    elif request.method == "POST":
        positionForm = PositionModelForm(request.POST, instance=position)
        if positionForm.is_valid():
            positionForm.save()
            messages.success(request, "Cargo atualizado com sucesso.",extra_tags='successPosition')
            return redirect('Position')
    context = {
        'Position' : positionForm
    }
    return render(request, 'config/Position.html', context)

@login_required
@transaction.atomic
def deletePosition(request, id_position):
    position = get_object_or_404(Position, id=id_position)
    if request.method == "POST":
        position.is_Active = False
        position.save()
        messages.success(request, "Cargo deletado com sucesso.",extra_tags="successPosition")
        return redirect('Position')  
    context = {
        'position': position
    }

    return render(request, 'config/Position.html', context)

### SITUATION



### ChartOfAccounts

@login_required
def chartOfAccounts(request):
    context = {
        # 'ChartOfAccounts': ChartOfAccounts.objects.filter(is_Active=True)
        'ChartOfAccounts': ChartOfAccounts.objects.all()
    }
    return render(request, 'config/ChartOfAccounts.html', context)

@login_required
@transaction.atomic
def ChartOfAccountsForm(request):
    if request.method == "GET":
        chartOfAccountsForm = ChartOfAccountsModelForm()
        context = {
            'ChartOfAccounts' : chartOfAccountsForm
        }
        return render(request, 'config/ChartOfAccountsForm.html', context)
    else:
        chartOfAccountsForm = ChartOfAccountsModelForm(request.POST)
        if chartOfAccountsForm.is_valid():
            chartOfAccountsForm.save()
            messages.success(request, "Plano de Contas cadastrado com sucesso.",extra_tags='successChartOfAccounts')
            return redirect('ChartofAccounts')
        else:
            print('Erros:',chartOfAccountsForm.errors)
    context = {
        'ChartOfAccounts' : chartOfAccountsForm
    }
    return render(request, 'config/ChartOfAccounts.html', context)

@login_required
@transaction.atomic
def updateChartOfAccounts(request, id_chartOfAccounts):
    chartOfAccounts = get_object_or_404(ChartOfAccounts, id=id_chartOfAccounts)
    if request.method == "GET":
        chartOfAccountsForm = ChartOfAccountsModelForm(instance=chartOfAccounts)

        context = {
            'chartOfAccounts': chartOfAccounts,
            'ChartOfAccounts': chartOfAccountsForm
        }
        return render(request, 'config/ChartOfAccountsForm.html',context)
    elif request.method == "POST":
        chartOfAccountsForm = ChartOfAccountsModelForm(request.POST, instance=chartOfAccounts)
        if chartOfAccountsForm.is_valid():
            chartOfAccounts.code = ''
            chartOfAccountsForm.save()
            messages.success(request, "Plano de Contas atualizado com sucesso.",extra_tags='successChartOfAccounts')
            return redirect('ChartofAccounts')
    context = {
        'ChartOfAccounts' : chartOfAccountsForm
    }
    return render(request, 'config/ChartOfAccounts.html', context)

@login_required
@transaction.atomic
def disableChartOfAccounts(request, id_chartOfAccounts):
    chartOfAccounts = get_object_or_404(ChartOfAccounts, id=id_chartOfAccounts)
    if request.method == "POST":
        chartOfAccounts.is_Active = False
        chartOfAccounts.save()
        messages.success(request, "Plano de Contas desativado com sucesso.",extra_tags='successChartOfAccounts')
        return redirect('ChartofAccounts') 
    context = {
        'chartOfAccounts': chartOfAccounts
    }

    return render(request, 'config/ChartOfAccounts.html', context)

@login_required
@transaction.atomic
def ActiveChartOfAccounts(request, id_chartOfAccounts):
    chartOfAccounts = get_object_or_404(ChartOfAccounts, id=id_chartOfAccounts)
    if request.method == "POST":
        chartOfAccounts.is_Active = True
        chartOfAccounts.save()
        messages.success(request, "Plano de Contas ativado com sucesso.",extra_tags='successChartOfAccounts')
        return redirect('ChartofAccounts')  
    context = {
        'chartOfAccounts': chartOfAccounts
    }

    return render(request, 'config/ChartOfAccounts.html', context)




@login_required
def buscar_forma_pagamento(request):
    query = request.GET.get('query','').strip()
    page_num = request.GET.get('page,1')

    resultados = PaymentMethod.objects.filter(
        Q(id__istartswith=query)|
        Q(name_paymentMethod__istartswith=query)
    ).order_by('id')

    payments = [
        {
            'id': forma_pagamento.id,
            'name_paymentMethod':forma_pagamento.name_paymentMethod,
            'is_Active':forma_pagamento.is_Active
        } for forma_pagamento in resultados
    ]

    usuario_paginator = Paginator(payments,20)
    page = usuario_paginator.get_page(page_num)

    response_data = {
        'paymentsMethod':list(page.object_list),
        'pagination':{
            'has_previous':page.has_previous(),
            'previous_page':page.previous_page_number() if page.has_previous() else None,
            'has_next':page.has_next(),
            'next_page': page.next_page_number() if page.has_next() else None,
            'current_page': page.number,
            'total_pages': usuario_paginator.num_pages
        },
        'message':f"{len(payments)} Formas de Pagamento encontrados"
    }
    return JsonResponse(response_data)
   
@login_required
def teste_permissao(request):
    permissoes = Permission.objects.all()

    permissoes_formatadas = []
    for permissao in permissoes:
        full_codename = f"{permissao.content_type.app_label}.{permissao.codename}"
        tem_permissao = request.user.has_perm(full_codename)  # Verifica na view

        permissoes_formatadas.append({
            "nome": permissao.name,
            "codename": permissao.codename,
            "full_codename": full_codename,
            "tem_permissao": tem_permissao  # Passamos True/False para o template
        })

    return render(request, 'config/testePermissao.html', {"permissoes": permissoes_formatadas})

@login_required
def permitions_list(request):
    users = User.objects.exclude(id = request.user.id)
    context = {
        'users': users
    }
    return render(request, 'config/PermitionsList.html', context)

@login_required
def select_permissions(request, id=id):
    # def editperms(request, id=id):
    user = get_object_or_404(User,id=id)
    permitions = Permission.objects.all()
    if (request.method == 'POST'): 
        # Permissões enviadas pelo formulário
        permissoes_ids = request.POST.getlist('permissoes')
        novas_permissoes = Permission.objects.filter(id__in=permissoes_ids)

        # Remove todas as permissões diretas e adiciona as selecionadas
        user.user_permissions.set(novas_permissoes)

        return redirect('permitions_list')  # ou qualquer outra página que desejar

    else: 
        # users = user.get_all_permissions()
        # u = user.get_all_permissions()
        u = permitions
        users = UserPermissionAssignForm(instance=user)
        for i in u:
            print(i)
        print(type(u))

    # user = get_object_or_404(User, id=id)
    
    # if request.method == "POST":
    #     users = PermsForm(request.POST, instance=user)
    #     if users.is_valid():
    #         messages.success(request, f'Permissao do Usuario {user.username} atualizadas com Sucesso')
    #         return redirect('permitions_list')
    # else: 
    #     users = PermsForm(instance=user) 
    #     print(f'permissoes do usuario {user.get_all_permissions()}')
        # print(f'formulario de permissoes {users}')
    context = {
        'users': users,
        'perm': permitions,
    }
    return render(request, 'config/PermitionsForm.html', context) 

def editperms(request, id=id):
    # Organizar permissões por modelo
    content_types = ContentType.objects.all().order_by('app_label', 'model')
    grouped_permissions = {}

    for ct in content_types:
        perms = Permission.objects.filter(content_type=ct)
        if perms.exists():
            grouped_permissions[ct] = perms

    if request.method == 'POST':
        form = PermissionMultipleSelectForm(request.POST)
        if form.is_valid():
            selected_perms = form.cleaned_data['permissions']
            request.user.user_permissions.set(selected_perms)
            return render(request, 'success.html', {'perms': selected_perms})
    else:
        form = PermissionMultipleSelectForm()

    return render(request, 'config/PermitionsForm.html', {
        'form': form,
        'grouped_permissions': grouped_permissions
    })

### TESTE

@login_required
def bank(request):
    context = {
        'Banks': Bank.objects.filter(is_Active=True)
    }
    return render(request, 'config/Bank.html', context)

@login_required
@transaction.atomic
def BankForm(request):
    if request.method == "GET":
        if 'HTTP_REFERER' in request.META:
            request.session['previous_page'] = request.META['HTTP_REFERER']
        bankForm = BankModelForm()
        context = {
            'bank' : bankForm
        }
        return render(request, 'config/BankForm.html', context)
    else:
        bankForm = BankModelForm(request.POST)
         # SALVA O LINK DA PAGINA ANTERIOR
        previous_url = request.session.get('previous_page','/')
        if bankForm.is_valid():

            bankForm.save()
            messages.success(request, "Banco cadastrado com sucesso.",extra_tags="successBank")
            return redirect(previous_url)
    context = {
        'bank' : bankForm
    }
    return render(request, 'config/Bank.html', context)

@login_required  
@transaction.atomic  
def updateBank(request, id_bank):
    bank = get_object_or_404(Bank, id=id_bank)
    if request.method == "GET":
        bankForm = BankModelForm(instance=bank)

        context = {
            'Bank': bank,
            'bank': bankForm
        }
        return render(request, 'config/BankForm.html',context)
    elif request.method == "POST":
        bankForm = BankModelForm(request.POST, instance=bank)
        if bankForm.is_valid():
            bankForm.save()
            messages.success(request, "Forma de Pagamento atualizada com sucesso.",extra_tags="successPayment")
            return redirect('Bank')
    context = {
        'Bank' : bankForm
    }
    return render(request, 'config/Bank.html', context)

@login_required
@transaction.atomic
def deleteBank(request, id_bank):
    bank = get_object_or_404(Bank, id=id_bank)
    if request.method == "POST":
        bank.is_Active = False
        bank.save()
        messages.success(request, "Forma de Pagamento deletada com sucesso.",extra_tags="successPayment")
        return redirect('Bank')  
    context = {
        'bank': bank
    }

    return render(request, 'config/Bank.html', context)
