## Como criar a interface React do SmartPark

A interface do SmartPark foi desenvolvida com React e está organizada da seguinte forma:

- Pasta src/components/

Contém os componentes React que representam as diferentes partes da interface. Atualmente, temos o componente criarReserva.js, responsável pelo formulário e lógica de criação de reservas.

- Arquivo src/api.js

Centraliza as chamadas à API do backend. Por exemplo, a função criarReserva faz a requisição POST para o endpoint que cria a reserva no servidor Django.

- Arquivo src/App.js

É o componente principal que gerencia a tela única (single-page) da aplicação. Ele importa o componente criarReserva e renderiza essa interface. Também pode ser usado para adicionar outros componentes e botões para navegar entre funcionalidades futuras.

## Como usar

Para iniciar a aplicação, execute npm start na raiz do frontend.

A interface abrirá no navegador em http://localhost:3000 e mostrará a tela única com o formulário de criação de reserva.

O componente criarReserva envia os dados para o backend usando as funções definidas em api.js.