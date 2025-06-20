import React, { useEffect, useState } from 'react';
import { buscarEventos, atualizarStatusEvento } from '../../api'; // importe a função que vamos criar
import './Eventos.css';
import Button from '../Button/Button';

export default function Eventos() {
  const [eventos, setEventos] = useState([]);
  const [erro, setErro] = useState('');
  const [mensagem, setMensagem] = useState('');

  useEffect(() => {
    carregarEventos();
  }, []);

  async function carregarEventos() {
    try {
      const dados = await buscarEventos();
      setEventos(dados.reverse());
      if (dados.length === 0) {
        setMensagem('Nenhum evento cadastrado.');
      } else {
        setMensagem('');
      }
      setErro('');
    } catch (e) {
      setErro(e.message || 'Erro ao carregar eventos');
      setMensagem('');
    }
  }

  async function handleAtualizarStatus(id, status) {
    try {
      await atualizarStatusEvento(id, status);
      setMensagem(`Evento ${status} com sucesso.`);
      // Atualiza localmente
      setEventos(oldEventos =>
        oldEventos.map(ev =>
          ev._id === id ? { ...ev, metadata: { ...ev.metadata, status } } : ev
        )
      );
      setErro('');
    } catch {
      setErro('Erro ao atualizar status do evento.');
      setMensagem('');
    }
  }

  return (
    <div className="eventos-container">
      <h2>Eventos Cadastrados</h2>
      {erro && <p className="eventos-erro">{erro}</p>}
      {mensagem && <p className="eventos-mensagem">{mensagem}</p>}

      {eventos.map((evento) => (
        <div key={evento._id} className="evento-card">
          <p><strong>Título:</strong> {evento.titulo}</p>
          <p><strong>Responsável:</strong> {evento.responsavel_cpf}</p>
          <p><strong>Data e Hora:</strong> {new Date(evento.data_hora).toLocaleString()}</p>
          <p><strong>Status:</strong> {evento.metadata?.status || 'N/A'}</p>
          <p><strong>Participantes:</strong></p>
          <ul>
            {evento.participantes.map((p, i) => (
              <li key={i}>
                {p.cpf} {p.placa_veiculo ? `— ${p.placa_veiculo}` : ''}
              </li>
            ))}
          </ul>

          <div style={{ marginTop: 10 }}>
            {evento.metadata?.status === 'pendente' && (
            <>
                <Button onClick={() => handleAtualizarStatus(evento._id, 'concluido')}>Concluir evento</Button>
                <Button onClick={() => handleAtualizarStatus(evento._id, 'cancelado')}>Cancelar evento</Button>
            </>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}
