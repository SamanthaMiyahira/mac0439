// src/components/criarReserva.js
import React, { useState } from 'react';
import { criarReserva } from '../api';

export default function CriarReserva() {
  const [cpf, setCpf] = useState('');
  const [data, setData] = useState('');
  const [tipo, setTipo] = useState('eventual'); // ou 'mensal' etc
  const [mensagem, setMensagem] = useState(null);
  const [erro, setErro] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMensagem(null);
    setErro(null);

    try {
      const resultado = await criarReserva({ cpf, data, tipo });
      setMensagem(resultado.mensagem || 'Reserva criada com sucesso!');
    } catch (err) {
      setErro(err.message);
    }
  };

  return (
    <div>
      <h2>Criar Reserva</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>CPF: </label>
          <input type="text" value={cpf} onChange={(e) => setCpf(e.target.value)} required />
        </div>
        <div>
          <label>Data (YYYY-MM-DD): </label>
          <input type="date" value={data} onChange={(e) => setData(e.target.value)} required />
        </div>
        <div>
          <label>Tipo: </label>
          <select value={tipo} onChange={(e) => setTipo(e.target.value)}>
            <option value="eventual">Eventual</option>
            <option value="mensal">Mensal</option>
          </select>
        </div>
        <button type="submit">Criar Reserva</button>
      </form>

      {mensagem && <p style={{ color: 'green' }}>{mensagem}</p>}
      {erro && <p style={{ color: 'red' }}>{erro}</p>}
    </div>
  );
}
