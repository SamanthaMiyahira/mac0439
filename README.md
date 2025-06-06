# SmartPark - Sistema de Estacionamento

## COMO EXECUTAR O PROJETO 

### PRÉ-REQUISITOS:
- MongoDB instalado (baixe em: https://www.mongodb.com/try/download/community)
- Postgres instalado (https://www.postgresql.org/download/)

### INSTALAÇÃO:
1. Instale as dependências:

   `pip install -r requirements.txt`

2. Configure o banco de dados:

   `python manage.py makemigrations`

   `python manage.py migrate`

### EXECUÇÃO:
1. Inicie o servidor Django:

   `python manage.py runserver`

2. Acesse no navegador:
   http://localhost:8000

### ACESSO ADMIN:
- URL: http://localhost:8000/admin
- Usuário: admin
- Senha: admin

## ESTRUTURA DO PROJETO

O projeto Django está organizado dentro da pasta server com a seguinte estrutura principal:

`server/`

Contém arquivos principais do Django como settings.py, urls.py, wsgi.py, etc.

`server/api/`

Aplicação principal da API Django, com os seguintes subdiretórios:

`migrations/`

Arquivos gerados automaticamente para versionamento das alterações no banco de dados.

`scripts/`

Scripts Python usados para testar a API, como confirmação de entrada, confirmação de saída, criação de eventos, criação de reservas, pagamento de recibos, entre outros. Estes scripts simulam requisições à API enviando dados no formato JSON, facilitando testes automáticos e manuais.

`serializers/`

Contém os serializers do Django REST Framework, responsáveis por converter os dados dos modelos (models.py) em JSON e vice-versa, permitindo que a API envie e receba informações no formato adequado.

`services/`

Camada onde ficam as funções principais da aplicação, como criar_reserva, criar_evento, e outras lógicas de negócio. Essas funções manipulam os dados e interagem com os modelos.


`tests/`

Testes unitários da aplicação para garantir que funcionalidades específicas estão funcionando conforme esperado.

`utils/`

Utilitários e helpers, como o mongo_utils.py que inicializa o cliente MongoDB para operações com o banco NoSQL.

`views/`

As views do Django que recebem as requisições HTTP, validam dados, chamam as funções do serviço (services) e retornam as respostas da API. Elas atuam como controladoras, ligando os serializers, models e services.

`server/scripts_sql/`

Contém scripts SQL usados para popular o banco de dados PostgreSQL com dados iniciais (ex.: usuários, funcionários, vagas, veículos). Esses scripts facilitam a criação de registros para testes e desenvolvimento.

## TESTANDO O MONGODB 

1. Execute o script de teste para popular o banco de dados:

   `python manage.py test api`

1. Verifique se o MongoDB está rodando:

   `mongosh`

2. Conecte-se ao banco do projeto:

   `use smartpark_nosql`

3. Visualize os eventos cadastrados:

   `db.eventos.find().pretty()`

4. Para sair:

   `exit`

### POPULAR O BANCO DE DADOS

Os arquivos SQL de INSERT estão na pasta `\server\scripts`. Execute o comando 

`python scripts/populate.py` 

para popular o banco de dados PostgreSQL. O script já trata possíveis duplicações evitando erros ao inserir registros existentes.

### TESTAR A API

#### Scripts para testar a API (localizados em server/api/scripts):
`criar_reserva.py`

Script para criar uma nova reserva via API.

`confirmar_entrada.py`

Script para confirmar a entrada na reserva, enviando dados de QR code e placa.

`confirmar_saida.py`

Script para confirmar a saída do veículo.

`criar_evento.py`

Script para criar eventos no sistema.

`pagar_recibo.py`

Script para simular o pagamento de um recibo.

Estes scripts facilitam testes manuais e automatizados sem necessidade de ferramentas externas como Postman.

### COMANDOS ÚTEIS:
- Criar superusuário:

  `python manage.py createsuperuser`
  



