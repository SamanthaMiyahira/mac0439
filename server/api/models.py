from django.db import models

# Modelos SQL (temporário)

class Usuario(models.Model):
    cpf = models.CharField(max_length=14, unique=True)
    nome = models.CharField(max_length=100)
    email = models.EmailField()

class Veiculo(models.Model):
    placa = models.CharField(max_length=10, unique=True)
    dono = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=[('convencional', 'Convencional'), ('eletrico', 'Elétrico')])

class Vaga(models.Model):
    id_vaga = models.CharField(max_length=10, unique=True)
    tipo = models.CharField(max_length=20, choices=[('comum', 'Comum'), ('preferencial', 'Preferencial')])