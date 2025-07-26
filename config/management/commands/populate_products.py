from django.core.management.base import BaseCommand
from faker import Faker
from random import randint, choice
from decimal import Decimal
from registry.models import Person
from purchase.models import Product

class Command(BaseCommand):
    help = "Popula o banco de dados com produtos fictícios associados a pessoas como fornecedores."

    def handle(self, *args, **kwargs):
        fake = Faker(['pt_BR'])

        # Configuração: Número de produtos para criar
        num_products = 50  # Número de produtos fictícios
        suppliers = list(Person.objects.filter(isSupllier=True))  # Somente pessoas que são fornecedores

        if not suppliers:
            self.stdout.write(self.style.ERROR("Nenhum fornecedor encontrado no banco de dados."))
            return

        self.stdout.write("Gerando produtos fictícios...")

        for _ in range(num_products):
            supplier = choice(suppliers)  # Escolhe um fornecedor aleatório

            product = Product.objects.create(
                description=fake.word().capitalize(),
                product_code=fake.unique.ean(length=8),  # Código de produto fictício
                barcode=fake.unique.ean(length=13),      # Código de barras fictício
                unit_of_measure=choice(["UN", "KG", "L", "M"]),
                brand=fake.company(),
                cost_of_product=Decimal(fake.random_number(digits=5)) / 100,  # Custo do produto
                selling_price=Decimal(fake.random_number(digits=5)) / 100 + Decimal(randint(10, 100)),  # Preço de venda
                ncm=fake.unique.random_number(digits=8),
                csosn=str(fake.random_number(digits=3)),
                cfop=str(fake.random_number(digits=4)),
                current_quantity=randint(0, 500),  # Quantidade atual aleatória
                maximum_quantity=randint(100, 1000),  # Quantidade máxima aleatória
                minimum_quantity=randint(10, 100),  # Quantidade mínima aleatória
                is_active=choice([True, False]),
                supplier=supplier,  # Fornecedor escolhido
            )

            self.stdout.write(f"Produto criado: {product.description} (Fornecedor: {supplier.id})")

        self.stdout.write(self.style.SUCCESS("Produtos fictícios gerados com sucesso!"))
