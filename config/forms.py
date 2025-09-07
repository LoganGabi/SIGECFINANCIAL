from django import forms
from .models import *
from django.contrib.auth.models import Permission, User, Group



class ChartOfAccountsModelForm(forms.ModelForm):
    class Meta:
        
        model = ChartOfAccounts
        fields = ['name_ChartOfAccounts', 'father', 'natureOfTheAccount']
        widgets = {
            'name_ChartOfAccounts' : forms.TextInput(
                attrs = {
                    'class':'form-control'
                }
            ),
            'father':forms.Select(
                attrs={
                    'class':'form-select ' 
                }
            ),
            'natureOfTheAccount':forms.Select(
                attrs={
                    'class':'form-select ' 
                }
            ),
            # 'natureOfTheAccount' : forms.ChoiceField(choices=NatureOfTheAccount, label='Natureza da Conta')
        }

    def __init__(self, *args, **kwargs):
        super(ChartOfAccountsModelForm, self).__init__(*args, **kwargs)
        self.fields['name_ChartOfAccounts'].widget.attrs.update({'class': 'label-text'})

class PaymentMethodModelForm(forms.ModelForm):
    # ativo = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    
    class Meta:
        model = PaymentMethod
        fields = ['name_paymentMethod','creditPermission', 'considerInCash','bank']
        widgets = {
            'considerInCash' : forms.CheckboxInput(attrs={
                'class':'form-check-input'
                }),
            'creditPermission':forms.CheckboxInput(attrs={
                'class':'form-check-input'
                })
        } 

    def __init__(self, *args, **kwargs): 
        super(PaymentMethodModelForm, self).__init__(*args, **kwargs)
        self.fields['name_paymentMethod'].widget.attrs.update({'class': 'label-text'})

class BankModelForm(forms.ModelForm):
    # ativo = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    
    class Meta:
        model = Bank
        fields = ['bank_name','agencia', 'conta']

    def __init__(self, *args, **kwargs): 
        super(BankModelForm, self).__init__(*args, **kwargs)
        self.fields['bank_name'].widget.attrs.update({'class': 'label-text'})
        self.fields['agencia'].widget.attrs.update({'class': 'label-text'})
        self.fields['conta'].widget.attrs.update({'class': 'label-text'})

class PositionModelForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['name_position']

    def __init__(self, *args, **kwargs):
        super(PositionModelForm, self).__init__(*args, **kwargs)
        self.fields['name_position'].widget.attrs.update({'class': 'label-text'})


class PermsForm(forms.ModelForm):
    class Meta:
        model = Permission
        fields = '__all__'
        # exclude = ['name','codename'] 
        widgets = {
            # 'name': forms.
        }

class UserPermissionAssignForm(forms.ModelForm): # Renomeei para clareza
    def label_from_instance(self, obj):
        modules_perms = {
            'Pessoa':{
                'address':'Endereço',
                'fisic person':'Pessoal Fisica',
                'foreign person':'Estrangeiro',
                'legal person':'Pessoa Juridica',
                'person':'Dados Gerais de Pessoa',
            },
            'Product':{
                'Product':'Produtos',
                'person':'Dados Gerais de Pessoa',
                },
            'Purchase':{
                'Product':'Produtos',
                'compra item':'Compras',
                'compra item':'Itens Presentes em Compras',
                },
            'accounts':{
                'accounts':'Contas',
                'accounts':'Contas',
                'accounts':'Contas',
                'accounts':'Contas',
                },
            'registry':'Cadastro',
            'sale':'Venda',
            'service':'Serviço',
            }
        # modules_name = {
        #     'Config':'Configuração',
        #     'Finance':'Financeiro',
        #     'Purchase':'Compras',
        #     'registry':'Cadastro',
        #     'sale':'Venda',
        #     'service':'Serviço',
        #     }
        # modules_perms = {
        #     'Config':'Configuração',
        #     'Finance':'Financeiro',
        #     'Purchase':'Compras',
        #     'registry':'Cadastro',
        #     'sale':'Venda',
        #     'service':'Serviço',
        #     }
        # models = {
        #     'chart of accounts':'Plano de Contas',
        #     'payment method':'Forma de Pagamento',
        #     'position':'Cargo',
        #     'service':'Serviço',
        #     'situation':'Situação',
        #     'accounts':'Contas',
        #     'caixa diario':'Caixa Diario',
        #     'cash movement':'Movimentação de Caixa',
        #     'fechamento de caixa':'Fechamento de Caixa',
        #     'paypayment method_ accounts':'Forma de Pagamento de Contas',
        #     '':'',
        # }

        # obj é uma instância do modelo Permission
        # O método __str__ padrão de Permission retorna algo como:
        # f"{obj.content_type.app_label} | {obj.content_type.model} | {obj.name}"

        # Você pode retornar o que quiser aqui. Exemplos:
        # return f"{obj.name}"  # Apenas o nome legível da permissão
        # return f"Permissão: {obj.name.upper()} (App: {obj.content_type.app_label})"
        # return f"Código: {obj.codename}" # Se quiser mostrar o codename
        
        # Exemplo de transformação simples (como um "pipe" faria):
        return obj.name.replace("Can ", "").capitalize() # Ex: "add user" -> "Add user"

    
    # user_permissions = forms.ModelMultipleChoiceField(
    #     queryset=Permission.objects.filter(content_type_id__gte = 7).order_by('content_type__app_label', 'content_type__model', 'name'),
    #     widget=forms.CheckboxSelectMultiple, # ISSO GERA OS CHECKBOXES
    #     required=False,
    #     label="Atribuir Permissões ao Usuário"
    # )

    group = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget = forms.CheckboxSelectMultiple,
        label='Selecione as Permissões'
    )

    class Meta:
        model = Group # O formulário é para um Usuário
        fields = ['group'] # O campo que queremos editar no Usuário

    # Este formulário, quando instanciado com um objeto User,
    # mostrará todas as permissões como checkboxes,
    # e as permissões que o usuário já possui virão marcadas.

class PermissionMultipleSelectForm(forms.Form):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Permissões"
    )

