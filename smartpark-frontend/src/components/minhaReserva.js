import React, { useState } from 'react';
import { buscarReservaPorCpf, confirmarEntrada, confirmarSaida } from '../api';

export default function MinhaReserva() {
  const [cpf, setCpf] = useState('');
  const [reservas, setReservas] = useState([]);
  const [mensagem, setMensagem] = useState('');
  const [erro, setErro] = useState('');

  const handleBuscar = async () => {
    setMensagem('');
    setErro('');
    setReservas([]);
    if (!cpf) {
      setErro('Por favor, digite o CPF');
      return;
    }
    try {
      const dados = await buscarReservaPorCpf(cpf);
      setReservas(dados);
      if (dados.length === 0) setMensagem('Nenhuma reserva encontrada');
    } catch (e) {
      setErro(e.message);
    }
  };

  const handleEntrada = async (reserva) => {
    setMensagem('');
    setErro('');
    try {
      const res = await confirmarEntrada(reserva.credencial.qrcode, reserva.veiculo.placa);
      setMensagem(res.mensagem || 'Entrada confirmada');
      // Atualiza status localmente
      setReservas((old) =>
        old.map((r) => (r.id === reserva.id ? { ...r, status: 'entrada confirmada' } : r))
      );
    } catch {
      setErro('Erro ao confirmar entrada');
    }
  };

  const handleSaida = async (reserva) => {
    setMensagem('');
    setErro('');
    try {
      const res = await confirmarSaida(reserva.credencial.qrcode, reserva.veiculo.placa);
      setMensagem(res.mensagem || 'Saída confirmada');
      setReservas((old) =>
        old.map((r) => (r.id === reserva.id ? { ...r, status: 'concluida' } : r))
      );
    } catch {
      setErro('Erro ao confirmar saída');
    }
  };

  return (
    <div>
      <h2>Consultar Reservas por CPF</h2>
      <input
        type="text"
        placeholder="Digite seu CPF"
        value={cpf}
        onChange={(e) => setCpf(e.target.value)}
      />
      <button onClick={handleBuscar}>Buscar</button>

      {erro && <p style={{ color: 'red' }}>{erro}</p>}
      {mensagem && <p style={{ color: 'green' }}>{mensagem}</p>}

      {reservas.length > 0 && (
        <div>
          <h3>Reservas encontradas:</h3>
          {reservas.map((reserva) => (
            <div key={reserva.id} style={{ border: '1px solid #ccc', padding: 10, margin: 5 }}>
              <p><strong>ID:</strong> {reserva.id}</p>
              <p><strong>Tipo:</strong> {reserva.tipo}</p>
              <p><strong>Status:</strong> {reserva.status}</p>
              <p><strong>Data:</strong> {reserva.data}</p>
              <p><strong>Placa:</strong> {reserva.veiculo?.placa || 'N/A'}</p>
              <button onClick={() => handleEntrada(reserva)}>Confirmar Entrada</button>
              <button onClick={() => handleSaida(reserva)}>Confirmar Saída</button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
