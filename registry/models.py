from django.db import models
from django.contrib.auth.models import User
from functools import partial
from auditlog.registry import auditlog
from auditlog.models import AuditlogHistoryField

class Address(models.Model):
    cep = models.CharField('CEP', max_length=10)
    road = models.CharField('rua', max_length=100)
    number = models.PositiveIntegerField('numero da casa' )
    neighborhood = models.CharField('Bairro', max_length=100)
    reference = models.CharField('Ponto de Referencia', max_length=100, null=True, blank=True)
    complement = models.CharField('Complemento', max_length=100, null=True, blank=True)
    city = models.CharField('cidade', max_length=100)
    uf = models.CharField('UF', max_length=2)
    country = models.CharField('país', max_length=100)
    historico = AuditlogHistoryField()
    def __str__(self):
        return f"{self.road}, {self.number}, {self.city}"

class FisicPerson(models.Model):
    name = models.CharField('Nome', max_length=100)
    cpf = models.CharField('Cadastro de Pessoa Fisica - CPF', max_length=100)
    rg = models.CharField('Registro Geral - RG', max_length=100)
    dateOfBirth = models.CharField('Data de Aniversario', max_length=14)
    historico = AuditlogHistoryField() 

    def __str__(self):
        return self.name

class ForeignPerson(models.Model):
    name_foreigner = models.CharField('Nome', max_length=100)
    num_foreigner = models.CharField('Numero do Documento', max_length=100)
    historico = AuditlogHistoryField()

    def __str__(self):
        return self.name_foreigner

class LegalPerson(models.Model):
    fantasyName = models.CharField('Nome Fantasia', max_length=100)
    cnpj = models.CharField('CNPJ', max_length=100)
    socialReason = models.CharField('Razão Social', max_length=100)
    StateRegistration = models.CharField('Inscrição Estadual', max_length=100)
    typeOfTaxpayer = models.CharField('Tipo de Contribuinte', max_length=100)
    MunicipalRegistration = models.CharField('Inscrição Municipal', max_length=100)
    suframa = models.CharField('SUFRAMA', max_length=100)
    Responsible = models.CharField('Responsavel', max_length=100)
    historico = AuditlogHistoryField()

    def __str__(self):
        return self.fantasyName
    
class Person(models.Model):
    WorkPhone = models.CharField('Telefone de Trabalho', max_length=100)
    PersonalPhone = models.CharField('Telefone Pessoal', max_length=100)
    isActive = models.BooleanField('isActive', max_length=100)
    site = models.CharField('site', max_length=100,null=True, blank=True) 
    salesman = models.CharField('Vendedor', max_length=100,null=True, blank=True)
    creditLimit = models.DecimalField('Limite de Crédito', max_length=100, decimal_places=2, max_digits=10,default=0)
    email = models.EmailField('E-mail', max_length=128, null=True, blank=True) 
    password = models.CharField('Senha', max_length=128, null=True, blank=True) 

    isClient = models.BooleanField("Cliente",null=True, blank=True)
    isSupllier = models.BooleanField("Fornecedor",null=True, blank=True)
    isUser = models.BooleanField("Usuario do Sistema",null=True, blank=True)
    isEmployee = models.BooleanField("Funcionario",null=True, blank=True)
    issalesman = models.BooleanField("Vendedor",null=True, blank=True)
    isFormer_employee = models.BooleanField("Ex-Funcionario",null=True, blank=True)
    isCarrier = models.BooleanField("Transportadora",null=True, blank=True)
    isDelivery_man = models.BooleanField("Entregador",null=True, blank=True)
    isTechnician = models.BooleanField("Tecnico",null=True, blank=True)
 
    id_FisicPerson_fk = models.OneToOneField ('FisicPerson', on_delete=models.SET_NULL,null=True, blank=True, db_column='id_FisicPerson_fk')
    id_LegalPerson_fk = models.OneToOneField ('LegalPerson', on_delete=models.SET_NULL,null=True, blank=True, db_column='id_LegalPerson_fk')
    id_ForeignPerson_fk = models.OneToOneField ('ForeignPerson', on_delete=models.SET_NULL,null=True, blank=True, db_column='id_ForeignPerson_fk')
    id_address_fk = models.OneToOneField ('Address', on_delete=models.CASCADE, db_column='id_address_fk')
    id_user_fk = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, db_column='id_user_fk')
    
    historico = AuditlogHistoryField()

    def __str__(self):
        if self.id_FisicPerson_fk != None:
            return self.id_FisicPerson_fk.name
        elif self.id_LegalPerson_fk != None:
            return self.id_LegalPerson_fk.fantasyName
        elif self.id_ForeignPerson_fk != None:
            return self.id_ForeignPerson_fk.name_foreigner
        else:
            return None



auditlog.register(Address)
auditlog.register(FisicPerson)
auditlog.register(ForeignPerson)
auditlog.register(LegalPerson)
auditlog.register(Person)
