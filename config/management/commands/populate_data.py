from django.core.management.base import BaseCommand
from faker import Faker
from random import randint, choice
from decimal import Decimal
from registry.models import Address, FisicPerson, ForeignPerson, LegalPerson, Person

class Command(BaseCommand):
    help = "Popula o banco de dados com dados fictícios."

    def handle(self, *args, **kwargs):
        fake = Faker(['pt_BR'])

        # Configuração: Número de registros para criar
        num_addresses = 30
        num_fisic_persons = 10
        num_foreign_persons = 10
        num_legal_persons = 10
        num_people = 30

        self.stdout.write("Gerando dados fictícios...")

        # Criar endereços
        addresses = []
        for _ in range(num_addresses):
            address = Address.objects.create(
                cep=fake.postcode(),
                road=fake.street_name(),
                number=fake.building_number(),
                neighborhood=fake.neighborhood(),
                reference=fake.sentence(nb_words=4),
                city=fake.city(),
                uf=fake.state_abbr(),
                country=fake.country(),
            )
            addresses.append(address)
        
        # Garantir que os endereços sejam usados apenas uma vez
        available_addresses = addresses[:]

        # Criar pessoas físicas
        fisic_persons = []
        for _ in range(num_fisic_persons):
            fisic_person = FisicPerson.objects.create(
                name=fake.name(),
                cpf=fake.cpf(),
                rg=fake.rg(),
                dateOfBirth=fake.date_of_birth(minimum_age=18, maximum_age=80).strftime('%d/%m/%Y'),
            )
            fisic_persons.append(fisic_person)

        # Criar pessoas estrangeiras
        foreign_persons = []
        for _ in range(num_foreign_persons):
            foreign_person = ForeignPerson.objects.create(
                name_foreigner=fake.name(),
                num_foreigner=fake.uuid4(),
            )
            foreign_persons.append(foreign_person)

        # Criar pessoas jurídicas
        legal_persons = []
        for _ in range(num_legal_persons):
            legal_person = LegalPerson.objects.create(
                fantasyName=fake.company(),
                cnpj=fake.cnpj(),
                socialReason=fake.company_suffix(),
                StateRegistration=fake.uuid4(),
                typeOfTaxpayer=fake.job(),
                MunicipalRegistration=fake.uuid4(),
                suframa=fake.uuid4(),
                Responsible=fake.name(),
            )
            legal_persons.append(legal_person)

        # Criar entidades de Person
        for _ in range(num_people):
            # Determinar o tipo de relação
            person_type = choice(['fisic', 'legal', 'foreign'])

            # Inicializar as variáveis com None
            id_FisicPerson_fk = None
            id_LegalPerson_fk = None
            id_ForeignPerson_fk = None

            # Associar o ID correto com base no tipo de pessoa
            if person_type == 'fisic' and fisic_persons:
                id_FisicPerson_fk = fisic_persons.pop()  # Apenas o ID da pessoa física
            elif person_type == 'legal' and legal_persons:
                id_LegalPerson_fk = legal_persons.pop()  # Apenas o ID da pessoa jurídica
            elif person_type == 'foreign' and foreign_persons:
                id_ForeignPerson_fk = foreign_persons.pop()  # Apenas o ID da pessoa estrangeira

            # Verificar se pelo menos uma chave estrangeira foi atribuída
            if not any([id_FisicPerson_fk, id_LegalPerson_fk, id_ForeignPerson_fk]):
                # Pular esta iteração se não houver chave estrangeira válida
                continue
            
            # Criar a entidade Person com apenas uma relação
            Person.objects.create(
                WorkPhone=fake.phone_number(),
                PersonalPhone=fake.phone_number(),
                isActive=choice([False, False]),
                site=fake.url(),
                salesman=fake.name() if choice([True, False]) else None,
                creditLimit=Decimal(randint(500, 10000)),
                isClient=choice([True, False]),
                isSupllier=choice([True, False]),
                isUser=choice([False, False]),
                isEmployee=choice([True, False]),
                isFormer_employee=choice([True, False]),
                isCarrier=choice([True, False]),
                isDelivery_man=choice([True, False]),
                isTechnician=choice([True, False]),
                id_FisicPerson_fk=id_FisicPerson_fk,
                id_LegalPerson_fk=id_LegalPerson_fk,
                id_ForeignPerson_fk=id_ForeignPerson_fk,
                id_address_fk=available_addresses.pop(),  # Retira um endereço da lista

            )

        self.stdout.write(self.style.SUCCESS("Dados fictícios gerados com sucesso!"))
