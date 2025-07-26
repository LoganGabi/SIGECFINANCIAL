# your_app/signals.py

from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission
from django.apps import AppConfig, apps
from django.contrib.contenttypes.models import ContentType

def add_permissions(sender, **kwargs):
    
    def grant_all_permissions_to_manager():
        gerente_group, _ = Group.objects.get_or_create(name="gerente")
        all_permissions = Permission.objects.all()
        gerente_group.permissions.set(all_permissions)
        gerente_group.save()

    grant_all_permissions_to_manager()
    
    grupos_permissoes = {
        # "auxiliar_administrativo": [
        #     ("finance", "accounts", ["add", "change", "delete", "view"]),
        #     ("finance", "paymentmethod_accounts", ["add", "change", "delete", "view"]),
        #     ("registry", "address", ["add", "change"]),
        #     ("registry", "fisicperson", ["add", "change"]),
        #     ("registry", "foreignperson", ["add", "change"]),
        #     ("registry", "legalperson", ["add", "change"]),
        #     ("registry", "person", ["add", "change"]),
        # ],
        # "caixa": [
        #     ("finance", "accounts", ["add", "change", "delete", "view"]),
        #     ("finance", "paymentmethod_accounts", ["add", "change", "delete", "view"]),
        # ],
        # "estoquista": [
        #     ("purchase", "compra", ["add", "change", "delete", "view"]),
        #     ("purchase", "product", ["add", "change", "delete", "view"]),
        # ],
        # "lider_de_patio": [
        #     ("registry", "address", ["add", "change"]),
        #     ("registry", "fisicperson", ["add", "change"]),
        #     ("registry", "foreignperson", ["add", "change"]),
        #     ("registry", "legalperson", ["add", "change"]),
        #     ("registry", "person", ["add", "change"]),
        # ],
        # "vendedor": [
        #     ("registry", "address", ["add", "change"]),
        #     ("registry", "fisicperson", ["add", "change"]),
        #     ("registry", "foreignperson", ["add", "change"]),
        #     ("registry", "legalperson", ["add", "change"]),
        #     ("registry", "person", ["add", "change"]),
        #     ("sale", "venda", ["add", "change", "delete", "view"]),
        #     ("sale", "vendaitem", ["add", "change", "delete", "view"]),
        # ],
        ## feito por klei a partir da linha 53
        "Cadastro uma Pessoas": [
            ("registry", "address", ["add"]),
            ("registry", "fisicperson", ["add"]),
            ("registry", "foreignperson", ["add"]),
            ("registry", "legalperson", ["add"]),
            ("registry", "person", ["add"]),
        ],
        "Editar uma Pessoas": [
            ("registry", "address", ["change"]),
            ("registry", "fisicperson", ["change"]),
            ("registry", "foreignperson", ["change"]),
            ("registry", "legalperson", ["change"]),
            ("registry", "person", ["change"]),
        ],
        "Visualizar uma Pessoas": [
            ("registry", "address", ["view"]),
            ("registry", "fisicperson", ["view"]),
            ("registry", "foreignperson", ["view"]),
            ("registry", "legalperson", ["view"]),
            ("registry", "person", ["view"]),
        ],
        "Deletar uma Pessoas": [
            ("registry", "address", ["delete"]),
            ("registry", "fisicperson", ["delete"]),
            ("registry", "foreignperson", ["delete"]),
            ("registry", "legalperson", ["delete"]),
            ("registry", "person", ["delete"]),
        ],
        "Cadastro de Produtos": [
            ("purchase", "product", ["add"]),
        ],
        "Editar um Produto": [
            ("purchase", "product", ["change"]),
        ],
        "Visualizar um Produtos": [
            ("purchase", "product", ["view"]),
        ],
        "Deletar um Produtos": [
            ("purchase", "product", ["delete"]),
        ],
        "Criar Compras": [
            ("purchase", "compra", ["add"]),
            ("purchase", "product", ["add"]),
        ],
        "Editar uma Compra": [
            ("purchase", "compra", ["change"]),
            ("purchase", "product", ["change"]),
        ],
        "Visualizar uma Compra": [
            ("purchase", "compra", ["view"]),
            ("purchase", "product", ["view"]),
        ],
        "Deletar uma Compra": [
            ("purchase", "compra", ["delete"]),
            ("purchase", "product", ["delete"]),
        ],
        "Criar uma Venda": [
            ("sale", "venda", ["add"]),
            ("sale", "vendaitem", ["add"]),
            ("sale", "paymentmethodvenda", ["add"]),
        ],
        "Editar uma Venda": [
            ("sale", "venda", ["change"]),
            ("sale", "vendaitem", ["change"]),
            ("sale", "paymentmethodvenda", ["change"]),
        ],
        "Visualizar uma Venda": [
            ("sale", "venda", ["view"]),
            ("sale", "vendaitem", ["view"]),
            ("sale", "paymentmethodvenda", ["view"]),
        ],
        "Deletar uma Venda": [
            ("sale", "venda", ["delete"]),
            ("sale", "vendaitem", ["delete"]),
            ("sale", "paymentmethodvenda", ["delete"]),
        ],
        "Criar uma Ordem de Serviço": [
            ("service", "vendaservice", ["add"]),
            ("service", "vendaitemservice", ["add"]),
            ("service", "vendaitem", ["add"]),
            ("service", "paymentmethodvendaservice", ["add"]),
        ],
        "Editar uma Ordem de Serviço": [
            ("service", "vendaservice", ["change"]),
            ("service", "vendaitemservice", ["change"]),
            ("service", "vendaitem", ["change"]),
            ("service", "paymentmethodvendaservice", ["change"]),
        ],
        "Visualizar uma Ordem de Serviço": [
            ("service", "vendaservice", ["view"]),
            ("service", "vendaitemservice", ["view"]),
            ("service", "vendaitem", ["view"]),
            ("service", "paymentmethodvendaservice", ["view"]),
        ],
        "Ordem de Serviço": [
            ("service", "vendaservice", ["delete"]),
            ("service", "vendaitemservice", ["delete"]),
            ("service", "vendaitem", ["delete"]),
            ("service", "paymentmethodvendaservice", ["delete"]),
        ],
        "Cadastrar uma Situação": [
            ("config", "situation", ["add"]),
        ],
        "Editar uma Situação": [
            ("config", "situation", ["change"]),
        ],
        "Visualizar uma Situação": [
            ("config", "situation", ["view"]),
        ],
        "Deletar uma Situação": [
            ("config", "situation", ["delete"]),
        ],
        "Criar uma Conta": [
            ("finance", "accounts", ["add"]),
            ("finance", "paymentmethodaccounts", ["add"]),
        ],
        "Editar uma Conta": [
            ("finance", "accounts", ["change"]),
            ("finance", "paymentmethodaccounts", ["change"]),
        ],
        "Visualizar uma Conta": [
            ("finance", "accounts", ["view"]),
            ("finance", "paymentmethodaccounts", ["view"]),
        ],
        "Deletar uma Contas": [
            ("finance", "accounts", ["delete"]),
            ("finance", "paymentmethodaccounts", ["delete"]),
        ],
        "Cadastrar uma Forma de Pagamento": [
            ("config", "paymentmethod", ["add"]),
        ],
        "Editar uma Forma de Pagamento": [
            ("config", "paymentmethod", ["change"]),
        ],
        "Visualizar uma Forma de Pagamento": [
            ("config", "paymentmethod", ["view"]),
        ],
        "Deletar uma Forma de Pagamento": [
            ("config", "paymentmethod", ["delete"]),
        ],
        "Cadastrar um Serviço": [
            ("config", "service", ["add"]),
        ],
        "Editar um Serviço": [
            ("config", "service", ["change"]),
        ],
        "Visualizar um Serviço": [
            ("config", "service", ["view"]),
        ],
        "Deletar um Serviço": [
            ("config", "service", ["delete"]),
        ],
        "Cadastrar um Plano de Contas": [
            ("config", "chartofacounts", ["add"]),
        ],
        "Editar um Plano de Contas": [
            ("config", "chartofacounts", ["change"]),
        ],
        "Visualizar um Plano de Contas": [
            ("config", "chartofacounts", ["view"]),
        ],
        "Deletar um Plano de Contas": [
            ("config", "chartofacounts", ["delete"]),
        ],
        "Adicionar Permissões": [
            ("auth", "group", ["add"]),
            ("auth", "permission", ["add"]),
        ],
        "Editar Permissões": [
            ("auth", "group", ["change"]),
            ("auth", "permission", ["change"]),
        ],
        "Visualizar Permissões": [
            ("auth", "group", ["view"]),
            ("auth", "permission", ["view"]),
        ],
        "Deletar Permissões": [
            ("auth", "group", ["delete"]),
            ("auth", "permission", ["delete"]),
        ],
        "Caixa": [
            ("finance", "caixadiario", ["add", "view"]),
            ("finance", "cashmovement", ["add", "change", "view"]),
            ("finance", "FechamentoCaixa", ["add", "view"]),
        ],
        "Credito": [
            ("finance", "accounts", ["view"]),
            ("registry", "person", ["change", "view"]),
        ],
    }

    for grupo_nome, permissoes in grupos_permissoes.items():
        grupo, created = Group.objects.get_or_create(name=grupo_nome)
        for app_label, model, actions in permissoes:
            try:
                content_type = ContentType.objects.get(app_label=app_label, model=model)
                for action in actions:
                    codename = f"{action}_{model}"
                    permission = Permission.objects.filter(codename=codename, content_type=content_type).first()
                    if permission:
                        grupo.permissions.add(permission)
                        print(f"✅ Permissão '{codename}' adicionada ao grupo '{grupo_nome}'.")
                    else:
                        print(f"⚠️ Permissão '{codename}' não encontrada para '{app_label}.{model}'.")
            except ContentType.DoesNotExist:
                print(f"⚠️ ContentType não encontrado: '{app_label}.{model}'")
                
post_migrate.connect(add_permissions)