const input = document.getElementById("searchInput");
const resultsContainer = document.getElementById("results");
const messageContainer = document.getElementById("messageContainer");  // Elemento onde a mensagem será exibida
const csrfToken = document.querySelector('meta[name="csrf-token"]').content;
let paginationContainer = document.getElementById("paginationContainer");
input.addEventListener("input", () => {
    const query = input.value;

    fetch(`/b-prsn/?query=${encodeURIComponent(query)}`)
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

        if (data.message && query !="" ) {
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
                            <button type="submit" class="btn" style="background-color: #130561;color: white;">Editar</button>
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

            const createDiv = document.createElement('div');
            const boxPagination = document.createElement('div');
            createDiv.className = 'row text-center';
            boxPagination.className = 'col me-5';
            if (has_previous) {
                const prevLink = document.createElement("a");
                // Inclui o parâmetro 'query' na URL para a navegação anterior
                prevLink.href = `/prsn/?page=${previous_page}&query=${encodeURIComponent(query)}`;
                prevLink.className="pagination-link me-5";

                const span = document.createElement('span');
                span.setAttribute('aria-hidden','true');
                span.style.fontSize = '32px';
                span.innerHTML = '&laquo;'

                prevLink.appendChild(span);
                prevLink.appendChild(span);
                boxPagination.appendChild(prevLink);
                createDiv.appendChild(boxPagination)
                paginationContainer.appendChild(createDiv);
            }
            else{
                const prevLink = document.createElement("a");
                prevLink.className="pagination-link me-5";

                const span = document.createElement('span');
                span.setAttribute('aria-hidden','true');
                span.setAttribute('aria-disabled','true');
                span.style.fontSize = '32px';
                span.style.color = 'gray';
                span.style.pointerEvents = 'none';
                span.innerHTML = '&laquo;'

                prevLink.appendChild(span);
                boxPagination.appendChild(prevLink);
                createDiv.appendChild(boxPagination)
                paginationContainer.appendChild(createDiv);
               
                
            }
            
            if (has_next) {
                const nextLink = document.createElement("a");
                // Inclui o parâmetro 'query' na URL para a navegação próxima
                nextLink.href = `/prsn/?page=${next_page}&query=${encodeURIComponent(query)}`;
                nextLink.className = "pagination-link me-5";

                const span = document.createElement('span');
                span.setAttribute('aria-hidden','true');
                span.style.fontSize = '32px';
                span.innerHTML = `&raquo;`

                nextLink.appendChild(span);
                boxPagination.appendChild(nextLink);
                createDiv.appendChild(boxPagination)
                paginationContainer.appendChild(createDiv);
            }
            else{
                const nextLink = document.createElement("a");
                // nextLink.href = `/venda/?page=${next_page}&query=${encodeURIComponent(query)}`;
                // nextLink.textContent = "Próximo";
                nextLink.className = "pagination-link me-5";

                const span = document.createElement('span');
                span.setAttribute('aria-hidden','true');
                span.setAttribute('aria-disabled','true');
                span.style.fontSize = '32px';
                span.style.color = 'gray';
                span.style.pointerEvents = 'none';
                span.innerHTML = `&raquo;`

                nextLink.appendChild(span);
                boxPagination.appendChild(nextLink);
                createDiv.appendChild(boxPagination)
                paginationContainer.appendChild(createDiv);
            }
        }
    })
    .catch(error => console.error("Erro ao buscar clientes:", error));
     const links = document.querySelectorAll(".cabecalho");
            links.forEach(link=>{
                const url = new URL(link.href);
                url.searchParams.set("query",query);
                link.href = url.toString();
            })
});