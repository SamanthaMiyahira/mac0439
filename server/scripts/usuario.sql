INSERT INTO api_usuario (cpf, nome, tipo, email, prioridade, foto) VALUES
('123.456.789-00', 'Sabrina Araújo', 'administrador', 'sabrina@example.com', 1, NULL),
('987.654.321-00', 'Carlos Silva', 'funcionario', 'carlos@example.com', 2, NULL),
('111.222.333-44', 'Ana Pereira', 'visitante', 'ana@example.com', NULL, NULL),
('222.333.444-55', 'Pedro Almeida', 'funcionario', 'pedro.a@example.com', 2, NULL),
('333.444.555-66', 'Mariana Costa', 'funcionario', 'mariana.c@example.com', 1, NULL),
('444.555.666-77', 'João Santos', 'visitante', 'joao.s@example.com', NULL, NULL),
('555.666.777-88', 'Fernanda Lima', 'funcionario', 'fernanda.l@example.com', 3, NULL),
('666.777.888-99', 'Ricardo Oliveira', 'funcionario', 'ricardo.o@example.com', 1, NULL),
('777.888.999-00', 'Amanda Souza', 'visitante', 'amanda.s@example.com', NULL, NULL),
('888.999.000-11', 'Lucas Pereira', 'funcionario', 'lucas.p@example.com', 2, NULL)
ON CONFLICT (cpf) DO NOTHING;