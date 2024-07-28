document.addEventListener('DOMContentLoaded', function() {
    // Função para adicionar um novo profissional
    document.getElementById('novoProfissionalForm').addEventListener('submit', function(event) {
        event.preventDefault();

        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const documentNumber = document.getElementById('documentNumber').value;
        const specialty = document.getElementById('specialty').value;

        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        const formData = new FormData();
        formData.append('name', name);
        formData.append('email', email);
        formData.append('document', documentNumber);
        formData.append('specialty', specialty);
        formData.append('csrfmiddlewaretoken', csrfToken);

        fetch('/profissionais/novo/', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const tbody = document.querySelector('tbody');
                const newRow = document.createElement('tr');
                newRow.setAttribute('data-id', data.profissional.id);
                newRow.innerHTML = `
                    <td>${data.profissional.name}</td>
                    <td>${data.profissional.email}</td>
                    <td>${data.profissional.document}</td>
                    <td>${data.profissional.specialty}</td>
                    <td>
                        <a 
                        href="#" 
                        class="btn btn-warning btn-sm"
                        data-bs-toggle="modal"
                        data-bs-target="#editarProfissionalModal"
                        data-id="${data.profissional.id}" 
                        data-name="${data.profissional.name}" 
                        data-email="${data.profissional.email}" 
                        data-document="${data.profissional.document}"
                        data-specialty="${data.profissional.specialty}">
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

                const novoProfissionalModal = bootstrap.Modal.getInstance(document.getElementById('novoProfissionalModal'));
                novoProfissionalModal.hide();
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

    // Função para editar um profissional
    document.getElementById('editarProfissionalForm').addEventListener('submit', function(event) {
        event.preventDefault();

        const id = document.getElementById('edit-profissional-id').value;
        const name = document.getElementById('edit-name').value;
        const email = document.getElementById('edit-email').value;
        const documentNumber = document.getElementById('edit-document').value;
        const specialty = document.getElementById('edit-specialty').value;

        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        fetch(`/profissional/editar/${id}/`, {
            method: 'PUT',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: name,
                email: email,
                document: documentNumber,
                specialty: specialty
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Atualiza a linha do profissional na tabela sem recarregar a página
                const row = document.querySelector(`tr[data-id="${id}"]`);
                if (row) {
                    row.innerHTML = `
                        <td>${data.profissional.name}</td>
                        <td>${data.profissional.email}</td>
                        <td>${data.profissional.document}</td>
                        <td>${data.profissional.specialty}</td>
                        <td>
                            <a 
                            href="#" 
                            class="btn btn-warning btn-sm"
                            data-bs-toggle="modal"
                            data-bs-target="#editarProfissionalModal"
                            data-id="${data.profissional.id}" 
                            data-name="${data.profissional.name}" 
                            data-email="${data.profissional.email}" 
                            data-document="${data.profissional.document}"
                            data-specialty="${data.profissional.specialty}">
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

                const editarProfissionalModal = bootstrap.Modal.getInstance(document.getElementById('editarProfissionalModal'));
                editarProfissionalModal.hide();
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

    document.getElementById('editarProfissionalModal').addEventListener('show.bs.modal', function(event) {
        const button = event.relatedTarget;
        const id = button.getAttribute('data-id');
        const name = button.getAttribute('data-name');
        const email = button.getAttribute('data-email');
        const documentNumber = button.getAttribute('data-document');
        const specialty = button.getAttribute('data-specialty');

        document.getElementById('edit-profissional-id').value = id;
        document.getElementById('edit-name').value = name;
        document.getElementById('edit-email').value = email;
        document.getElementById('edit-document').value = documentNumber;
        document.getElementById('edit-specialty').value = specialty;
        
    });

   
    document.querySelector('tbody').addEventListener('click', function(event) {
        const deleteButton = event.target.closest('.delete-button');
        if (deleteButton) {
            event.preventDefault();
            
            if (confirm('Você tem certeza que deseja deletar este profissional?')) {
                const id = deleteButton.getAttribute('data-id');
                const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

                fetch(`/profissional/${id}/excluir`, {
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
                        console.error('Erro ao deletar o profissional.');
                    }
                })
                .catch(error => console.error('Error:', error));
            }
        }
    });
});