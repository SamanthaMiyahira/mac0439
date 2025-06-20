import React, { useState } from 'react';
import './MapaEstacionamento.css';

export default function MapaEstacionamento({ vagasData, onSelecionar }) {
    // Se quiser, passe as vagas por props, senão use aqui mesmo:
    const [vagas, setVagas] = useState(vagasData || [
        { id: 1, status: 'livre' },
        { id: 2, status: 'ocupada' },
        { id: 3, status: 'livre' },
        { id: 4, status: 'livre' },
        { id: 5, status: 'ocupada' },
        { id: 6, status: 'livre' },
        { id: 7, status: 'livre' },
        { id: 8, status: 'livre' }
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
        </div>

    );
}
