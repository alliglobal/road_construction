from django.db import models
from core.models import WarehouseTransaction, DailyLogMaterialUsage

def process_daily_log(daily_log):
    """
    - Duyệt từng công việc trong nhật ký
    - Tính vật tư tiêu hao theo dự trù
    - Xuất kho
    - Trả cảnh báo vượt định mức
    """

    warnings = []
    project = daily_log.project

    for item in daily_log.items.select_related('work_item'):
        work_item = item.work_item

        if not work_item.quantity or work_item.quantity <= 0:
            continue

        ratio = item.quantity_done / work_item.quantity

        for wm in work_item.materials.select_related('material'):
            used_quantity = wm.quantity * ratio

            # 🔹 LƯU VẬT TƯ TIÊU HAO
            DailyLogMaterialUsage.objects.create(
                daily_log_item=item,
                material=wm.material,
                quantity_used=used_quantity
            )

            # 🔹 XUẤT KHO
            WarehouseTransaction.objects.create(
                material=wm.material,
                quantity=used_quantity,
                transaction_type='OUT',
                date=daily_log.log_date,
                work_item=work_item
            )

            # 🔹 TÍNH CẢNH BÁO
            total_used = (
                WarehouseTransaction.objects
                .filter(
                    material=wm.material,
                    transaction_type='OUT'
                )
                .aggregate(total=models.Sum('quantity'))['total'] or 0
            )

            if wm.quantity > 0:
                percent = round(total_used / wm.quantity * 100, 2)

                if percent >= 80:
                    warnings.append({
                        'material': wm.material.name,
                        'percent': percent
                    })

    return warnings
