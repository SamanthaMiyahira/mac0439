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

#### Criação da reserva

A API de criar reserva está em: `http://localhost:8000/api/criar-reserva/`.

O script para se comunicar com essa API está em `scripts/criar_reserva.py`.

Este script é útil para testar manualmente o funcionamento da API de reservas sem precisar usar uma interface gráfica ou ferramenta como Postman.

#### Confirmação da entrada

A API para confirmar a entrada está em: `http://localhost:8000/api/confirmar-entrada/.`

O script para se comunicar com essa API está em `scripts/confirmar_entrada.py`.

Este script permite testar a confirmação da entrada da reserva, enviando os dados do QR code da credencial e a placa do veículo. Caso a credencial não esteja ativa ou esteja bloqueada, a confirmação não será realizada.

### COMANDOS ÚTEIS:
- Criar superusuário:

  `python manage.py createsuperuser`
  



