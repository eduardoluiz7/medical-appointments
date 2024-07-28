document.addEventListener('DOMContentLoaded', function() {
    // Função para adicionar um novo paciente
    document.getElementById('novoPacienteForm').addEventListener('submit', function(event) {
        event.preventDefault();

        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const documentNumber = document.getElementById('documentNumber').value;

        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        const formData = new FormData();
        formData.append('name', name);
        formData.append('email', email);
        formData.append('document', documentNumber);
        formData.append('csrfmiddlewaretoken', csrfToken);

        fetch('/pacientes/novo/', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Atualizar a lista de pacientes na tabela sem recarregar a página
                const tbody = document.querySelector('tbody');
                const newRow = document.createElement('tr');
                newRow.setAttribute('data-id', data.paciente.id);
                newRow.innerHTML = `
                    <td>${data.paciente.name}</td>
                    <td>${data.paciente.email}</td>
                    <td>${data.paciente.document}</td>
                    <td>
                        <a 
                        href="#" 
                        class="btn btn-warning btn-sm"
                        data-bs-toggle="modal"
                        data-bs-target="#editarPacienteModal"
                        data-id="${data.paciente.id}" 
                        data-name="${data.paciente.name}" 
                        data-email="${data.paciente.email}" 
                        data-document="${data.paciente.document}">
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

                const novoPacienteModal = bootstrap.Modal.getInstance(document.getElementById('novoPacienteModal'));
                novoPacienteModal.hide();
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

    // Função para editar um paciente
    document.getElementById('editarPacienteForm').addEventListener('submit', function(event) {
        event.preventDefault();

        const id = document.getElementById('edit-paciente-id').value;
        const name = document.getElementById('edit-name').value;
        const email = document.getElementById('edit-email').value;
        const documentNumber = document.getElementById('edit-document').value;

        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        fetch(`/paciente/editar/${id}/`, {
            method: 'PUT',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: name,
                email: email,
                document: documentNumber
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Atualiza a linha do paciente na tabela sem recarregar a página
                const row = document.querySelector(`tr[data-id="${id}"]`);
                if (row) {
                    row.innerHTML = `
                        <td>${data.paciente.name}</td>
                        <td>${data.paciente.email}</td>
                        <td>${data.paciente.document}</td>
                        <td>
                            <a 
                            href="#" 
                            class="btn btn-warning btn-sm"
                            data-bs-toggle="modal"
                            data-bs-target="#editarPacienteModal"
                            data-id="${data.paciente.id}" 
                            data-name="${data.paciente.name}" 
                            data-email="${data.paciente.email}" 
                            data-document="${data.paciente.document}">
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

                const editarPacienteModal = bootstrap.Modal.getInstance(document.getElementById('editarPacienteModal'));
                editarPacienteModal.hide();
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

    document.getElementById('editarPacienteModal').addEventListener('show.bs.modal', function(event) {
        const button = event.relatedTarget;
        const id = button.getAttribute('data-id');
        const name = button.getAttribute('data-name');
        const email = button.getAttribute('data-email');
        const documentNumber = button.getAttribute('data-document');

        document.getElementById('edit-paciente-id').value = id;
        document.getElementById('edit-name').value = name;
        document.getElementById('edit-email').value = email;
        document.getElementById('edit-document').value = documentNumber;
    });

   
    document.querySelector('tbody').addEventListener('click', function(event) {
        const deleteButton = event.target.closest('.delete-button');
        if (deleteButton) {
            event.preventDefault();
            
            if (confirm('Você tem certeza que deseja deletar este paciente?')) {
                const id = deleteButton.getAttribute('data-id');
                const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

                fetch(`/paciente/${id}/excluir`, {
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
                        console.error('Erro ao deletar o paciente.');
                    }
                })
                .catch(error => console.error('Error:', error));
            }
        }
    });
});