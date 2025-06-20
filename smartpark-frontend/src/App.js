// src/App.js
import React, { useState } from 'react';
import CriarReserva from './components/CriarReserva/CriarReserva';
import MinhaReserva from './components/MinhaReserva/MinhaReserva'; 
import Button from './components/Button/Button';
import CriarEvento from './components/CriarEvento/CriarEvento';
import Eventos from './components/Eventos/Eventos';
import Pagamentos from './components/Pagamentos/Pagamentos';

export default function App() {
  const [tela, setTela] = useState('reserva');
  const [idReserva, setIdReserva] = useState(null); 

  return (
    <div>
      <nav style={{ marginBottom: 20 }}>
        <Button onClick={() => setTela('reserva')}>Criar reserva</Button>
        <Button onClick={() => setTela('minha')}>Minhas reservas</Button>
        <Button onClick={() => setTela('evento')}>Criar evento</Button>
        <Button onClick={() => setTela('eventos')}>Eventos</Button>
        <Button onClick={() => setTela('pagamentos')}>Pagamentos</Button>
      </nav>

      <main>
        {tela === 'reserva' && <CriarReserva setIdReserva={setIdReserva} />}
        {tela === 'minha' && <MinhaReserva idReserva={idReserva} />}
        {tela === 'evento' && <CriarEvento />}
        {tela === 'eventos' && <Eventos />}
        {tela === 'pagamentos' && <Pagamentos />}
      </main>
    </div>
  );
}
