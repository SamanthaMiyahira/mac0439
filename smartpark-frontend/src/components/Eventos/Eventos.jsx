import React, { useEffect, useState } from 'react';
import { buscarEventos } from '../../api';
import './Eventos.css';

export default function Eventos() {
  const [eventos, setEventos] = useState([]);
  const [erro, setErro] = useState('');
  const [mensagem, setMensagem] = useState('');

  useEffect(() => {
    const carregarEventos = async () => {
      try {
        const dados = await buscarEventos();
        setEventos(dados);
        if (dados.length === 0) {
          setMensagem('Nenhum evento cadastrado.');
        }
      } catch (e) {
        setErro(e.message || 'Erro ao carregar eventos');
      }
    };
    carregarEventos();
  }, []);

  return (
    <div className="eventos-container">
      <h2>Eventos Cadastrados</h2>
      {erro && <p className="eventos-erro">{erro}</p>}
      {mensagem && <p className="eventos-mensagem">{mensagem}</p>}

      {eventos.map((evento) => (
        <div key={evento._id} className="evento-card">
          <p><strong>Título:</strong> {evento.titulo}</p>
          <p><strong>Responsável:</strong> {evento.responsavel_cpf}</p>
          <p><strong>Vagas Reservadas:</strong> {evento.vagas_reservadas}</p>
          <p><strong>Data e Hora:</strong> {new Date(evento.data_hora).toLocaleString()}</p>
          <p><strong>Participantes:</strong></p>
          <ul>
            {evento.participantes.map((p, i) => (
              <li key={i}>
                {p.cpf} — {p.placa_veiculo}
              </li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
}
