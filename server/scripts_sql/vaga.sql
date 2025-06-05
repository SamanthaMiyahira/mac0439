INSERT INTO api_vaga (status, tipo, localizacao) VALUES
-- Vagas Convencionais
('disponivel', 'convencional', 'A1'),
('disponivel', 'convencional', 'A2'),
('disponivel', 'convencional', 'A3'),
('disponivel', 'convencional', 'A4'),
('disponivel', 'convencional', 'A5'),
('disponivel', 'convencional', 'B1'),
('disponivel', 'convencional', 'B2'),
('disponivel', 'convencional', 'B3'),
('disponivel', 'convencional', 'B4'),
('disponivel', 'convencional', 'B5'),
('disponivel', 'convencional', 'C1'),
('disponivel', 'convencional', 'C2'),
('disponivel', 'convencional', 'C3'),
('disponivel', 'convencional', 'C4'),
('disponivel', 'convencional', 'C5'),

-- Vagas Elétricas
('disponivel', 'eletrica', 'E1'),
('disponivel', 'eletrica', 'E2'),
('disponivel', 'eletrica', 'E3'),
('disponivel', 'eletrica', 'E4'),
('disponivel', 'eletrica', 'E5'),

-- Vagas Preferenciais
('disponivel', 'preferencial', 'P1'),
('disponivel', 'preferencial', 'P2'),
('disponivel', 'preferencial', 'P3'),
('disponivel', 'preferencial', 'P4'),
('disponivel', 'preferencial', 'P5')
ON CONFLICT (localizacao) DO NOTHING;

