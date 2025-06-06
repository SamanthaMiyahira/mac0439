from django.db import models
from django.core.validators import URLValidator, MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

def validate_url(value):
    validator = URLValidator()
    try:
        validator(value)
    except ValidationError:
        raise ValidationError('URL inválida')

class Usuario(models.Model):
    TIPO_USUARIO_CHOICES = [
        ('visitante', 'Visitante'),
        ('funcionario', 'Funcionário'),
        ('administrador', 'Administrador')
    ]
    
    cpf = models.CharField(max_length=14, primary_key=True)
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_USUARIO_CHOICES)
    email = models.EmailField(unique=True)
    prioridade = models.IntegerField(validators=[MinValueValidator(0)], null=True, blank=True)
    foto = models.URLField(max_length=500, validators=[validate_url], null=True, blank=True)

class Funcionario(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True, related_name='funcionario')
    hierarquia_do_cargo = models.CharField(max_length=50)
    departamento = models.CharField(max_length=50)

class Veiculo(models.Model):
    TIPO_VEICULO_CHOICES = [
        ('convencional', 'Convencional'),
        ('eletrico', 'Elétrico')
    ]
    
    placa = models.CharField(max_length=10, primary_key=True)
    modelo = models.CharField(max_length=50)
    marca = models.CharField(max_length=50)
    tipo = models.CharField(max_length=30, choices=TIPO_VEICULO_CHOICES)
    imagem_placa = models.URLField(max_length=500, validators=[validate_url], null=True, blank=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

class Vaga(models.Model):
    STATUS_CHOICES = [
        ('ocupada', 'Ocupada'),
        ('reservada', 'Reservada'),
        ('disponivel', 'Disponível'),
        ('bloqueada', 'Bloqueada')
    ]
    
    TIPO_VAGA_CHOICES = [
        ('convencional', 'Convencional'),
        ('eletrica', 'Elétrica'),
        ('preferencial', 'Preferencial')
    ]
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    tipo = models.CharField(max_length=20, choices=TIPO_VAGA_CHOICES)
    localizacao = models.CharField(max_length=20, primary_key=True)

class Credencial(models.Model):
    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('bloqueado', 'Bloqueado'),
        ('desativado', 'Desativado')
    ]
    
    data_emissao = models.DateTimeField()
    data_expiracao = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    qrcode = models.URLField(max_length=500, validators=[validate_url])

class Reserva(models.Model):
    tipo_CHOICES = [
        ('eventual', 'Eventual'),
        ('recorrente', 'Recorrente')
    ]

    STATUS_CHOICES = [
        ('ativa', 'Ativa'),
        ('concluida', 'Concluída'),
    ]
    
    data_hora_entrada = models.DateTimeField(null=True, blank=True)
    data_hora_saida = models.DateTimeField(null=True, blank=True)
    data = models.DateField(null=True, blank=True)
    tipo = models.CharField(max_length=20, choices=tipo_CHOICES)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.SET_NULL, null=True)
    vaga = models.ForeignKey(Vaga, on_delete=models.SET_NULL, null=True, blank=True)
    credencial = models.ForeignKey(Credencial, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ativa')

class FilaDeEspera(models.Model):
    STATUS_CHOICES = [
        ('aguardando', 'Aguardando'),
        ('cancelada', 'Cancelada'),
        ('realizada', 'Realizada')
    ]
    
    prioridade = models.IntegerField(validators=[MinValueValidator(0)])
    data_hora = models.DateTimeField()
    data_reserva = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    reserva = models.ForeignKey(Reserva, on_delete=models.SET_NULL, null=True, blank=True)

class Incidente(models.Model):
    gravidade = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    acao = models.TextField()
    data_hora = models.DateTimeField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    reserva = models.ForeignKey(Reserva, on_delete=models.SET_NULL, null=True, blank=True)

class Notificacao(models.Model):
    TIPO_CHOICES = [
        ('reserva', 'Reserva'),
        ('fila_de_espera', 'Fila de Espera'),
        ('incidente', 'Incidente')
    ]
    
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    mensagem = models.TextField()
    data_hora = models.DateTimeField()
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    reserva = models.ForeignKey(Reserva, on_delete=models.SET_NULL, null=True, blank=True)