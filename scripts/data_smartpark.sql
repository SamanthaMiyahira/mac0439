
-- DADOS FICTICIOS PARA POPULAR O BANCO SMARTPARK

-- usuarios
INSERT INTO usuarios (cpf, nome, tipo_de_usuario, email, prioridade, foto) VALUES
('11111111111', 'Alice Souza', 'funcionario', 'alice@exemplo.com', 1, 'https://ex.com/foto1.jpg'),
('22222222222', 'Bruno Lima', 'visitante', 'bruno@exemplo.com', 2, NULL),
('33333333333', 'Carla Mendes', 'administrador', 'carla@exemplo.com', 0, 'https://ex.com/foto2.jpg'),
('44444444444', 'Daniel Rocha', 'funcionario', 'daniel@exemplo.com', 3, 'https://ex.com/foto3.jpg'),
('55555555555', 'Eduarda Nunes', 'visitante', 'eduarda@exemplo.com', 1, NULL);

-- funcionarios
INSERT INTO funcionarios (hierarquia_do_cargo, departamento, cpf) VALUES
('Gerente', 'Administração', '11111111111'),
('Analista', 'Tecnologia', '44444444444');

-- veiculos
INSERT INTO veiculos (placa, modelo, marca, tipo_de_veiculo, imagem_placa, cpf_usuario) VALUES
('ABC1D23', 'Model 3', 'Tesla', 'eletrico', 'https://ex.com/placa1.jpg', '11111111111'),
('XYZ9F87', 'Corolla', 'Toyota', 'convencional', NULL, '22222222222'),
('QWE8R56', 'Onix', 'Chevrolet', 'convencional', 'https://ex.com/placa2.jpg', '44444444444'),
('LMN3T99', 'Leaf', 'Nissan', 'eletrico', 'https://ex.com/placa3.jpg', '55555555555');

-- vagas
INSERT INTO vagas (status, tipo_de_vaga, localizacao) VALUES
('disponivel', 'convencional', 'A1'),
('reservada', 'eletrica', 'B2'),
('ocupada', 'preferencial', 'C3'),
('bloqueada', 'eletrica', 'D4'),
('disponivel', 'preferencial', 'E5');

-- credenciais
INSERT INTO credenciais (data_emissao, data_expiracao, status, qrcode) VALUES
(NOW(), NOW() + INTERVAL '30 days', 'ativo', 'https://ex.com/qr1.png'),
(NOW(), NOW() + INTERVAL '15 days', 'bloqueado', 'https://ex.com/qr2.png'),
(NOW(), NOW() + INTERVAL '10 days', 'desativado', 'https://ex.com/qr3.png');

-- reservas
INSERT INTO reservas (data_hora_entrada, data_hora_saida, periodo, tipo_reserva, cpf_usuario, id_veiculo, id_vaga, id_credencial) VALUES
(NOW(), NOW() + INTERVAL '2 hours', INTERVAL '2 hours', 'eventual', '11111111111', 1, 1, 1),
(NOW(), NULL, INTERVAL '3 hours', 'recorrente', '22222222222', 2, 2, 2),
(NOW(), NOW() + INTERVAL '1.5 hours', INTERVAL '1.5 hours', 'eventual', '44444444444', 3, 3, 3);

-- fila_de_espera
INSERT INTO fila_de_espera (prioridade, data_hora, status, cpf_usuario, id_reserva) VALUES
(1, NOW(), 'aguardando', '33333333333', 1),
(2, NOW(), 'cancelada', '55555555555', NULL),
(0, NOW(), 'realizada', '44444444444', 2);

-- incidentes
INSERT INTO incidentes (tipo_incidente, gravidade, acao, data_hora, cpf_usuario, id_reserva) VALUES
('Dano ao veículo', 7, 'Acionar segurança', NOW(), '11111111111', 1),
('Uso indevido da vaga', 5, 'Advertência enviada', NOW(), '22222222222', NULL),
('Estacionamento irregular', 9, 'Reboque solicitado', NOW(), '44444444444', 2);

-- eventos
INSERT INTO eventos (data_hora, titulo, numero_participantes, cpf_responsavel) VALUES
(NOW(), 'Feira de Inovação', 100, '33333333333'),
(NOW(), 'Workshop de Sustentabilidade', 40, NULL),
(NOW(), 'Apresentação de Teses', 20, '11111111111');

-- pagamentos
INSERT INTO pagamentos (valor, data_hora, status, metodo, id_reserva, cpf_usuario) VALUES
(15.50, NOW(), 'concluido', 'pix', 1, '11111111111'),
(10.00, NOW(), 'pendente', 'credito', 2, '22222222222'),
(20.00, NOW(), 'cancelado', 'debito', 3, '44444444444');

-- notificacoes
INSERT INTO notificacoes (tipo_notificacao, mensagem, data_hora, cpf_usuario, id_reserva) VALUES
('reserva', 'Sua reserva foi confirmada.', NOW(), '11111111111', 1),
('fila_de_espera', 'Você foi adicionado à fila de espera.', NOW(), '33333333333', NULL),
('incidente', 'Ocorrência registrada com gravidade 9.', NOW(), '44444444444', 2);
