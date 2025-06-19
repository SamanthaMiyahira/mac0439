const API = 'http://localhost:8000/api';

export async function criarReserva(dadosReserva) {
  try {
    const response = await fetch(`${API}/criar-reserva/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(dadosReserva),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.erro || 'Erro ao criar reserva');
    }

    return data;
  } catch (error) {
    throw error;
  }
}

export async function confirmarEntrada(qrcode, placa) {
  try {
    const response = await fetch(`${API}/confirmar-entrada/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ qrcode, placa }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.erro || 'Erro ao confirmar entrada');
    }

    return data;
  } catch (error) {
    throw error;
  }
}

export async function confirmarSaida(qrcode, placa) {
  try {
    const response = await fetch(`${API}/confirmar-saida/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ qrcode, placa }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.erro || 'Erro ao confirmar saída');
    }

    return data;
  } catch (error) {
    throw error;
  }
}

export async function buscarReservaPorCpf(cpf) {
  try {
    const response = await fetch(`${API}/reservas/cpf/${cpf}`, {
      headers: {
        'Content-Type': 'application/json',
      },
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.erro || 'Erro ao buscar reserva');
    }

    return data;
  } catch (error) {
    throw error;
  }
}



