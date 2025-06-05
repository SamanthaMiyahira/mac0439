CREATE TABLE usuarios (
    cpf VARCHAR(11) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    tipo_de_usuario VARCHAR(20) NOT NULL CHECK (tipo_de_usuario IN ('visitante', 'funcionario', 'administrador')),
    email VARCHAR(100) UNIQUE NOT NULL,
    prioridade INT CHECK (prioridade >= 0),
    foto TEXT
);

CREATE TABLE funcionarios (
    id SERIAL PRIMARY KEY,
    hierarquia_do_cargo VARCHAR(50) NOT NULL,
    departamento VARCHAR(50) NOT NULL,
    cpf VARCHAR(11) NOT NULL UNIQUE,
    FOREIGN KEY (cpf) REFERENCES usuarios(cpf) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE veiculos (
    id SERIAL PRIMARY KEY,
    placa VARCHAR(10) NOT NULL UNIQUE,
    modelo VARCHAR(50) NOT NULL,
    marca VARCHAR(50) NOT NULL,
    tipo_de_veiculo VARCHAR(30) NOT NULL CHECK (tipo_de_veiculo IN ('convencional', 'eletrico')),
    imagem_placa TEXT,
    cpf_usuario VARCHAR(11) NOT NULL,
    FOREIGN KEY (cpf_usuario) REFERENCES usuarios(cpf) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE vagas (
    id SERIAL PRIMARY KEY,
    status VARCHAR(20) NOT NULL CHECK (status IN ('ocupada', 'reservada', 'disponivel', 'bloqueada')),
    tipo_de_vaga VARCHAR(20) NOT NULL CHECK (tipo_de_vaga IN ('convencional', 'eletrica', 'preferencial')),
    localizacao VARCHAR(20)
);

CREATE TABLE credenciais (
    id SERIAL PRIMARY KEY,
    data_emissao TIMESTAMP NOT NULL,
    data_expiracao TIMESTAMP NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('ativo', 'bloqueado', 'desativado')),
    qrcode TEXT NOT NULL
);

CREATE TABLE reservas (
    id SERIAL PRIMARY KEY,
    data_hora_entrada TIMESTAMP NOT NULL,
    data_hora_saida TIMESTAMP,
    periodo INTERVAL NOT NULL,
    tipo_reserva VARCHAR(20) NOT NULL CHECK (tipo_reserva IN ('eventual', 'recorrente')),
    cpf_usuario VARCHAR(11) NOT NULL,
    id_veiculo INT,
    id_vaga INT,
    id_credencial INT,
    FOREIGN KEY (cpf_usuario) REFERENCES usuarios(cpf) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (id_veiculo) REFERENCES veiculos(id) ON UPDATE CASCADE ON DELETE SET NULL,
    FOREIGN KEY (id_vaga) REFERENCES vagas(id) ON UPDATE CASCADE ON DELETE SET NULL,
    FOREIGN KEY (id_credencial) REFERENCES credenciais(id) ON UPDATE CASCADE ON DELETE SET NULL
);

CREATE TABLE fila_de_espera (
    id SERIAL PRIMARY KEY,
    prioridade INT NOT NULL CHECK (prioridade >= 0),
    data_hora TIMESTAMP NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('aguardando', 'cancelada', 'realizada')),
    cpf_usuario VARCHAR(11) NOT NULL,
    id_reserva INT,
    FOREIGN KEY (cpf_usuario) REFERENCES usuarios(cpf) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (id_reserva) REFERENCES reservas(id) ON UPDATE CASCADE ON DELETE SET NULL
);

CREATE TABLE incidentes (
    id SERIAL PRIMARY KEY,
    tipo_incidente VARCHAR(50) NOT NULL,
    gravidade INT NOT NULL CHECK (gravidade BETWEEN 1 AND 10),
    acao TEXT NOT NULL,
    data_hora TIMESTAMP NOT NULL,
    cpf_usuario VARCHAR(11) NOT NULL,
    id_reserva INT,
    FOREIGN KEY (cpf_usuario) REFERENCES usuarios(cpf) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (id_reserva) REFERENCES reservas(id) ON UPDATE CASCADE ON DELETE SET NULL
);

CREATE TABLE eventos (
    id SERIAL PRIMARY KEY,
    data_hora TIMESTAMP NOT NULL,
    titulo VARCHAR(100) NOT NULL,
    numero_participantes INT CHECK (numero_participantes >= 0),
    cpf_responsavel VARCHAR(11),
    FOREIGN KEY (cpf_responsavel) REFERENCES usuarios(cpf) ON UPDATE CASCADE ON DELETE SET NULL
);

CREATE TABLE pagamentos (
    id SERIAL PRIMARY KEY,
    valor DECIMAL(10, 2) NOT NULL CHECK (valor >= 0),
    data_hora TIMESTAMP NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('pendente', 'concluido', 'cancelado')),
    metodo VARCHAR(30) NOT NULL CHECK (metodo IN ('pix', 'boleto', 'credito', 'debito')),
    id_reserva INT,
    cpf_usuario VARCHAR(11) NOT NULL,
    FOREIGN KEY (id_reserva) REFERENCES reservas(id) ON UPDATE CASCADE ON DELETE SET NULL,
    FOREIGN KEY (cpf_usuario) REFERENCES usuarios(cpf) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE notificacoes (
    id SERIAL PRIMARY KEY,
    tipo_notificacao VARCHAR(50) NOT NULL CHECK (tipo_notificacao IN ('reserva', 'fila_de_espera', 'incidente')),
    mensagem TEXT NOT NULL,
    data_hora TIMESTAMP NOT NULL,
    cpf_usuario VARCHAR(11),
    id_reserva INT,
    FOREIGN KEY (cpf_usuario) REFERENCES usuarios(cpf) ON UPDATE CASCADE ON DELETE SET NULL,
    FOREIGN KEY (id_reserva) REFERENCES reservas(id) ON UPDATE CASCADE ON DELETE SET NULL
);



-- triggers

-- 1) validacao da url da foto em usuario

CREATE OR REPLACE FUNCTION is_valid_url(url TEXT)
RETURNS BOOLEAN AS $$
BEGIN
  IF url IS NULL THEN
    RETURN TRUE;
  END IF;

  RETURN url ~* '^https?://[a-zA-Z0-9.-]+(\.[a-zA-Z]{2,})(:[0-9]{1,5})?(/[^\s]*)?$';
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION trigger_validate_foto_url()
RETURNS TRIGGER AS $$
BEGIN
  IF NOT is_valid_url(NEW.foto) THEN
    RAISE EXCEPTION 'Campo "foto" não é uma URL válida: %', NEW.foto;
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER trg_check_foto_url
BEFORE INSERT OR UPDATE ON usuarios
FOR EACH ROW
EXECUTE FUNCTION trigger_validate_foto_url();


-- 2) validacao da url da imagem_placa do veiculo

CREATE OR REPLACE FUNCTION trigger_validate_imagem_placa_url()
RETURNS TRIGGER AS $$
BEGIN
  IF NOT is_valid_url(NEW.imagem_placa) THEN
    RAISE EXCEPTION 'Campo "imagem_placa" não é uma URL válida: %', NEW.imagem_placa;
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER trg_check_imagem_placa_url
BEFORE INSERT OR UPDATE ON veiculos
FOR EACH ROW
EXECUTE FUNCTION trigger_validate_imagem_placa_url();


-- 3) validacao da url do qrcode da credencial

CREATE OR REPLACE FUNCTION trigger_validate_qrcode_url()
RETURNS TRIGGER AS $$
BEGIN
  IF NOT is_valid_url(NEW.qrcode) THEN
    RAISE EXCEPTION 'Campo "qrcode" não é uma URL válida: %', NEW.qrcode;
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER trg_check_qrcode_url
BEFORE INSERT OR UPDATE ON credenciais
FOR EACH ROW
EXECUTE FUNCTION trigger_validate_qrcode_url();
