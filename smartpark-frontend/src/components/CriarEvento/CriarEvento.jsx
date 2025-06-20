import React, { useState } from 'react';
import TextInput from '../TextInput/TextInput';
import Button from '../Button/Button';
import './CriarEvento.css';
import { criarEvento } from '../../api';

export default function CriarEvento() {
  const [titulo, setTitulo] = useState('');
  const [responsavelCpf, setResponsavelCpf] = useState('');
  const [dataHora, setDataHora] = useState('');
  const [participantes, setParticipantes] = useState([{ cpf: '' }]);
  const [mensagem, setMensagem] = useState('');
  const [erro, setErro] = useState('');

  const handleAdicionarParticipante = () => {
    setParticipantes([...participantes, { cpf: '' }]);
  };

  const handleChangeParticipante = (index, field, value) => {
    const novosParticipantes = [...participantes];
    novosParticipantes[index][field] = value;
    setParticipantes(novosParticipantes);
  };

  const handleCriar = async () => {
    setMensagem('');
    setErro('');

    if (!titulo || !responsavelCpf || !dataHora) {
      setErro('Preencha todos os campos obrigatórios.');
      return;
    }

    try {
      const evento = {
        titulo,
        responsavel_cpf: responsavelCpf,
        data_hora: new Date(dataHora).toISOString(),
        participantes,
      };

      const res = await criarEvento(evento);
      setMensagem(res.mensagem || 'Evento criado com sucesso!');
      setTitulo('');
      setResponsavelCpf('');
      setDataHora('');
      setParticipantes([{ cpf: ''}]);
    } catch (e) {
      setErro(e.message || 'Erro ao criar evento');
    }
  };

  return (
    <div className="criar-evento-container">
      <h2>Criar Evento</h2>
      <TextInput placeholder="Título" value={titulo} onChange={(e) => setTitulo(e.target.value)} />
      <TextInput placeholder="CPF do Responsável" value={responsavelCpf} onChange={(e) => setResponsavelCpf(e.target.value)} />
      <TextInput placeholder="Data e Hora" type="datetime-local" value={dataHora} onChange={(e) => setDataHora(e.target.value)} />

      <h4>Participantes</h4>
      {participantes.map((p, index) => (
        <div key={index} className="participante-item">
          <TextInput
            placeholder="CPF"
            value={p.cpf}
            onChange={(e) => handleChangeParticipante(index, 'cpf', e.target.value)}
          />
        </div>
      ))}
      <Button onClick={handleAdicionarParticipante}>Adicionar Participante</Button>
      <Button onClick={handleCriar}>Criar Evento</Button>

      {erro && <p className="criar-evento-erro">{erro}</p>}
      {mensagem && <p className="criar-evento-mensagem">{mensagem}</p>}
    </div>
  );
}
