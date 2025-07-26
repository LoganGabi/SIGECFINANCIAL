from django.db import models
from registry.models import Person
from django.db import transaction
from django.contrib.auth.models import User, Group
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import Permission
from auditlog.registry import auditlog
from auditlog.models import AuditlogHistoryField

class Bank(models.Model):
    bank_name = models.CharField(verbose_name='Nome do Banco', max_length=250)
    agencia =  models.CharField(verbose_name='Agencia do Banco', max_length=250, null=True, blank=True)
    conta =  models.CharField(verbose_name='Conta', max_length=250, null=True, blank=True)
    is_Active = models.BooleanField('ativo', default=True)
    value_in_bank = models.IntegerField(verbose_name='valor arrecadado no banco',default=0)
    
    def __str__(self):
        return self.bank_name

class PaymentMethod(models.Model):
    # CONSIDERINCASH = [
    #     ('entrada', 'Entrada'),
    #     ('saida', 'Saída'),

    # ]
    name_paymentMethod = models.CharField('Nome da Forma de Pagamento', max_length=50)
    creditPermission = models.BooleanField('creditPermission',default=False)
    is_Active = models.BooleanField('ativo',default=True) 
    considerInCash = models.BooleanField('considerar em caixa', default=False, blank=True, null=True) 
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, verbose_name='Banco que recebe a Forma de Pagamento')
    # considerInCash = models.CharField('considerar em caixa',choices= CONSIDERINCASH, default=False, blank=True, null=True, max_length=50)
    is_Active = models.BooleanField('ativo', default=True) 

    def __str__(self):
        return self.name_paymentMethod

class ChartOfAccounts(models.Model): 
    NatureOfTheAccount = [
            ('E', 'Entrada'),
            ('S', 'Saída'),
        ]

    code = models.CharField(max_length=20, unique=True, blank=True, verbose_name='Codigo de Conta')
    name_ChartOfAccounts = models.CharField('Nome do Plano de Contas', max_length=50)
    father = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='filhos', #onde os filhos vão receber o id do pai 
        verbose_name='Referente a'
    )
    natureOfTheAccount =  models.CharField(
        max_length=1,
        choices=NatureOfTheAccount,
        default='E',
        verbose_name='Natureza da Conta'
    )
    is_Active = models.BooleanField('ativo',default=True)
    historico = AuditlogHistoryField()

    def save(self, *args, **kwargs):
        if not self.code:
            with transaction.atomic():  # evita conflito em ambiente concorrente
                #se o plano de contas ja estiver uma linha pai 
                if self.father:
                    lastson = ChartOfAccounts.objects.filter(father=self.father).order_by('-code').first()
                    if lastson:
                        #cria uma lista que divide o plano de contas em subniveis
                        newlastson = lastson.code.split(".")
                        # pega o ultimo item da lista e incrementa adicionando 1 ao valor do item da lista
                        # deixando ele sempre com 3 digitos
                        newlastson[-1] = str(int(newlastson[-1]) + 1).zfill(3)
                        self.code = '.'.join(newlastson)
                    else: # se nao tiver nenhum filho é criado o primeiro
                        self.code = f'{self.father.code}.001'
                else: # se for a raiz do plano de contas
                    roots = ChartOfAccounts.objects.filter(father__isnull=True)
                    if roots.exists():
                        # pega o ultimo codigo do plano de contas e adiciona '1' para o novo plano de contas
                        last_code = roots.order_by('-code').first().code
                        self.code = str(int(last_code) + 1)
                    else:
                        self.code = '1'

        super().save(*args, **kwargs)


    def __str__(self):
        return f'{self.code} - {self.name_ChartOfAccounts}'
    
class Position(models.Model): #desativado
    name_position = models.CharField('Nome do Cargo', max_length=25)
    is_Active = models.BooleanField('ativo',default=True)
    
    def __str__(self):
        return self.name_position
 

class GroupSetBackend(ModelBackend):
    def get_group_permissions(self, user_obj, obj=None):
        if not user_obj.is_active or user_obj.is_anonymous:
            return set()

        permissions = set()

        # Permissões dos grupos normais
        permissions.update(super().get_group_permissions(user_obj, obj))

        # Permissões dos grupos agrupados (GroupSet)
        group_sets = user_obj.groupset_set.all()
        for group_set in group_sets:
            for group in group_set.groups.all():
                perms = group.permissions.values_list(
                    "content_type__app_label", "codename"
                ).order_by()
                permissions.update(
                    ["%s.%s" % (ct, name) for ct, name in perms]
                )

        return permissions

class Log(models.Model):
    """
    user: usuario presente na requisição " request.user "

    date: data atual do log " datetime.now().strftime("%d/%m/%Y as %H:%M:%S") "

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
    """
    CHOICES_LOG_TYPE = {
        ('01','pessoa'),
        ('02','produtos'),
        ('03','compras'),
        ('04','vendas'),
        ('05','ordem de serviço'),
        ('06','contas a pagar'),
        ('07','contas a receber'),
        ('08','formas de pagamento'),
        ('09','situação'),
        ('10','plano de contas'),
        ('11','serviços'),
        ('12','Login'),
        ('13','logout'),

    }
    CHOICES_LOG = {
        ('e','login'),
        ('s','logout'),
        ('c','create'),
        ('r','read'),
        ('u','update'),
        ('d','delete')
    }

    user = models.ForeignKey(User, verbose_name='Usuario', on_delete=models.CASCADE)
    date = models.DateTimeField( auto_created=True, verbose_name="data e hora do log")
    # action = models.CharField(max_length=255, null=False, blank=False, verbose_name="Ação feita pelo usuario")

    type = models.CharField(max_length=2, choices=CHOICES_LOG_TYPE, verbose_name='tipo de transação')
    action = models.CharField(max_length=1, choices=CHOICES_LOG, verbose_name='tipo de transação')

class Info_logs(models.Model):
    """
    log_principal: id do log principal

    info_old: informação antiga cadastrada

    info_now: Informação nova para update

    field: nome do campo que foi modificado
    """

    log_principal = models.ForeignKey(Log, verbose_name='log principal', on_delete=models.CASCADE)

    info_old = models.CharField(max_length=255, null=False, blank=False, verbose_name="Informação antiga")
    info_now = models.CharField(max_length=255, null=True, blank=False, verbose_name="Informação atual")
    field = models.CharField(max_length=255, null=True, blank=False, verbose_name="nome do campo")
   


auditlog.register(PaymentMethod)
auditlog.register(ChartOfAccounts)



