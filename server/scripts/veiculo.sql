INSERT INTO api_veiculo (placa, modelo, marca, tipo, imagem_placa, usuario_id) VALUES
('ABC1D23', 'Gol', 'Volkswagen', 'convencional', NULL, '123.456.789-00'),
('XYZ4E56', 'Onix', 'Chevrolet', 'convencional', NULL, '987.654.321-00'),
('FGH7I89', 'Kwid', 'Renault', 'convencional', NULL, '111.222.333-44'),
('JKL0M12', 'HB20', 'Hyundai', 'convencional', NULL, '222.333.444-55'),
('MNO3P45', 'Argo', 'Fiat', 'convencional', NULL, '333.444.555-66'),
('PQR6S78', 'T-Cross', 'Volkswagen', 'convencional', NULL, '444.555.666-77'),
('STU9V01', 'Compass', 'Jeep', 'convencional', NULL, '555.666.777-88'),
('VWX2Y34', 'Corolla', 'Toyota', 'convencional', NULL, '666.777.888-99'),
('YZA5B67', 'Civic', 'Honda', 'convencional', NULL, '777.888.999-00'),
('BCD8C90', 'Tracker', 'Chevrolet', 'convencional', NULL, '888.999.000-11')
ON CONFLICT (placa) DO NOTHING;