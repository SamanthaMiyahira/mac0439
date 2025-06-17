// src/App.js
import React, { useState } from 'react';
import CriarReserva from './components/criarReserva';
// Importe outros componentes quando criar, ex:
// import ConfirmarEntrada from './components/ConfirmarEntrada';
// import ConfirmarSaida from './components/ConfirmarSaida';
// import PagarRecibo from './components/PagarRecibo';

export default function App() {
  const [tela, setTela] = useState('reserva');

  return (
    <div>
      <nav style={{ marginBottom: 20 }}>
        <button onClick={() => setTela('reserva')}>Criar Reserva</button>
        <button onClick={() => setTela('entrada')}>Confirmar Entrada</button>
        <button onClick={() => setTela('saida')}>Confirmar Saída</button>
        <button onClick={() => setTela('pagar')}>Pagar Recibo</button>
      </nav>

      <main>
        {tela === 'reserva' && <CriarReserva />}
        {/* Aqui você adiciona as outras telas quando criar */}
        {tela === 'entrada' && <div>Confirmar Entrada (em desenvolvimento)</div>}
        {tela === 'saida' && <div>Confirmar Saída (em desenvolvimento)</div>}
        {tela === 'pagar' && <div>Pagar Recibo (em desenvolvimento)</div>}
      </main>
    </div>
  );
}
