from django import template

register = template.Library()

@register.filter(name="has_perm")
def has_perm(user, perm_name):
    """Verifica se o usuário tem uma permissão específica."""
    return user.has_perm(perm_name)

    #FIXME - Esse filtro (pipe) verifica através da própria API do Django se o usuário tem uma permissão específica.
    #FIXME - O Django possui um sistema de permissões e grupos de usuários.

@register.filter(name='entrada_saida')
def entrada_saida(value):
    if value == 'E':
        return 'Entrada'
    elif value == 'S':
        return 'Saída' 

@register.filter(name='custom_name')
def custom_name(value):
    
    NOME_AMIGAVEL_CAMPOS = {
        'cep' : 'CEP', 
        'road' : 'rua', 
        'number' : 'numero da casa',
        'neighborhood' : 'Bairro', 
        'reference' : 'Ponto de Referencia', 
        'complement' : 'Complemento', 
        'city' : 'cidade',
        'uf' : 'UF', 
        'country' : 'país', 
        'name' : 'Nome',
        'cpf' : 'Cadastro de Pessoa Fisica - CPF',
        'rg' : 'Registro Geral - RG',
        'dateOfBirth' : 'Data de Aniversario',
        'name_foreigner' : 'Nome',
        'num_foreigner' : 'Numero do Documento',
        'fantasyName' : 'Nome Fantasia',
        'cnpj' : 'CNPJ',
        'socialReason' : 'Razão Social',
        'StateRegistration' : 'Inscrição Estadual',
        'typeOfTaxpayer' : 'Tipo de Contribuinte',
        'MunicipalRegistration' : 'Inscrição Municipal',
        'suframa' : 'SUFRAMA',
        'Responsible' : 'Responsavel',
        'WorkPhone' : 'Telefone de Trabalho', 
        'PersonalPhone' : 'Telefone Pessoal', 
        'isActive' : 'isActive', 
        'site' : 'site', 
        'salesman' : 'Vendedor',
        'creditLimit' : 'Limite de Crédito', 
        'email' : 'E-mail', 
        'password' : 'Senha', 
        'isClient' : "Cliente",
        'isSupllier' : "Fornecedor",
        'isUser' : "Usuario do Sistema",
        'isEmployee' : "Funcionario",
        'issalesman' : "Vendedor",
        'isFormer_employee' : "Ex-Funcionario",
        'isCarrier' : "Transportadora",
        'isDelivery_man' : "Entregador",
        'isTechnician' : "Tecnico",
        'id_FisicPerson_fk' : 'Codigo de Pessoa Fisica',
        'id_LegalPerson_fk' : 'Codigo de Pessoa Juridica',
        'id_ForeignPerson_fk' : 'Codigo de Estrangeiro',
        'id_address_fk' : 'Codigo de Endereço',
        'id_user_fk' : 'Codigo de Usuario',
        'person' : "codigo de Pessoa com Credito",
        'credit_data' : 'Data do Crédito',
        'credit_value' : 'Valor de Credito' 
    }
    return NOME_AMIGAVEL_CAMPOS.get(value, value)

@register.filter(name='cont_type')
def cont_type(value):

    NOME_AMIGAVEL_CAMPOS = {
        '1' : 'log de Erros',
        '3' : 'Grupos de Usuarios',
        '2' : 'Permissões',
        '4' : 'Usuarios',
        '5' : 'Tipo de Conteudo',
        '6' : 'Sessão', 
        '7' : 'Forma de Pagamento',
        '8' : 'Cargos',
        '9' : 'Serviços',
        '10' : 'Situações Personalizadas',
        '11' : 'Plano de Contas',
        '12' : 'log_desativado',
        '13' : 'info_logs_desativado',
        '14' : 'supergroup_ainda em analise',
        '15' : 'Endereço',
        '16' : 'Pessoa Fisica',
        '17' : 'Estrangeiro',
        '18' : 'Pessoa Juridica',
        '19' : 'Pessoa',
        '20' : 'Limite de Credito',
        '21' : 'Venda',
        '22' : 'Formas de Pagamento Presentes na Venda',
        '23' : 'Produtos dentro da Venda',
        '24' : 'Compras',
        '25' : 'Fretes',
        '26' : 'Lista de escolhas',
        '27' : 'Produtos',
        '28' : 'Produtos dentro da Compra',
        '29' : 'Imposto',
        '30' : 'Contas',
        '31' : 'Caixa Diario',
        '32' : 'Fechamento de Caixa',
        '33' : 'Formas de Pagamento em Contas',
        '34' : 'Movimentação de Caixa',
        '35' : 'Ordem de Serviço',
        '36' : 'Serviços dentro da Ordem de Serviço',
        '37' : 'Produtos dentro da Ordem de Serviço',
        '38' : 'paymentmethod_vendaservice',
        '39' : 'log de Auditoria',

    }
    return NOME_AMIGAVEL_CAMPOS.get(str(value), f"Desconhecido (ID {value})")  # Retorna nome amigável, ou o próprio valor se não encontrar

@register.filter(name='action')
def cont_type(value):
    NOME_AMIGAVEL_CAMPOS = {
        '0' : 'Criou',
        '1' : 'Editou',
        '2' : 'Deletou',
    }
    return NOME_AMIGAVEL_CAMPOS.get(str(value), f"Desconhecido (ID {value})")  # Retorna nome amigável, ou o próprio valor se não encontrar

@register.filter(name='action')
def cont_type(value):
    NOME_AMIGAVEL_CAMPOS = {
        '0' : 'Criou',
        '1' : 'Editou',
        '2' : 'Deletou',
    }
    return NOME_AMIGAVEL_CAMPOS.get(str(value), f"Desconhecido (ID {value})")  # Retorna nome amigável, ou o próprio valor se não encontrar