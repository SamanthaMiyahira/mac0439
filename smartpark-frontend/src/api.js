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

export async function confirmarEntrada(credencial_id, placa) {
  try {
    const response = await fetch(`${API}/confirmar-entrada/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ credencial_id, placa }),
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

export async function confirmarSaida(credencial_id, placa) {
  try {
    const response = await fetch(`${API}/confirmar-saida/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ credencial_id, placa }),
    });

    console.log('Resposta status:', response.status);
    const data = await response.json();
    console.log('Resposta data:', data);

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
    const cpfUrl = encodeURIComponent(cpf);  
    const response = await fetch(`${API}/reservas/cpf/${cpfUrl}/`, {
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

export async function criarEvento(evento) {
  const response = await fetch(`${API}/criar-evento/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(evento),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.erro || 'Erro ao criar evento');
  }

  return response.json();
}

export async function buscarEventos() {
  const res = await fetch("http://localhost:8000/api/eventos/");
  if (!res.ok) throw new Error("Erro ao buscar eventos");
  return res.json();
}






