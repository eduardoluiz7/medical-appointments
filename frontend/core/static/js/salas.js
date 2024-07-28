document.addEventListener('DOMContentLoaded', function() {
    // Função para adicionar um novo sala
    document.getElementById('novoSalaForm').addEventListener('submit', function(event) {
        event.preventDefault();

        const name = document.getElementById('name').value;

        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        const formData = new FormData();
        formData.append('name', name);
        formData.append('csrfmiddlewaretoken', csrfToken);

        fetch('/salas/novo/', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Atualizar a lista de salas na tabela sem recarregar a página
                const tbody = document.querySelector('tbody');
                const newRow = document.createElement('tr');
                newRow.setAttribute('data-id', data.sala.id);
                newRow.innerHTML = `
                    <td>${data.sala.id}</td>
                    <td>${data.sala.name}</td>
                    <td>
                        <a 
                        href="#" 
                        class="btn btn-warning btn-sm"
                        data-bs-toggle="modal"
                        data-bs-target="#editarPacienteModal"
                        data-id="${data.sala.id}" 
                        data-name="${data.sala.name}" 
                        >
                            <i class="bi bi-pencil"></i>
                            Editar
                        </a>
                        <a href="#" class="btn btn-danger btn-sm">
                            <i class="bi bi-trash"></i>
                            Deletar
                        </a>
                    </td>
                `;
                tbody.appendChild(newRow);

                const novoSalaModal = bootstrap.Modal.getInstance(document.getElementById('novoSalaModal'));
                novoSalaModal.hide();
            } else {
                const errors = data.errors;
                for (const [field, messages] of Object.entries(errors)) {
                    const inputField = document.getElementById(field);
                    const errorDiv = document.createElement('div');
                    errorDiv.className = 'invalid-feedback';
                    errorDiv.innerText = messages.join(' ');
                    inputField.classList.add('is-invalid');
                    inputField.parentNode.appendChild(errorDiv);
                }
            }
        })
        .catch(error => console.error('Error:', error));
    });

    // Função para editar um sala
    document.getElementById('editarSalaForm').addEventListener('submit', function(event) {
        event.preventDefault();

        const id = document.getElementById('edit-sala-id').value;
        const name = document.getElementById('edit-name').value;

        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        fetch(`/salas/editar/${id}/`, {
            method: 'PUT',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: name
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Atualiza a linha do sala na tabela sem recarregar a página
                const row = document.querySelector(`tr[data-id="${id}"]`);
                if (row) {
                    row.innerHTML = `
                        <td>${id}</td>
                        <td>${data.sala.name}</td>
                        <td>
                            <a 
                            href="#" 
                            class="btn btn-warning btn-sm"
                            data-bs-toggle="modal"
                            data-bs-target="#editarPacienteModal"
                            data-id="${data.sala.id}" 
                            data-name="${data.sala.name}" 
                           >
                                <i class="bi bi-pencil"></i>
                                Editar
                            </a>
                            <a href="#" class="btn btn-danger btn-sm">
                                <i class="bi bi-trash"></i>
                                Deletar
                            </a>
                        </td>
                    `;
                } else {
                    console.error(`Linha com ID ${id} não encontrada.`);
                }

                const editarSalaModal = bootstrap.Modal.getInstance(document.getElementById('editarSalaModal'));
                editarSalaModal.hide();
            } else {
                const errors = data.errors;
                for (const [field, messages] of Object.entries(errors)) {
                    const inputField = document.getElementById(`edit-${field}`);
                    const errorDiv = document.createElement('div');
                    errorDiv.className = 'invalid-feedback';
                    errorDiv.innerText = messages.join(' ');
                    inputField.classList.add('is-invalid');
                    inputField.parentNode.appendChild(errorDiv);
                }
            }
        })
        .catch(error => console.error('Error:', error));
    });

    document.getElementById('editarSalaModal').addEventListener('show.bs.modal', function(event) {
        const button = event.relatedTarget;
        const id = button.getAttribute('data-id');
        const name = button.getAttribute('data-name');

        document.getElementById('edit-sala-id').value = id;
        document.getElementById('edit-name').value = name;

    });

   
    document.querySelector('tbody').addEventListener('click', function(event) {
        const deleteButton = event.target.closest('.delete-button');
        if (deleteButton) {
            event.preventDefault();
            
            if (confirm('Você tem certeza que deseja deletar este sala?')) {
                const id = deleteButton.getAttribute('data-id');
                const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

                fetch(`/salas/${id}/excluir`, {
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
                        console.error('Erro ao deletar o sala.');
                    }
                })
                .catch(error => console.error('Error:', error));
            }
        }
    });
});