from django import forms
from .models import *

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = "__all__"
        widgets = {
            'road':forms.TextInput(attrs={
                'class':'form-control ',
                'placeholder':'Rua dos Operários'
            }),
            'number':forms.NumberInput(attrs={
                'class':'form-control w-number ',
                'placeholder':'0'
            }),
            'cep':forms.TextInput(attrs={
                'class':'form-control ',
                'onblur':"pesquisacep(this.value);",
                'mask-cep':"00000-000",
                'placeholder':"00000-000"
            }),
            'neighborhood':forms.TextInput(attrs={
                'class':'form-control ',
                'placeholder':'Belo Jardim'

            }),
             'reference':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Do lado da panificadora'
            }),
             'complement':forms.TextInput(attrs={
                'class':'form-control ',
                'placeholder':'Quarto 504'
            }),
             'city':forms.TextInput(attrs={
                'class':'form-control ',
                'placeholder':'Rio Branco'
            }),
             'uf':forms.TextInput(attrs={
                'class':'form-control ',
                'placeholder':'AC'
            }),
             'country':forms.TextInput(attrs={
                'class':'form-control ',
                'placeholder':'Ex: Brasil'
            })
        }

class LegalPersonModelForm(forms.ModelForm):
    class Meta:
        model = LegalPerson
        fields = ["fantasyName","cnpj","socialReason","StateRegistration","typeOfTaxpayer","MunicipalRegistration","suframa","Responsible"]
        widgets = {
            'fantasyName':forms.TextInput(attrs={
                'class':'form-control row'
            }),
            'cnpj':forms.TextInput(attrs={
                'class':'form-control row'
            }),
            'socialReason':forms.TextInput(attrs={
                'class':'form-control row'
            }),
            'StateRegistration':forms.TextInput(attrs={
                'class':'form-control row'
            }),
            'typeOfTaxpayer':forms.TextInput(attrs={
                'class':'form-control row'
            }),
            'MunicipalRegistration':forms.TextInput(attrs={
                'class':'form-control row'
            }),
            'suframa':forms.TextInput(attrs={
                'class':'form-control row'
            }),
            'Responsible':forms.TextInput(attrs={
                'class':'form-control row'
            })


        }

class ForeignerModelForm(forms.ModelForm):
    class Meta:
        model = ForeignPerson
        fields = ["name_foreigner","num_foreigner"]
        widgets = {
            'name_foreigner':forms.TextInput(attrs={
                'class':'form-control row'
            }),
            'num_foreigner':forms.TextInput(attrs={
                'class':'form-control row'
            })
        }

class FisicPersonForm(forms.ModelForm):
    class Meta:
        model = FisicPerson
        fields = ["name","cpf","rg","dateOfBirth"] 
        widgets = {
            'name':forms.TextInput(attrs={
                'class':'form-control row ',
                'placeholder':'Kleilson Colaço Leoncio Cezar'
            }),
            'cpf':forms.TextInput(attrs={
                'class':'form-control row mask-cpf ',
                'placeholder':'___.___.___-__'
            }),
            'rg':forms.TextInput(attrs={
                'class':'form-control row ',
                'placeholder':''
            }),
            'dateOfBirth':forms.DateInput(attrs={
                'class':'form-control row mask-date',
            })
        }

    
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.fields['dateOfBirth'].widget.attrs.update({'class': 'form-control row mask-date'})
        self.fields['cpf'].widget.attrs.update({'class': 'form-control row mask-cpf '})

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['WorkPhone', 
                  'PersonalPhone', 
                  'site', 'salesman', 
                  'creditLimit', 
                  'isClient', 
                  'isSupllier', 
                  'isUser', 
                  'isEmployee', 
                  'issalesman', 
                  'isFormer_employee', 
                  'isCarrier', 
                  'isDelivery_man', 
                  'isTechnician',
                  'email',
                  'password',
                  ] # 'isActive'

        widgets = {
            'WorkPhone':forms.TextInput(attrs={
                'class':'form-control row'
            }),
            'PersonalPhone':forms.TextInput(attrs={
                'class':'form-control row'
            }),
            'site':forms.TextInput(attrs={
                'class':'form-control row'
            }),
            'salesman':forms.TextInput(attrs={
                'class':'form-control row'
            }),
            'creditLimit':forms.NumberInput(attrs={
                'class':'form-control row',
                'min':0,
            }),
            'isClient':forms.CheckboxInput(attrs={
                'class':'form-check-input'}
            ),
            'isSupllier':forms.CheckboxInput(attrs={
                'class':'form-check-input'}
            ),
            'isUser':forms.CheckboxInput(attrs={
                'class':'form-check-input',
                'onchange':"mostrarCampos()"
                }
            ), 
            'isEmployee':forms.CheckboxInput(attrs={
                'class':'form-check-input'}
            ), 
            'issalesman':forms.CheckboxInput(attrs={
                'class':'form-check-input'}
            ), 
            'isFormer_employee':forms.CheckboxInput(attrs={
                'class':'form-check-input'}
            ), 
            'isCarrier':forms.CheckboxInput(attrs={
                'class':'form-check-input'}
            ), 
            'isDelivery_man':forms.CheckboxInput(attrs={
                'class':'form-check-input'}
            ), 
            'isTechnician':forms.CheckboxInput(attrs={
                'class':'form-check-input'}
            ),
            'email':forms.TextInput(attrs={
                'class':'form-control',
            }),
             'password':forms.PasswordInput(attrs={
                'class' : 'form-control ',
                # 'minlength' : '8',
                # 'type' : "password" 
            }),
        }

    
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        
class ClientSearchForm(forms.Form): 
    search = forms.CharField(max_length=100, required=False, label="Pesquisar Cliente")

