INSERT INTO api_funcionario (usuario_id, hierarquia_do_cargo, departamento) VALUES
('987.654.321-00', 'Pleno', 'TI'),
('222.333.444-55', 'Júnior', 'Vendas'),
('555.666.777-88', 'Sênior', 'RH'),
('888.999.000-11', 'Júnior', 'Marketing'),
('333.444.555-66', 'Pleno', 'Financeiro'),
('666.777.888-99', 'Estagiário', 'TI')
ON CONFLICT (usuario_id) DO NOTHING;