// src/App.js
import React, { useState } from 'react';
import CriarReserva from './components/CriarReserva/CriarReserva';
import MinhaReserva from './components/MinhaReserva/MinhaReserva'; 
import Button from './components/Button/Button';

export default function App() {
  const [tela, setTela] = useState('reserva');
  const [idReserva, setIdReserva] = useState(null); 

  return (
    <div>
      <nav style={{ marginBottom: 20 }}>
        <Button onClick={() => setTela('reserva')}>Criar Reserva</Button>
        <Button onClick={() => setTela('minha')}>Minha Reserva</Button>
      </nav>

      <main>
        {tela === 'reserva' && <CriarReserva setIdReserva={setIdReserva} />}
        {tela === 'minha' && <MinhaReserva idReserva={idReserva} />}
      </main>
    </div>
  );
}
