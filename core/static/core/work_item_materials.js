document.addEventListener('DOMContentLoaded', function () {

    const materialSelect = document.getElementById('material-select');
    const coefficientInput = document.getElementById('coefficient-input');
    const normInput = document.getElementById('norm-input');
    const quantityPreview = document.getElementById('quantity-preview');

    if (!materialSelect || !coefficientInput || !normInput || !quantityPreview) {
        return;
    }

    function calculateQuantity() {
        const norm = parseFloat(normInput.value) || 0;
        const coefficient = parseFloat(coefficientInput.value) || 1;

        const quantity = WORK_ITEM_QUANTITY * norm * coefficient;
        quantityPreview.value = quantity.toFixed(4);
    }

    // Khi đổi vật liệu → load hệ số
    materialSelect.addEventListener('change', function () {
        const materialId = this.value;
        if (materialId) {
            fetch(`/materials/${materialId}/coefficient/`)
                .then(res => res.json())
                .then(data => {
                    coefficientInput.value = data.coefficient;
                    calculateQuantity();
                });
        }
    });

    normInput.addEventListener('input', calculateQuantity);
    coefficientInput.addEventListener('input', calculateQuantity);

});



