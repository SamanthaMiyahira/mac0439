import React, { useState } from 'react';
import { buscarReservaPorCpf, confirmarEntrada, confirmarSaida } from '../../api';
import Button from '../Button/Button'; 
import TextInput from '../TextInput/TextInput'; 
import './MinhaReserva.css';
import FilaDeEspera from '../FilaDeEspera/FilaDeEspera';

export default function MinhaReserva() {
    const [cpf, setCpf] = useState('');
    const [reservas, setReservas] = useState([]);
    const [mensagem, setMensagem] = useState('');
    const [erro, setErro] = useState('');
    const [abaAtiva, setAbaAtiva] = useState('reservas'); // 'reservas' ou 'fila'
    const [pesquisou, setPesquisou] = useState(false);

    const handleBuscar = async () => {
        setMensagem('');
        setErro('');
        setReservas([]);
        setPesquisou(false);
        if (!cpf) {
            setErro('Por favor, digite o CPF');
            return;
        }
        try {
            const dados = await buscarReservaPorCpf(cpf);
            const dadosOrdenados = dados.sort((a, b) => b.id - a.id);
            setReservas(dadosOrdenados);
            if (dados.length === 0) setMensagem('Nenhuma reserva encontrada');
            setPesquisou(true);
            setAbaAtiva('reservas'); // sempre abre na aba reservas após busca
        } catch (e) {
            setErro(e.message);
        }
    };

    const handleEntrada = async (reserva) => {
        setMensagem('');
        setErro('');
        try {
            const res = await confirmarEntrada(reserva.credencial.id, reserva.veiculo.placa);
            setMensagem(res.mensagem || 'Entrada confirmada');

            if (res.reserva) {
                setReservas(old =>
                    old.map(r => (r.id === res.reserva.id ? res.reserva : r))
                );
            } else {
                setReservas(old =>
                    old.map(r => (r.id === reserva.id ? { ...r, status: 'entrada confirmada' } : r))
                );
            }
        } catch (e) {
            setErro(e.message || 'Erro ao confirmar entrada');
        }
    };

    const handleSaida = async (reserva) => {
        setMensagem('');
        setErro('');
        try {
            const res = await confirmarSaida(reserva.credencial.id, reserva.veiculo.placa);
            setMensagem(res.mensagem || 'Saída confirmada');

            if (res.reserva) {
                setReservas(old =>
                    old.map(r => (r.id === res.reserva.id ? res.reserva : r))
                );
            } else {
                setReservas(old =>
                    old.map(r => (r.id === reserva.id ? { ...r, status: 'concluida' } : r))
                );
            }
        } catch {
            setErro('Erro ao confirmar saída');
        }
    };

    return (
        <div className="minha-reserva-container">
            <h2>Consultar minhas reservas</h2>
            <div className="minha-reserva-input-row">
                <TextInput
                    placeholder="Digite seu CPF"
                    value={cpf}
                    onChange={(e) => setCpf(e.target.value)}
                />
                <Button onClick={handleBuscar}>Buscar</Button>
            </div>

            {erro && <p className="minha-reserva-erro">{erro}</p>}
            {mensagem && <p className="minha-reserva-mensagem">{mensagem}</p>}

            {pesquisou && (
                <>
                    <div className="abas-container" style={{ marginTop: 20 }}>
                        <button
                            className={abaAtiva === 'reservas' ? 'aba-ativa' : ''}
                            onClick={() => setAbaAtiva('reservas')}
                        >
                            Reservas
                        </button>
                        <button
                            className={abaAtiva === 'fila' ? 'aba-ativa' : ''}
                            onClick={() => setAbaAtiva('fila')}
                        >
                            Fila de Espera
                        </button>
                    </div>

                    {abaAtiva === 'reservas' && reservas.length > 0 && (
                        <div className="minha-reserva-lista">
                            <h3>Reservas encontradas:</h3>
                            {reservas.map((reserva) => (
                                <div key={reserva.id} className="minha-reserva-card">
                                    <p><strong>ID:</strong> {reserva.id}</p>
                                    <p><strong>Tipo da reserva:</strong> {reserva.tipo}</p>
                                    <p><strong>Status:</strong> {reserva.status}</p>
                                    <p><strong>Data:</strong> {reserva.data}</p>
                                    <p><strong>Placa do veículo:</strong> {reserva.veiculo?.placa || 'N/A'}</p>
                                    <p><strong>Vaga:</strong> {reserva.vaga ? `${reserva.vaga.tipo} - ${reserva.vaga.localizacao}` : 'N/A'}</p>
                                    <p><strong>Credencial (QR Code):</strong> {reserva.credencial?.qrcode || 'N/A'}</p>
                                    <p><strong>Status da Credencial:</strong> {reserva.credencial?.status || 'N/A'}</p>
                                    {reserva.status !== 'cancelada' && reserva.status !== 'concluida' && (
                                        <>
                                            {reserva.credencial?.status === 'ativo' ? (
                                                <Button onClick={() => handleEntrada(reserva)}>Confirmar Entrada</Button>
                                            ) : (
                                                <Button onClick={() => handleSaida(reserva)}>Confirmar Saída</Button>
                                            )}
                                        </>
                                    )}
                                </div>
                            ))}
                        </div>
                    )}

                    {abaAtiva === 'fila' && <FilaDeEspera cpf={cpf} />}
                </>
            )}
        </div>
    );
}
