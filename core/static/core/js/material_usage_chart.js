document.addEventListener("DOMContentLoaded", function () {

    const canvas = document.getElementById("materialChart");
    if (!canvas) {
        console.error("❌ Không có canvas");
        return;
    }

    if (!window.chartLabels || !window.chartPercents) {
        console.error("❌ Không có dữ liệu");
        return;
    }

    const ctx = canvas.getContext("2d");

    console.log("🎯 DRAWING CHART");

    new Chart(ctx, {
        type: "bar",
        data: {
            labels: window.chartLabels,
            datasets: [{
                label: "% sử dụng so với định mức",
                data: window.chartPercents,
                backgroundColor: window.chartColors || "rgba(54,162,235,0.7)"
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            onClick: function (evt, elements) {
                if (!elements.length) return;

                const index = elements[0].index;
                const materialId = window.chartMaterialIds[index];

                const url =
                    `/projects/${window.projectId}/materials/${materialId}/usage/`;

                window.location.href = url;
            }
            }
    });
});
