import React, { useState } from 'react';
import { listarRecibosPendentes, pagarRecibo } from '../../api';
import Button from '../Button/Button';
import TextInput from '../TextInput/TextInput';
import './Pagamentos.css';

export default function Pagamentos() {
  const [cpf, setCpf] = useState('');
  const [recibos, setRecibos] = useState([]);
  const [erro, setErro] = useState('');
  const [mensagem, setMensagem] = useState('');

  const handleBuscar = async () => {
    setErro('');
    setMensagem('');
    try {
      const dados = await listarRecibosPendentes(cpf);
      setRecibos(dados);
      if (dados.length === 0) {
        setMensagem('Nenhum recibo pendente.');
      }
    } catch (e) {
      setErro(e.message);
    }
  };

  const handlePagar = async (reciboId) => {
    try {
      await pagarRecibo({ cpf, recibo_id: reciboId, metodo_pagamento: 'PIX' });
      setMensagem('Pagamento realizado com sucesso!');
      setRecibos(prev => prev.filter(r => r._id !== reciboId));
    } catch (e) {
      setErro(e.message);
    }
  };

  return (
    <div className="pagamentos-container">
        <h2>Pagamentos pendentes</h2>
        <div className="cpf-buscar-container">
            <TextInput
            placeholder="Digite seu CPF"
            value={cpf}
            onChange={(e) => setCpf(e.target.value)}
            />
            <Button onClick={handleBuscar}>Buscar recibos</Button>
        </div>

      {erro && <p className="pagamentos-erro">{erro}</p>}
      {mensagem && <p className="pagamentos-mensagem">{mensagem}</p>}

      {recibos.map((recibo) => (
        <div key={recibo._id} className="pagamento-card">
          <p><strong>ID:</strong> {recibo._id}</p>
          <p><strong>Valor:</strong> R$ {recibo.valor.toFixed(2)}</p>
          <p><strong>Status:</strong> {recibo.status}</p>
          <p><strong>Data:</strong> {new Date(recibo.data_hora).toLocaleString()}</p>
          <p><strong>Visitante:</strong> {recibo.visitante?.nome} - {recibo.visitante?.cpf}</p>
          <Button onClick={() => handlePagar(recibo._id)}>Pagar via PIX</Button>
        </div>
      ))}
    </div>
  );
}
