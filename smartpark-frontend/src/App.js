// src/App.js
import React, { useState } from 'react';
import CriarReserva from './components/criarReserva';
import MinhaReserva from './components/minhaReserva'; 

export default function App() {
  const [tela, setTela] = useState('reserva');
  const [idReserva, setIdReserva] = useState(null); 

  return (
    <div>
      <nav style={{ marginBottom: 20 }}>
        <button onClick={() => setTela('reserva')}>Criar Reserva</button>
        <button onClick={() => setTela('minha')}>Minha Reserva</button>
      </nav>

      <main>
        {tela === 'reserva' && <CriarReserva setIdReserva={setIdReserva} />}
        {tela === 'minha' && <MinhaReserva idReserva={idReserva} />}
      </main>
    </div>
  );
}
