import React, { useState } from 'react';
import './MapaEstacionamento.css';
import Button from '../Button/Button';

export default function MapaEstacionamento({ vagasData, onSelecionar, setTela }) {
    // Se quiser, passe as vagas por props, senão use aqui mesmo:
    const [vagas, setVagas] = useState(vagasData || [
        { id: 1, status: 'livre' },
        { id: 2, status: 'ocupada' },
        { id: 3, status: 'livre' },
        { id: 4, status: 'livre' },
        { id: 5, status: 'ocupada' },
        { id: 6, status: 'livre' },
        { id: 7, status: 'livre' },
        { id: 8, status: 'livre' },
        { id: 9, status: 'livre' },
        { id: 10, status: 'livre' },
        { id: 11, status: 'livre' },
        { id: 12, status: 'ocupada' },
        { id: 13, status: 'livre' },
        { id: 14, status: 'livre' },
        { id: 15, status: 'livre' },
        { id: 16, status: 'livre' },
        { id: 17, status: 'livre' },
        { id: 18, status: 'livre' },
        { id: 19, status: 'livre' },
        { id: 20, status: 'livre' }
    ]);
    const [vagaSelecionada, setVagaSelecionada] = useState(null);

    function selecionarVaga(id) {
        setVagaSelecionada(id);
        if (onSelecionar) onSelecionar(id);
    }

    return (
        <div>
            <h2>Selecione uma vaga</h2>
            <div className="estacionamento-grid">
                {vagas.map((vaga) => (
                    <button
                        key={vaga.id}
                        className={`vaga ${vaga.status} ${vagaSelecionada === vaga.id ? 'selecionada' : ''}`}
                        disabled={vaga.status === 'ocupada'}
                        onClick={() => selecionarVaga(vaga.id)}
                    >
                        {vaga.id}
                    </button>
                ))}
            </div>
            {vagaSelecionada && (
                <div style={{ textAlign: 'center', marginTop: 16 }}>
                    <strong>Vaga selecionada:</strong> {vagaSelecionada}
                </div>
            )}
            <Button type="button" onClick={() => setTela('reserva')}>Voltar</Button>
        </div>

    );
}
