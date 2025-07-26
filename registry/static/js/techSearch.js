const input = document.getElementById("searchInput");
const resultsContainer = document.getElementById("results");
const messageContainer = document.getElementById("messageContainer");  // Elemento onde a mensagem será exibida
const csrfToken = document.querySelector('meta[name="csrf-token"]').content;

input.addEventListener("input", () => {
    const query = input.value;

    fetch(`/b-tech/?query=${encodeURIComponent(query)}`)
    .then(response => {
        // Verifica se a resposta é JSON
        if (response.ok && response.headers.get('Content-Type').includes('application/json')) {
            return response.json();
        } else {
            throw new Error('Resposta não é JSON');
        }
    }) 
    .then(data => {
        resultsContainer.innerHTML = ""; // Limpa os resultados anteriores
        messageContainer.innerHTML = ""; // Limpa qualquer mensagem anterior

        if (data.message) {
            // Exibe a mensagem de erro ou sucesso
            messageContainer.innerHTML = `<p>${data.message}</p>`;
        }
        
        // input.value = query;

        if (data.clientes.length > 0) {
            data.clientes.forEach(cliente => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${cliente.id}</td>
                    <td>${cliente.name || "N/A"}</td>
                    <td>${cliente.WorkPhone || "N/A"}</td>
                    <td>${cliente.PersonalPhone || "N/A"}</td>
                    <td> 
                        <form action="/pessoa/buscar/${cliente.id}/" method="GET" style="display:inline-block;">
                            <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                            <button type="submit" class="btn" style="background-color: #117027;color: white;">Visualizar</button>
                        </form>
                        <form action="/pessoa/atualizar/${cliente.id}/" method="GET" style="display:inline-block;">
                            <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                            <button type="submit" class="btn" style="background-color: #117027;color: white;">Editar</button>
                        </form>
                        <form action="/pessoa/deletar/${cliente.id}/" method="POST" style="display:inline-block;">
                            <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                            <button type="submit" class="btn" style="background-color: rgb(139, 16, 16);color: white;" onclick="return confirm('Tem certeza que deseja deletar este cliente?')">Deletar</button>
                        </form>
                    </td>
                `;
                resultsContainer.appendChild(row);
            });
        }
        paginationContainer.innerHTML = ""; // Limpa os links de paginação anteriores  search_client
        // search_client.innerHTML = ""; // Limpa os links de paginação anteriores

        if (data.pagination) {
            const { has_previous, has_next, previous_page, next_page } = data.pagination;
            if (has_previous) {
                const prevLink = document.createElement("a");
                // Inclui o parâmetro 'query' na URL para a navegação anterior
                prevLink.href = `/prsn/?page=${previous_page}&query=${encodeURIComponent(query)}`;
                prevLink.textContent = "Anterior";
                prevLink.className = "pagination-link";
                paginationContainer.appendChild(prevLink);
            }
            
            if (has_next) {
                const nextLink = document.createElement("a");
                // Inclui o parâmetro 'query' na URL para a navegação próxima
                nextLink.href = `/prsn/?page=${next_page}&query=${encodeURIComponent(query)}`;
                nextLink.textContent = "Próximo";
                nextLink.className = "pagination-link";
                paginationContainer.appendChild(nextLink);
            }
        }
    })
    .catch(error => console.error("Erro ao buscar clientes:", error));
});