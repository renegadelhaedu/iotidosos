let alertIntervalId = null;

function playAlertSound() {
    try {
        const audioContext = new AudioContext();
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();

        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);

        oscillator.frequency.setValueAtTime(800, audioContext.currentTime);
        gainNode.gain.setValueAtTime(0.2, audioContext.currentTime);

        oscillator.start();
        oscillator.stop(audioContext.currentTime + 0.2);
    } catch (error) {
        console.warn('Não foi possível reproduzir som:', error);
    }
}

const socket = io();
const statusDot = document.getElementById('statusDot');
const statusText = document.getElementById('statusText');

socket.on('connect', function() {
    statusDot.className = 'status-dot connected';
    statusText.textContent = 'Conectado ao servidor';

});

socket.on('disconnect', function() {
    statusDot.className = 'status-dot disconnected';
    statusText.textContent = 'Desconectado do servidor';
});

socket.on('novo_alerta', function(data) {
    const houseId = data.casa;
    const alertType = data.alerta;

    const houseElement = document.getElementById(`house${houseId}`);
    if (houseElement) {
        playAlertSound();
        alertIntervalId = setInterval(playAlertSound, 2000);

        houseElement.classList.remove('normal');
        houseElement.classList.add('alert');
        houseElement.querySelector('.house-status').textContent = alertType;
    }

});



function mostrarDetalhes(idpessoa, numcasa) {

    var house = document.getElementById('house' + numcasa);

    if (!house) {
        console.error('Essa house não existe para o ID:', numcasa);
        return;
    }
    if(house.classList.contains('alert')){
        clearInterval(alertIntervalId);
        alertIntervalId = null;

        house.classList.remove('alert');
        house.classList.add('normal');
        house.querySelector('.house-status').textContent = 'Casa ' + numcasa;
    }else{
        const modal = document.getElementById('myModal');
        const modalBody = document.getElementById('modal-body');

        modalBody.innerHTML = 'Carregando detalhes...';
        modal.style.display = 'block';


        fetch('pessoa/modal/'+ idpessoa)
            .then(response => {

                if (!response.ok) {
                    throw new Error('Erro na requisição');
                }
                return response.text();
            })
            .then(data => {

                modalBody.innerHTML = data;
            })
            .catch(error => {
                console.error('Erro:', error);
                modalBody.innerHTML = 'Não foi possível carregar os detalhes.';
            });
    }


}

function fecharModal() {
    const modal = document.getElementById('myModal');
    modal.style.display = 'none';
}


window.onclick = function(event) {
    const modal = document.getElementById('myModal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}


