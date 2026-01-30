import pandas as pd
from django.utils import timezone
from django.shortcuts import render, redirect
from .models import *
from .forms import ExcelUploadForm
from .forms import ProjectForm
from .forms import WarehouseTransactionForm

from django.contrib import messages
from .forms import MaterialNormExcelForm

from .forms import MaterialExcelImportForm

from django.shortcuts import get_object_or_404

from django.db.models import Sum
from .models import (
    Project,
    WorkItem,
    WorkItemMaterial,
    DailyLog,
    DailyLogMaterialUsage,
)



# def dashboard(request):
#     projects = Project.objects.all()
#     return render(request, 'core/dashboard.html', {'projects': projects})

from .models import Project

def dashboard(request):
    projects = Project.objects.all().order_by('-id')
    return render(request, 'core/dashboard.html', {
        'projects': projects
    })



def import_excel(request, project_id):
    project = Project.objects.get(id=project_id)

    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            df = pd.read_excel(request.FILES['file'])
            #them
            print(df.columns.tolist())
            df.columns = df.columns.str.strip()


            for _, row in df.iterrows():
                WorkItem.objects.create(
                    project=project,
                    code=row[0],
                    name=row[1],
                    unit=row[2],
                    quantity=row[3]
                )
            return redirect('work_items', project_id=project.id)
    else:
        form = ExcelUploadForm()

    return render(request, 'core/import_excel.html', {'form': form})


def work_items(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    work_items = (
        WorkItem.objects
        .filter(project=project)
        .select_related('parent')
        .order_by('index_code')
    )

    print("WORK ITEMS COUNT:", work_items.count())

    return render(request, 'core/work_items.html', {
        'project': project,
        'work_items': work_items
    })




# core/views.py

from datetime import date
from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, WorkItem, DailyLog, DailyLogItem


# core/views.py

from datetime import date
from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, WorkItem, DailyLog, DailyLogItem


from datetime import date
from django.shortcuts import render, get_object_or_404, redirect

from datetime import date
from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, WorkItem, DailyLog, DailyLogItem




from datetime import date
from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, DailyLog, WorkItem


# def warehouse(request):
#     transactions = WarehouseTransaction.objects.all()
#     return render(request, 'core/warehouse.html', {'transactions': transactions})

# def warehouse(request):
#     materials = Material.objects.all().order_by('name')
#     return render(request, 'core/warehouse.html', {
#         'materials': materials
#     })

def warehouse(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    materials = Material.objects.filter(project=project)

    return render(request, 'core/warehouse.html', {
        'project': project,
        'materials': materials
    })



def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProjectForm()

    return render(request, 'core/create_project.html', {
        'form': form
    })

def create_warehouse_transaction(request):
    if request.method == 'POST':
        form = WarehouseTransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('warehouse')
    else:
        form = WarehouseTransactionForm()

    return render(request, 'core/create_warehouse_transaction.html', {
        'form': form
    })

from .models import MaterialNorm

def material_norms(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    norms = (
        MaterialNorm.objects
        .filter(project=project)
        .select_related('material')
    )

    return render(request, 'core/material_norms.html', {
        'project': project,
        'norms': norms
    })





def import_material_norms(request, project_id):
    project = Project.objects.get(id=project_id)

    if request.method == 'POST':
        form = MaterialNormExcelForm(request.POST, request.FILES)
        if form.is_valid():
            df = pd.read_excel(request.FILES['file'])
            #them
            df.columns = df.columns.str.strip()

            for _, row in df.iterrows():
                work_code = str(row[0]).strip()
                material_name = str(row[2]).strip()
                norm_value = float(row[3])

                try:
                    work_item = WorkItem.objects.get(
                        project=project,
                        code=work_code
                    )
                except WorkItem.DoesNotExist:
                    continue

                material, _ = Material.objects.get_or_create(
                    name=material_name,
                    defaults={'unit': ''}
                )

                MaterialNorm.objects.update_or_create(
                    work_item=work_item,
                    material=material,
                    defaults={'norm_quantity': norm_value}
                )

            messages.success(
                request, 'Import định mức vật tư thành công!'
            )
            return redirect('work_items', project_id=project.id)
    else:
        form = MaterialNormExcelForm()

    return render(request, 'core/import_material_norms.html', {
        'form': form,
        'project': project
    })


def import_materials_excel(request):
    if request.method == 'POST':
        form = MaterialExcelImportForm(request.POST, request.FILES)
        if form.is_valid():
            df = pd.read_excel(request.FILES['file'])

            for _, row in df.iterrows():
                name = str(row[0]).strip()
                unit = str(row[1]).strip()
                quantity = float(row[2])
                warning_1 = float(row[3])
                warning_2 = float(row[4])

                if not name:
                    continue

                material, created = Material.objects.update_or_create(
                    name=name,
                    defaults={
                        'unit': unit,
                        'warning_level_1': warning_1,
                        'warning_level_2': warning_2
                    }
                )

                # Nếu có khối lượng ban đầu → tạo giao dịch nhập kho
                if quantity > 0:
                    WarehouseTransaction.objects.create(
                        material=material,
                        quantity=quantity,
                        transaction_type='IN',
                        date=timezone.now().date()
                    )

            return redirect('warehouse')
    else:
        form = MaterialExcelImportForm()

    return render(request, 'core/import_materials_excel.html', {
        'form': form
    })

from .models import Project

def project_list(request):
    projects = Project.objects.all().order_by('-id')
    return render(request, 'core/project_list.html', {
        'projects': projects
    })

from .models import DailyLog

# def daily_logs(request, project_id):
#     project = get_object_or_404(Project, id=project_id)
#     logs = DailyLog.objects.filter(project=project).order_by('-date')

#     return render(request, 'core/daily_log.html', {
#         'project': project,
#         'logs': logs
#     })


# def daily_logs(request, project_id):
#     project = get_object_or_404(Project, id=project_id)
#     work_items = WorkItem.objects.filter(
#     project=project
# ).order_by('index_code')

#     # work_items = WorkItem.objects.filter(project=project)
#     daily_logs = DailyLog.objects.filter(project=project).order_by('-date')

#     warnings = []  # ⚠️ BẮT BUỘC khởi tạo

#     if request.method == 'POST':
#         date = request.POST.get('date')
#         work_item_id = request.POST.get('work_item')
#         quantity_done = float(request.POST.get('quantity_done'))
#         note = request.POST.get('note', '')

#         work_item = get_object_or_404(WorkItem, id=work_item_id)

#         # 👉 TẠO NHẬT KÝ + TÍNH TIÊU HAO
#         create_daily_log_and_calculate_materials(
#             project=project,
#             work_item=work_item,
#             date=date,
#             quantity_done=quantity_done,
#             note=note
#         )

#         # 👉 DÒNG BẠN HỎI NẰM CHÍNH XÁC Ở ĐÂY
#         warnings = check_material_warning_by_work_item(work_item)

#         return redirect('daily_logs', project_id=project.id)

#     return render(request, 'core/daily_logs.html', {
#         'project': project,
#         'work_items': work_items,
#         'daily_logs': daily_logs,
#         'warnings': warnings,
#     })




def project_warehouse(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    materials = Material.objects.filter(project=project)

    return render(request, 'core/project_warehouse.html', {
        'project': project,
        'materials': materials
    })

def project_material_norms(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    norms = MaterialNorm.objects.filter(project=project)

    return render(request, 'core/project_material_norms.html', {
        'project': project,
        'norms': norms
    })


def project_dashboard(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    # labels, percents, colors = get_material_usage_chart_data(project)
    labels, percents, colors, material_ids = get_material_usage_chart_data(project)


    print("LABELS:", labels)
    print("PERCENTS:", percents)
    print("material_ids",material_ids)

    return render(request, 'core/project_dashboard.html', {
        'project': project,
        'chart_labels': labels,
        'chart_percents': percents,
        'chart_colors': colors,
        'chart_material_ids': material_ids,
    })



import pandas as pd
from django.shortcuts import render, redirect, get_object_or_404
from .models import Project, Material, MaterialNorm
from .forms import MaterialNormExcelForm


def import_material_norms_excel(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        form = MaterialNormExcelForm(request.POST, request.FILES)
        if form.is_valid():
            df = pd.read_excel(request.FILES['file'])
            #them
            
            print(df.columns.tolist())
            df.columns = df.columns.str.strip()

            for _, row in df.iterrows():
                name = str(row['Tên vật tư']).strip()
                unit = str(row['Đơn vị']).strip()

                if not name:
                    continue

                material, _ = Material.objects.get_or_create(
                    project=project,
                    name=name,
                    defaults={
                        'unit': unit,
                        'warning_level_1': row.get('Mức cảnh báo 1', 0),
                        'warning_level_2': row.get('Mức cảnh báo 2', 0),
                    }
                )

                MaterialNorm.objects.update_or_create(
                    project=project,
                    material=material,
                    defaults={
                        'norm_quantity': row['Khối lượng định mức']
                    }
                )

            return redirect('material_norms', project_id=project.id)
    else:
        form = MaterialNormExcelForm()

    return render(request, 'core/import_material_norms_excel.html', {
        'project': project,
        'form': form
    })

import pandas as pd
from .models import WorkItem
from .utils.work_item_import import get_parent_index
from core.utils.excel_validators import validate_work_items_excel
from django.contrib import messages


# def import_work_items_excel(request, project_id):
#     project = get_object_or_404(Project, id=project_id)

#     if request.method == 'POST' and request.FILES.get('excel_file'):
#         df = pd.read_excel(request.FILES['excel_file'])
#         dtype={'Chỉ mục': str}
#         errors = validate_work_items_excel(df)

#         if errors:
#             for err in errors:
#                 messages.error(request, err)
#             return redirect('work_items', project_id=project.id)


        

#         print("COLUMNS:", df.columns.tolist())
#         print(df.head())

#         item_map = {}

#         for _, row in df.iterrows():
#             raw_index = row['Chỉ mục']

#             if pd.isna(raw_index):
#                 continue

#             index_code = str(raw_index).rstrip('.0').strip()
#             name = str(row['Tên công việc']).strip()

#             if not name:
#                 continue

#             unit = row.get('Đơn vị', '')
#             quantity = row.get('Khối lượng')

#             parent_index = get_parent_index(index_code)
#             parent = item_map.get(parent_index)

#             item = WorkItem.objects.create(
#                 project=project,
#                 index_code=index_code,
#                 name=name,
#                 unit='' if pd.isna(unit) else str(unit),
#                 quantity=None if pd.isna(quantity) else float(quantity),
#                 parent=parent
#             )

#             item_map[index_code] = item
#             print("✅ CREATED:", index_code, name)

#         print("🔥 IMPORT DONE")
#         return redirect('work_items', project_id=project.id)

#     return redirect('work_items', project_id=project.id)

def import_work_items_excel(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method != 'POST' or 'excel_file' not in request.FILES:
        messages.error(request, "❌ Vui lòng chọn file Excel")
        return redirect('work_items', project_id=project.id)

    try:
        # ✅ BẮT BUỘC đọc chỉ mục dạng TEXT
        df = pd.read_excel(
            request.FILES['excel_file'],
            dtype={'Chỉ mục': str}
        )
    except Exception as e:
        messages.error(request, f"❌ Không đọc được file Excel: {e}")
        return redirect('work_items', project_id=project.id)

    # ===== VALIDATE CỘT =====
    required_cols = ['Chỉ mục', 'Tên công việc']
    for col in required_cols:
        if col not in df.columns:
            messages.error(request, f"❌ Thiếu cột bắt buộc: {col}")
            return redirect('work_items', project_id=project.id)

    # ===== VALIDATE TRÙNG CHỈ MỤC TRONG EXCEL =====
    seen = set()
    for i, row in df.iterrows():
        index_code = str(row['Chỉ mục']).strip()
        if not index_code:
            continue

        if index_code in seen:
            messages.error(
                request,
                f"❌ Excel bị trùng chỉ mục '{index_code}' tại dòng {i + 2}"
            )
            return redirect('work_items', project_id=project.id)

        seen.add(index_code)

    # ===== XÓA TOÀN BỘ BOQ CŨ (CHỦ ĐÍCH) =====
    WorkItem.objects.filter(project=project).delete()

    item_map = {}

    # ===== IMPORT =====
    for _, row in df.iterrows():
        index_code = str(row['Chỉ mục']).strip()
        name = str(row['Tên công việc']).strip()

        if not index_code or not name:
            continue

        unit = row.get('Đơn vị', '')
        quantity = row.get('Khối lượng')

        parent_index = get_parent_index(index_code)
        parent = item_map.get(parent_index)

        item = WorkItem.objects.create(
            project=project,
            index_code=index_code,
            name=name,
            unit='' if pd.isna(unit) else str(unit),
            quantity=None if pd.isna(quantity) else float(quantity),
            parent=parent
        )

        item_map[index_code] = item

    messages.success(request, "✅ Import khối lượng công việc thành công")
    return redirect('work_items', project_id=project.id)



def work_item_materials(request, work_item_id):
    work_item = get_object_or_404(WorkItem, id=work_item_id)
    materials = work_item.materials.select_related('material')
    all_materials = Material.objects.all()

    if request.method == 'POST':
        material_id = request.POST.get('material')
        quantity = float(request.POST.get('quantity', 0))
        factor = float(request.POST.get('factor', 1))

        material = get_object_or_404(Material, id=material_id)

        work_qty = work_item.quantity or 0
        norm = 0
        if work_qty > 0:
            norm = quantity / work_qty / factor

        WorkItemMaterial.objects.create(
            work_item=work_item,
            material=material,
            # unit=material.unit,
            quantity=quantity,
            factor=factor,
            norm=norm
        )

        return redirect('work_item_materials', work_item_id=work_item.id)

    return render(request, 'core/work_item_materials.html', {
        'work_item': work_item,
        'materials': materials,
        'all_materials': all_materials
    })
#   SỬA DỰ TRÙ
def edit_work_item_material(request, pk):
    item = get_object_or_404(WorkItemMaterial, pk=pk)
    work_item = item.work_item

    if request.method == 'POST':
        item.norm = float(request.POST.get('norm'))
        item.factor = float(request.POST.get('factor', 1))

        quantity_input = request.POST.get('quantity')

        if quantity_input:
            # ✅ Người dùng nhập thủ công
            item.quantity = float(quantity_input)
        else:
            # 🔄 Tự tính lại
            item.quantity = work_item.quantity * item.norm * item.factor

        item.save()

        return redirect('work_item_materials', work_item_id=work_item.id)

    return render(request, 'core/work_item_material_edit_form.html', {
        'item': item,
        'work_item': work_item
    })


#   XOÁ DỰ TRÙ
def delete_work_item_material(request, pk):
    item = get_object_or_404(WorkItemMaterial, pk=pk)
    work_item_id = item.work_item.id

    if request.method == 'POST':
        item.delete()
        return redirect('work_item_materials', work_item_id=work_item_id)

    return render(request, 'core/confirm_delete.html', {
        'object': item
    })




#lấy hệ số
from django.http import JsonResponse

def get_material_coefficient(request, material_id):
    material = get_object_or_404(Material, id=material_id)
    return JsonResponse({
        'coefficient': material.default_coefficient
    })


# def create_daily_log_and_calculate_materials(
#     project, work_item, date, quantity_done, note
# ):
#     # 1️⃣ Tạo nhật ký
#     daily_log = DailyLog.objects.create(
#         # project=project,
#         work_item=work_item,
#         # date=date,
#         quantity_done=quantity_done,
#         # note=note
#     )

#     # 2️⃣ Cập nhật khối lượng công việc
#     work_item.completed_quantity += quantity_done
#     work_item.save()

#     # 3️⃣ TÍNH VẬT TƯ TIÊU HAO
#     planned_quantity = work_item.quantity

#     materials = WorkItemMaterial.objects.filter(work_item=work_item)

#     for wm in materials:
#         used_today = (
#             quantity_done / planned_quantity
#         ) * wm.quantity

#         DailyLogMaterialUsage.objects.create(
#             daily_log=daily_log,
#             material=wm.material,
#             quantity_used=used_today
#         )

#     return daily_log

# LOGIC CẢNH BÁO VƯỢT 80%
def check_material_warning(work_item):
    warnings = []

    for wm in WorkItemMaterial.objects.filter(work_item=work_item):
        used_total = DailyLogMaterialUsage.objects.filter(
            daily_log__work_item=work_item,
            material=wm.material
        ).aggregate(total=models.Sum('quantity_used'))['total'] or 0

        percent = used_total / wm.quantity * 100

        if percent >= 80:
            warnings.append({
                'material': wm.material.name,
                'used': round(used_total, 2),
                'planned': wm.quantity,
                'percent': round(percent, 1)
            })

    return warnings

#HÀM CẢNH BÁO ĐÚNG – CHUẨN NGHIỆP VỤ
def check_material_warning_by_work_item(work_item):
    warnings = []

    norms = WorkItemMaterial.objects.filter(work_item=work_item)

    for norm in norms:
        used_total = DailyLogMaterialUsage.objects.filter(
            daily_log__work_item=work_item,
            material=norm.material
        ).aggregate(total=Sum('quantity_used'))['total'] or 0

        percent = (used_total / norm.quantity) * 100 if norm.quantity > 0 else 0

        if percent >= 80:
            warnings.append({
                    'work_item': work_item.name,
                    'material': norm.material.name,
                    'used': round(used_total, 2),
                    'planned': round(norm.quantity, 2),
                    'percent': round(percent, 1),
                })
                

    return warnings


# HÀM TÍNH DỮ LIỆU BIỂU ĐỒ (BACKEND)
from collections import defaultdict
from .models import DailyLog, WorkItemMaterial, MaterialNorm


from collections import defaultdict
from django.db.models import Sum
from .models import DailyLog, WorkItemMaterial, MaterialNorm


def get_material_usage_chart_data(project):
    material_used = defaultdict(float)

    logs = DailyLog.objects.filter(project=project)

    for log in logs:
        for item in log.items.select_related('work_item'):
            work_item = item.work_item

            for m in work_item.materials.select_related('material'):
                used_qty = item.quantity_done * m.norm * m.factor
                material_used[m.material.name] += used_qty

    labels, percents, colors, material_ids = [], [], [], []

    norms = MaterialNorm.objects.filter(project=project)

    for norm in norms:
        used = material_used.get(norm.material.name, 0)

        if norm.norm_quantity <= 0:
            continue

        percent = round((used / norm.norm_quantity) * 100, 2)

        labels.append(norm.material.name)
        percents.append(percent)
        material_ids.append(norm.material.id)

        if percent < 80:
            colors.append("#28a745")
        elif percent <= 100:
            colors.append("#ffc107")
        else:
            colors.append("#dc3545")

    return labels, percents, colors, material_ids



from .models import Project, Material, DailyLog, WorkItemMaterial, MaterialNorm


# VIEW CHI TIẾT VẬT TƯ
from django.shortcuts import render, get_object_or_404
from core.models import (
    Project,
    Material,
    DailyLogMaterialUsage
)

def material_usage_detail(request, project_id, material_id):
    project = get_object_or_404(Project, id=project_id)
    material = get_object_or_404(Material, id=material_id)

    usages = (
        DailyLogMaterialUsage.objects
        .filter(
            material=material,
            daily_log_item__daily_log__project=project
        )
        .select_related(
            'daily_log_item__daily_log',
            'daily_log_item__work_item'
        )
        .order_by('daily_log_item__daily_log__log_date')
    )

    return render(request, 'core/material_usage_detail.html', {
        'project': project,
        'material': material,
        'usages': usages
    })




# XOÁ NHẬT KÝ (CÓ XÁC NHẬN)
def daily_log_delete(request, pk):
    log = get_object_or_404(DailyLog, pk=pk)
    project_id = log.project.id

    if request.method == 'POST':
        log.delete()
        return redirect('daily_logs', project_id=project_id)

    return render(request, 'core/daily_log_confirm_delete.html', {
        'log': log
    })

from core.services.material_flow import process_daily_log

# def daily_logs(request, project_id):
#     project = get_object_or_404(Project, id=project_id)

#     if request.method == 'POST':
#         work_item_id = request.POST.get('work_item')
#         quantity_done = float(request.POST.get('quantity_done'))

#         log = DailyLog.objects.create(
#             # project=project,
#             work_item_id=work_item_id,
#             quantity_done=quantity_done
#         )

#         warnings = process_daily_log(log)

#         if warnings:
#             messages.warning(
#                 request,
#                 f"Cảnh báo vượt định mức: {warnings}"
#             )

#         return redirect('daily_log', project_id=project.id)

    


# API CUNG CẤP VẬT TƯ THEO CÔNG VIỆC
# def work_item_materials_api(request, work_item_id):
#     materials = WorkItemMaterial.objects.filter(
#         work_item_id=work_item_id
#     )

#     return JsonResponse([
#         {
#             'material': m.material.name,
#             'norm': m.norm * m.factor,
#             'unit': m.material.unit
#         }
#         for m in materials
#     ], safe=False)

# View hiển thị lịch theo tháng

# core/views.py
import calendar
from datetime import date
from .models import DailyLog


# from datetime import date

# from datetime import date
# import calendar

# import calendar
# from datetime import date
# from django.shortcuts import render, get_object_or_404
# from .models import Project, DailyLog


# def daily_log_calendar(request, project_id, year=None, month=None):
#     project = get_object_or_404(Project, id=project_id)

#     today = date.today()
#     year = year or today.year
#     month = month or today.month

#     # Calendar matrix
#     cal = calendar.monthcalendar(year, month)

#     # Days that have logs
#     log_days = DailyLog.objects.filter(
#         project=project,
#         log_date__year=year,
#         log_date__month=month
#     ).values_list('log_date__day', flat=True)

    

#     # ===== PREV / NEXT MONTH (QUAN TRỌNG) =====
#     prev_month = month - 1
#     prev_year = year
#     if prev_month == 0:
#         prev_month = 12
#         prev_year -= 1

#     next_month = month + 1
#     next_year = year
#     if next_month == 13:
#         next_month = 1
#         next_year += 1

#     return render(request, 'core/daily_log_calendar.html', {
#         'project': project,
#         'calendar': cal,
#         'year': year,
#         'month': month,
#         'log_days': log_days,
#         'prev_year': prev_year,
#         'prev_month': prev_month,
#         'next_year': next_year,
#         'next_month': next_month,
#     })

from datetime import timedelta

from datetime import date
import calendar
from django.shortcuts import render, get_object_or_404
from core.models import Project, DailyLog


def daily_log_calendar(request, project_id, year=None, month=None):
    project = get_object_or_404(Project, id=project_id)

    today = date.today()
    year = int(year) if year else today.year
    month = int(month) if month else today.month

    # ===== THÁNG HIỆN TẠI =====
    current_month = date(year, month, 1)

    # ===== THÁNG TRƯỚC / SAU (XỬ LÝ QUA NĂM) =====
    prev_month = (current_month.replace(day=1) - timedelta(days=1)).replace(day=1)
    next_month = (current_month.replace(day=28) + timedelta(days=4)).replace(day=1)

    # ===== NHẬT KÝ TRONG THÁNG =====
    logs = DailyLog.objects.filter(
        project=project,
        log_date__year=year,
        log_date__month=month
    ).prefetch_related('items__work_item')
    
    # 🔥 CỰC KỲ QUAN TRỌNG
    log_map = {log.log_date.day: log for log in logs}

    cal = calendar.Calendar(firstweekday=6)
    calendar_month = cal.monthdayscalendar(year, month)

    return render(request, 'core/daily_log_calendar.html', {
        'project': project,
        'year': year,
        'month': month,
        'calendar': calendar_month,
        'log_map': log_map,

        # 🔥 TRUYỀN THÁNG TRƯỚC / SAU
        'prev_year': prev_month.year,
        'prev_month': prev_month.month,
        'next_year': next_month.year,
        'next_month': next_month.month,
    })


from datetime import date
from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, DailyLog, WorkItem

# Để click lịch tháng 12 và tháng 1
from datetime import date
from django.shortcuts import render, get_object_or_404, redirect
from core.models import (
    Project, DailyLog, DailyLogItem, WorkItem
)


from datetime import date
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages

def daily_log_form(request, project_id, year, month, day):
    project = get_object_or_404(Project, id=project_id)
    log_date = date(year, month, day)

    # 1️⃣ Lấy / tạo nhật ký ngày
    daily_log, _ = DailyLog.objects.get_or_create(
        project=project,
        log_date=log_date
    )

    # 2️⃣ Danh sách công việc
    work_items = WorkItem.objects.filter(
        project=project
    ).order_by('index_code')

    # 3️⃣ XỬ LÝ POST
    if request.method == 'POST':
        work_item_id = request.POST.get('work_item_id')
        quantity = request.POST.get('quantity')

        if not work_item_id or not quantity:
            messages.error(request, 'Thiếu dữ liệu.')
            return redirect(request.path)

        work_item = get_object_or_404(
            WorkItem,
            id=work_item_id,
            project=project
        )

        DailyLogItem.objects.create(
            daily_log=daily_log,
            work_item=work_item,
            quantity_done=float(quantity)
        )

        messages.success(request, 'Đã lưu nhật ký.')
        return redirect(
            'daily_log_form',
            project_id=project.id,
            year=year,
            month=month,
            day=day
        )

    # 4️⃣ Nhật ký đã ghi (để hiển thị phía dưới)
    items = daily_log.items.select_related('work_item')

    return render(request, 'core/daily_log_form.html', {
        'project': project,
        'log_date': log_date,
        'work_items': work_items,
        'items': items,
    })






# API vật tư theo công việc
def work_item_materials_api(request, work_item_id):
    materials = WorkItemMaterial.objects.filter(
        work_item_id=work_item_id
    ).select_related('material')

    return JsonResponse([
        {
            'material_id': m.material.id,
            'material': m.material.name,
            'unit': m.material.unit,
            'norm': m.norm,
            'factor': m.factor,
        }
        for m in materials
    ], safe=False)

from django.shortcuts import get_object_or_404, redirect, render
from core.models import DailyLogItem

# SỬA DÒNG NHẬT KÝ
def daily_log_item_edit(request, pk):
    item = get_object_or_404(DailyLogItem, pk=pk)
    daily_log = item.daily_log

    if request.method == 'POST':
        qty = request.POST.get('quantity_done')
        note = request.POST.get('note', '').strip()

        if qty and float(qty) > 0:
            item.quantity_done = float(qty)
            item.note = note
            item.save()

        return redirect(
            'daily_log_form',
            project_id=daily_log.project.id,
            year=daily_log.log_date.year,
            month=daily_log.log_date.month,
            day=daily_log.log_date.day
        )

    return render(request, 'core/daily_log_item_edit.html', {
        'item': item
    })

# XOÁ DÒNG NHẬT KÝ
def daily_log_item_delete(request, pk):
    item = get_object_or_404(DailyLogItem, pk=pk)
    daily_log = item.daily_log

    item.delete()

    return redirect(
        'daily_log_form',
        project_id=daily_log.project.id,
        year=daily_log.log_date.year,
        month=daily_log.log_date.month,
        day=daily_log.log_date.day
    )
