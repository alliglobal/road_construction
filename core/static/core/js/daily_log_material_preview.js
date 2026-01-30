// static/core/js/daily_log_material_preview.js

document.querySelectorAll('.material-input').forEach(input => {
    input.addEventListener('input', function () {
        const workItemId = this.dataset.workitem;
        const qty = parseFloat(this.value || 0);
        const container = document.getElementById(`materials-${workItemId}`);
        container.innerHTML = '';

        if (!window.workItemMaterials[workItemId]) return;

        window.workItemMaterials[workItemId].forEach(m => {
            const used = qty * m.norm * m.factor;
            container.innerHTML += `
                ${m.name}: <strong>${used.toFixed(2)} ${m.unit}</strong><br>
            `;
        });
    });
});
