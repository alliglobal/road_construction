from django import forms

from .models import WarehouseTransaction
from .models import Project

from .models import DailyLog

class ExcelUploadForm(forms.Form):
    file = forms.FileField()


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'start_date']
        labels = {
            'name': 'Tên dự án',
            'start_date': 'Ngày khởi công'
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'VD: Dự án nâng cấp QL1A đoạn Km10–Km20'
            }),
            'start_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            })
        }
        

class WarehouseTransactionForm(forms.ModelForm):
    class Meta:
        model = WarehouseTransaction
        fields = [
            'material',
            'transaction_type',
            'quantity',
            'date',
            'work_item'
        ]
        labels = {
            'material': 'Vật tư',
            'transaction_type': 'Loại giao dịch',
            'quantity': 'Số lượng',
            'date': 'Ngày',
            'work_item': 'Công việc sử dụng (nếu xuất)'
        }
        widgets = {
            'material': forms.Select(attrs={'class': 'form-select'}),
            'transaction_type': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'work_item': forms.Select(attrs={'class': 'form-select'})
        }
class MaterialNormExcelForm(forms.Form):
    file = forms.FileField(label='File Excel định mức')
    

class MaterialExcelImportForm(forms.Form):
    file = forms.FileField(label='File Excel vật tư')

# from django import forms

class MaterialNormExcelForm(forms.Form):
    file = forms.FileField(label='File Excel định mức vật tư')



# class DailyLogForm(forms.ModelForm):
#     class Meta:
#         model = DailyLog
#         fields = ['log_date']
#         widgets = {
#             'log_date': forms.DateInput(attrs={'type': 'date'}),
#         }