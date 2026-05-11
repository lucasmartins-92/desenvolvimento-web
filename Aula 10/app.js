document.addEventListener('DOMContentLoaded', () => {
    const selecoesContainer = document.getElementById('selecoes');
    if (!selecoesContainer || typeof selecoesData === 'undefined') return;

    // Clear anything that might be there
    selecoesContainer.innerHTML = '';

    selecoesData.forEach(selecao => {
        // Create the block
        const block = document.createElement('div');
        block.className = 'selecao-block';
        block.id = selecao.id;

        // Create the header
        const header = document.createElement('div');
        header.className = 'selecao-header';
        header.innerHTML = `
            <div class="selecao-brasao">
                <img src="${selecao.bandeira}" alt="${selecao.nome}">
            </div>
            <div>
                <h2 class="selecao-name">${selecao.nome}</h2>
                <div class="selecao-group">${selecao.grupo}</div>
            </div>
        `;
        block.appendChild(header);

        // Create the table
        const table = document.createElement('table');
        table.className = 'squad-table';
        
        const thead = document.createElement('thead');
        thead.innerHTML = `
            <tr>
                <th>Nº</th>
                <th>Pos</th>
                <th>Nome</th>
            </tr>
        `;
        table.appendChild(thead);

        const tbody = document.createElement('tbody');
        selecao.jogadores.forEach(jogador => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td class="jersey-number">${jogador.numero}</td>
                <td><span class="pos-badge">${jogador.posicao}</span></td>
                <td>${jogador.nome}</td>
            `;
            tbody.appendChild(tr);
        });
        table.appendChild(tbody);
        block.appendChild(table);

        // Add toggle functionality (assuming it was there or would be nice to have, since there is a '.show' class in CSS for it)
        header.addEventListener('click', () => {
            table.classList.toggle('show');
        });

        selecoesContainer.appendChild(block);
    });
});
