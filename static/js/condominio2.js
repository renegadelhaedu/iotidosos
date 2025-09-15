document.addEventListener('DOMContentLoaded', function() {
    const housesGrid = document.getElementById('housesGrid');
    const alertsContainer = document.getElementById('alertsContainer');
    const statusDot = document.getElementById('statusDot');
    const statusText = document.getElementById('statusText');
    const lastUpdate = document.getElementById('lastUpdate');

    // Conectar ao servidor Socket.IO
    const socket = io();

    // Gerar 12 casas (retângulos verdes)
    for (let i = 1; i <= 15; i++) {
        const house = document.createElement('div');
        house.className = 'house normal';
        house.id = `house-${i}`;
        house.innerHTML = `
            <div class="house-id">${i}</div>
            <div class="house-status">Normal</div>
        `;

        // Adicionar evento de clique para resetar o status
        house.addEventListener('click', function() {
            if (this.classList.contains('alert')) {
                this.classList.remove('alert');
                this.classList.add('normal');
                this.querySelector('.house-status').textContent = 'Normal';
            }
        });

        housesGrid.appendChild(house);
    }

    // Evento de conexão
    socket.on('connect', function() {
        statusDot.className = 'status-dot connected';
        statusText.textContent = 'Conectado ao servidor';
        updateLastUpdateTime();
    });

    // Evento de desconexão
    socket.on('disconnect', function() {
        statusDot.className = 'status-dot disconnected';
        statusText.textContent = 'Desconectado do servidor';
    });

    // Evento para receber alertas
    socket.on('novo_alerta', function(data) {
        const houseId = data.casa;
        const alertType = data.alerta;

        // Atualizar a casa correspondente
        const houseElement = document.getElementById(`house-${houseId}`);
        if (houseElement) {
            houseElement.classList.remove('normal');
            houseElement.classList.add('alert');
            houseElement.querySelector('.house-status').textContent = 'Alerta!';
        }

        // Adicionar ao histórico de alertas
        const alertItem = document.createElement('div');
        alertItem.className = 'alert-item';
        alertItem.innerHTML = `
            <div>
                <strong>Casa ${houseId}</strong>: ${alertType}
            </div>
            <div class="alert-time">${new Date().toLocaleTimeString()}</div>
        `;

        alertsContainer.prepend(alertItem);

        // Manter apenas os 10 alertas mais recentes
        if (alertsContainer.children.length > 10) {
            alertsContainer.removeChild(alertsContainer.lastChild);
        }

        updateLastUpdateTime();
    });

    function updateLastUpdateTime() {
        lastUpdate.textContent = `Última atualização: ${new Date().toLocaleTimeString()}`;
    }
});