import React, { useState } from 'react';
import { criarReserva } from '../../api';
import './CriarReserva.css';
import Button from '../Button/Button';
import TextInput from '../TextInput/TextInput';
import Select from '../Select/Select';

export default function CriarReserva({ setTela, setIdReserva }) {
  const [cpf, setCpf] = useState('');
  const [data, setData] = useState('');
  const [tipo, setTipo] = useState('recorrente');
  const [mensagem, setMensagem] = useState(null);
  const [erro, setErro] = useState(null);

  // Função para mascarar o CPF enquanto digita
  function formatarCpf(valor) {
    // Remove tudo que não for dígito
    valor = valor.replace(/\D/g, '');
    // Aplica a máscara
    if (valor.length <= 3) return valor;
    if (valor.length <= 6) return valor.replace(/(\d{3})(\d+)/, '$1.$2');
    if (valor.length <= 9) return valor.replace(/(\d{3})(\d{3})(\d+)/, '$1.$2.$3');
    return valor.replace(/(\d{3})(\d{3})(\d{3})(\d+)/, '$1.$2.$3-$4');
  }

  // onChange do input
  const handleCpfChange = (e) => {
    setCpf(formatarCpf(e.target.value));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMensagem(null);
    setErro(null);

    const dados = { cpf, data, tipo };
    console.log('Enviando para backend:', dados);

    try {
      const resultado = await criarReserva(dados);
      setMensagem(resultado.mensagem || 'Reserva criada com sucesso!');
    } catch (err) {
      console.error('Erro ao criar reserva:', err);
      setErro(err.message);
    }
  };

  return (
    <div className="criar-reserva-container">
      <h2>Criar Reserva</h2>
      <form className="criar-reserva-form" onSubmit={handleSubmit}>
        <div>
          <label>CPF: </label>
          <TextInput
            maxLength={14}
            value={cpf}
            onChange={handleCpfChange}
            placeholder="000.000.000-00"
            required
          />
        </div>
        <div>
          <label>Data (DD-MM-AAAA): </label>
          <TextInput type="date" value={data} onChange={e => setData(e.target.value)} required />
        </div>
        <div>
          <label>Tipo: </label>
          <Select value={tipo} onChange={e => setTipo(e.target.value)}>
            <option value="eventual">Eventual</option>
            <option value="recorrente">Recorrente</option>
          </Select>
        </div>
        <div>
          <label>Selecione a vaga: </label>
          <Button
            type="button"
            onClick={() => setTela('mapa')}
          >
            Abrir Mapa
          </Button>
        </div>
        <Button type="submit">Criar Reserva</Button>
      </form>
      {mensagem && <p className="criar-reserva-mensagem">{mensagem}</p>}
      {erro && <p className="criar-reserva-erro">{erro}</p>}
    </div>
  );
}
