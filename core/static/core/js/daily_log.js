let rowIndex = 0;

function addRow() {
    const tbody = document.querySelector("#log-table tbody");

    const tr = document.createElement("tr");
    tr.innerHTML = `
        <td>
            <select name="items[${rowIndex}][work_item]"
                    class="form-control work-item"
                    onchange="loadMaterials(this)">
                <option value="">-- Chọn công việc --</option>
                ${WORK_ITEMS_HTML}
            </select>
        </td>

        <td>
            <input type="number" step="0.01"
                   name="items[${rowIndex}][quantity_done]"
                   class="form-control quantity"
                   oninput="recalculate(this)">
        </td>

        <td class="materials"></td>

        <td>
            <button type="button"
                    class="btn btn-sm btn-danger"
                    onclick="this.closest('tr').remove()">
                ✖
            </button>
        </td>
    `;
    tbody.appendChild(tr);
    rowIndex++;
}

// Load vật tư theo công việc

function loadMaterials(select) {
    const tr = select.closest("tr");
    const materialsCell = tr.querySelector(".materials");
    const workItemId = select.value;

    if (!workItemId) return;

    fetch(`/api/work-items/${workItemId}/materials/`)
        .then(res => res.json())
        .then(data => {
            materialsCell.innerHTML = data.map(m =>
                `<div>
                    ${m.material}:
                    <span class="used" data-norm="${m.norm}">
                        0
                    </span> ${m.unit}
                </div>`
            ).join("");
        });
}

// Tính vật tư khi nhập khối lượng

function recalculate(input) {
    const tr = input.closest("tr");
    const quantity = parseFloat(input.value) || 0;

    tr.querySelectorAll(".used").forEach(span => {
        const norm = parseFloat(span.dataset.norm);
        span.innerText = (quantity * norm).toFixed(2);
    });
}

