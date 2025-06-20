import React, { useState } from 'react';
import { buscarFilaEsperaPorCpf } from '../../api';
import './FilaDeEspera.css';

export default function FilaDeEspera({ cpf }) {
  const [fila, setFila] = useState([]);
  const [erro, setErro] = useState('');
  const [loading, setLoading] = useState(false);

    const carregarFila = async () => {
        setErro('');
        setLoading(true);
        try {
            const dados = await buscarFilaEsperaPorCpf(cpf);
            setFila(dados);
        } catch (e) {
            if (e.message.includes('404')) {
            setFila([]);  
            } else {
            
            setFila([]);
            }
        }
        setLoading(false);
    };

  React.useEffect(() => {
    if (cpf) {
      carregarFila();
    }
  }, [cpf]);

  if (!cpf) return null;

  return (
    <div className="fila-espera-container">
      <h3>Fila de Espera</h3>
      {loading && <p>Carregando...</p>}
      {erro && <p className="erro">{erro}</p>}
      {!loading && fila.length === 0 && <p>Você não está na fila de espera.</p>}

      {fila.map((item) => (
        <div key={item.id} className={`fila-item status-${item.status}`}>
          <p><strong>Status:</strong> {item.status}</p>
          <p><strong>Prioridade:</strong> {item.prioridade}</p>
          <p><strong>Data da solicitação:</strong> {new Date(item.data_hora).toLocaleString()}</p>
          <p><strong>Data desejada para reserva:</strong> {item.data_reserva ? new Date(item.data_reserva).toLocaleDateString() : 'N/A'}</p>
          {item.reserva_id && <p><em>Reserva criada (ID: {item.reserva_id})</em></p>}
        </div>
      ))}
    </div>
  );
}
