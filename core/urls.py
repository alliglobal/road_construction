from django.urls import path
from . import views

# urlpatterns = [
#     path('', views.dashboard, name='dashboard'),
#     path('import/<int:project_id>/', views.import_excel, name='import_excel'),
#     path('works/<int:project_id>/', views.work_items, name='work_items'),
#     # path('warehouse/', views.warehouse, name='warehouse'),

#     # KHO VẬT TƯ
#     path('warehouse/', views.warehouse, name='warehouse'),
#     path('warehouse/import-materials/', views.import_materials_excel, name='import_materials_excel'),
#     path('warehouse/transaction/new/', views.create_warehouse_transaction, name='create_warehouse_transaction'),

#     # ĐỊNH MỨC VẬT TƯ
#     path('material-norms/', views.material_norms, name='material_norms'),
#     path('material-norms/import/', views.import_material_norms, name='import_material_norms'),


#     path('projects/create/', views.create_project, name='create_project'),
#     # path('warehouse/create/', views.create_warehouse_transaction,
#         #  name='create_warehouse_transaction'),

#     # path('material-norms/import/<int:project_id>/',
#     # views.import_material_norms,
#     # name='import_material_norms'),

#     # path(
#     # 'warehouse/import-materials/',
#     # views.import_materials_excel,
#     # name='import_materials_excel'
#     # ),
#     path('projects/', views.project_list, name='project_list'),

#     path(
#     'projects/<int:project_id>/warehouse/',
#     views.project_warehouse,
#     name='project_warehouse'
#     ),

#     path(
#     'projects/<int:project_id>/material-norms/',
#     views.project_material_norms,
#     name='project_material_norms'
#     ),

#     path(
#     'projects/<int:project_id>/',
#     views.project_dashboard,
#     name='project_dashboard'
#     ),


    

# ]

urlpatterns = [

    # Dashboard tổng
    path('', views.dashboard, name='dashboard'),

    # Dự án
    path('projects/', views.project_list, name='project_list'),
    path('projects/create/', views.create_project, name='create_project'),

    # Dashboard dự án
    path(
        'projects/<int:project_id>/',
        views.project_dashboard,
        name='project_dashboard'
    ),

    # path('daily-log/<int:pk>/edit/', views.daily_log_edit, name='daily_log_edit'),
    # path('daily-log/<int:pk>/delete/', views.daily_log_delete, name='daily_log_delete'),

    path(
        'projects/<int:project_id>/warehouse/',
        views.warehouse,
        name='warehouse'
    ),

    path(
        'projects/<int:project_id>/material-norms/',
        views.material_norms,
        name='material_norms'
    ),

    path(
    'projects/<int:project_id>/material-norms/import-excel/',
    views.import_material_norms_excel,
    name='import_material_norms_excel'
    ),

    #     # KHO VẬT TƯ
    path('warehouse/', views.warehouse, name='warehouse'),
    path('warehouse/import-materials/', views.import_materials_excel, name='import_materials_excel'),
    path('warehouse/transaction/new/', views.create_warehouse_transaction, name='create_warehouse_transaction'),

     #     # IMPORT KHỐI LƯỢNG CÔNG VIỆC
    path(
        'projects/<int:project_id>/work-items/',
        views.work_items,
        name='work_items'
    ),

    path(
        'projects/<int:project_id>/work-items/import/',
        views.import_work_items_excel,
        name='import_work_items_excel'
    ),

    path(
        'work-item/<int:work_item_id>/materials/',
        views.work_item_materials,
        name='work_item_materials'
    ),
# THÊM XOÁ SỬA DỰ TRÙ
    path(
        'work-item-material/<int:pk>/edit/',
        views.edit_work_item_material,
        name='edit_work_item_material'
    ),

    path(
        'work-item-material/<int:pk>/delete/',
        views.delete_work_item_material,
        name='delete_work_item_material'
    ),

    path(
        'materials/<int:material_id>/coefficient/',
        views.get_material_coefficient,
        name='get_material_coefficient'
    ),

    path(
        'projects/<int:project_id>/materials/<int:material_id>/usage/',
        views.material_usage_detail,
        name='material_usage_detail'
    ),

    path(
    'work-items/<int:work_item_id>/materials/',
    views.work_item_materials,
    name='work_item_materials'
    ),
    
    path(
    'api/work-items/<int:work_item_id>/materials/',
    views.work_item_materials_api
    ),

#     path(
#     'projects/<int:project_id>/daily-log/',
#     views.daily_log_calendar,
#     name='daily_log_calendar'
# ),
   
# ),
# Để click lịch tháng 12 và tháng 1
    path(
    'projects/<int:project_id>/daily-log/<int:year>/<int:month>/',
    views.daily_log_calendar,
    name='daily_log_calendar'
),


    path(
        'projects/<int:project_id>/daily-log/<int:year>/<int:month>/<int:day>/',
        views.daily_log_form,
        name='daily_log_form'
    ),


    path(
    'api/work-item/<int:work_item_id>/materials/',
    views.work_item_materials_api,
    name='work_item_materials_api'
),

path(
    'projects/<int:project_id>/daily-log/',
    views.daily_log_calendar,
    name='daily_log_calendar'
),

#Sửa / Xóa từng dòng nhật ký
path(
    'daily-log/item/<int:pk>/edit/',
    views.daily_log_item_edit,
    name='daily_log_item_edit'
),

path(
    'daily-log/item/<int:pk>/delete/',
    views.daily_log_item_delete,
    name='daily_log_item_delete'
),



]
