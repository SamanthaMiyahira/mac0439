export async function criarReserva(dadosReserva) {
  try {
    const response = await fetch('http://localhost:8000/api/criar-reserva/', {
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
