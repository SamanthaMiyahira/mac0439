# SmartPark - Sistema de Estacionamento

## COMO EXECUTAR O PROJETO 

### PRÉ-REQUISITOS:
- Python 3.12.3
- Django 5.2.1
- MongoDB instalado (baixe em: https://www.mongodb.com/try/download/community)

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

   `python test_script.py`

1. Verifique se o MongoDB está rodando:

   `mongosh`

2. Conecte-se ao banco do projeto:

   `use smartpark_nosql`

3. Visualize os eventos cadastrados:

   `db.eventos.find().pretty()`

4. Para sair:

   `exit`

### COMANDOS ÚTEIS:
- Criar superusuário:

  `python manage.py createsuperuser`
  




