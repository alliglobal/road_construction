# SERVICE TÍNH VẬT TƯ (TRÁI TIM HỆ THỐNG)
# core/services/daily_log_service.py

def calculate_material_usage(work_item, quantity_done):
    """
    quantity_used = quantity_done × norm_quantity × factor
    """
    results = []

    for norm in work_item.materials.all():
        used = quantity_done * norm.norm_quantity * norm.factor
        results.append({
            'material': norm.material,
            'quantity': used
        })

    return results
