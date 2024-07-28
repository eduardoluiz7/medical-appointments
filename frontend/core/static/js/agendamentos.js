document.addEventListener('DOMContentLoaded', function() {

    document.querySelector('tbody').addEventListener('click', function(event) {
        const cancelButton = event.target.closest('.cancel-button');
        if (cancelButton){
            event.preventDefault();

            if (confirm('Você tem certeza que deseja cancelar este agendamento?')) {
                const id = cancelButton.getAttribute('data-id');
                const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

                fetch(`/agendamento/editar/${id}/`, {
                    method: 'PATCH',
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'Content-Type': 'application/json'
                        },
                    body: JSON.stringify({
                        status: "CANCELED"
                    })
                    })
                    .then(response => response.json())
                    .catch(error => console.error('Error:', error));
            }
        }
    })

    // delete agendamento
    document.querySelector('tbody').addEventListener('click', function(event) {
        const deleteButton = event.target.closest('.delete-button');
        if (deleteButton) {
            event.preventDefault();
            
            if (confirm('Você tem certeza que deseja deletar este agendamento?')) {
                const id = deleteButton.getAttribute('data-id');
                const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

                fetch(`/agendamento/${id}/excluir`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json'
                    }
                })
                .then(response => {
                    if (response.ok) {
                        const row = document.querySelector(`tr[data-id="${id}"]`);
                        if (row) {
                            row.remove();
                        }
                    } else {
                        console.error('Erro ao deletar o agendamento.');
                    }
                })
                .catch(error => console.error('Error:', error));
            }
        }
    });
});