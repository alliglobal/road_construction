from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=255)
    start_date = models.DateField()

    def __str__(self):
        return self.name


class WorkItem(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    index_code = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    unit = models.CharField(max_length=50, blank=True)
    quantity = models.FloatField(null=True, blank=True)

    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.index_code} - {self.name}"

    @property
    def level(self):
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent
        return level


    # index_code = models.CharField(max_length=50)  # 1.2.1

    # code = models.CharField(
    #     max_length=50,
    #     blank=True,
    #     null=True
    # )



    # name = models.CharField(max_length=255)
    # unit = models.CharField(max_length=50)

    # quantity = models.FloatField()

    completed_quantity = models.FloatField(default=0)  # 👈 mới

    # parent = models.ForeignKey(
    #     'self',
    #     null=True,
    #     blank=True,
    #     on_delete=models.CASCADE,
    #     related_name='children'
    # )


    # def level(self):
    #     return self.code.count('.')

    def __str__(self):
        return f"{self.code} {self.name}"
    
    def progress_percent(self):
        if self.quantity > 0:
            return round(self.completed_quantity / self.quantity * 100, 2)
        return 0



# class DailyLog(models.Model):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     date = models.DateField()
#     description = models.TextField()

#     def __str__(self):
#         return f"{self.project} - {self.date}"

# class DailyLog(models.Model):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     work_item = models.ForeignKey(
#         WorkItem,
#         on_delete=models.CASCADE,
#         related_name='daily_logs'
#     )

#     date = models.DateField()
#     quantity_done = models.FloatField()
#     note = models.TextField(blank=True)

#     log_date = models.DateField()   # 👈 THÊM DÒNG NÀY

#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.project} - {self.date}"

class DailyLog(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    log_date = models.DateField()

    class Meta:
        unique_together = ('project', 'log_date')

    def __str__(self):
        return f"{self.project} - {self.log_date}"

#Chi tiết nhật ký (NHIỀU CÔNG VIỆC)

class DailyLogItem(models.Model):
    daily_log = models.ForeignKey(
        DailyLog,
        related_name='items',
        on_delete=models.CASCADE
    )
    work_item = models.ForeignKey(WorkItem, on_delete=models.CASCADE)
    quantity_done = models.FloatField()
    note = models.TextField(blank=True)


    def __str__(self):
        return f"{self.work_item} ({self.quantity_done})"





class DailyLogImage(models.Model):
    log = models.ForeignKey(DailyLog, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='daily_logs/')


class WorkProgress(models.Model):
    work_item = models.ForeignKey(WorkItem, on_delete=models.CASCADE)
    log = models.ForeignKey(DailyLog, on_delete=models.CASCADE)
    executed_quantity = models.FloatField()


class Material(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='materials'
    )

    name = models.CharField(max_length=255)
    unit = models.CharField(max_length=50)

    #Hệ số 
    default_coefficient = models.FloatField(
        default=1,
        help_text="Hệ số hao hụt mặc định"
    )

    warning_level_1 = models.FloatField(default=0)
    warning_level_2 = models.FloatField(default=0)

    def __str__(self):
        return f"{self.name} ({self.project.name})"




class WarehouseTransaction(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.FloatField()
    transaction_type = models.CharField(
        max_length=3,
        choices=[('IN', 'Nhập'), ('OUT', 'Xuất')]
    )
    date = models.DateField()
    work_item = models.ForeignKey(
        WorkItem, null=True, blank=True, on_delete=models.SET_NULL
    )


class MaterialNorm(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='material_norms',
        default='', null=True
    )

    material = models.ForeignKey(
        Material,
        on_delete=models.CASCADE
    )

    # nếu bạn có gắn với hạng mục công việc
    work_item = models.ForeignKey(
        WorkItem,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    norm_quantity = models.FloatField()

    def __str__(self):
        return f"{self.material.name} - {self.project.name}"


class WorkItemMaterial(models.Model):
    work_item = models.ForeignKey(
        WorkItem,
        on_delete=models.CASCADE,
        related_name='materials'
    )

    material = models.ForeignKey(Material, on_delete=models.CASCADE)

    norm = models.FloatField(help_text="Định mức cho 1 đơn vị công việc")
    # coefficient = models.FloatField(default=1)
    factor = models.FloatField(default=1)   # ✅ THÊM

    quantity = models.FloatField(help_text="Số lượng dự trù")

    class Meta:
        unique_together = ('work_item', 'material')

    def __str__(self):
        return f"{self.material.name} - {self.work_item.name}"

#MODEL VẬT TƯ TIÊU HAO THEO NHẬT KÝ
# class DailyLogMaterialUsage(models.Model):
#     daily_log_item = models.ForeignKey(
#         DailyLogItem,
#         related_name='materials',
#         on_delete=models.CASCADE
#     )
#     material = models.ForeignKey(Material, on_delete=models.CASCADE)
#     quantity_used = models.FloatField()

class DailyLogMaterialUsage(models.Model):
    daily_log_item = models.ForeignKey(
        DailyLogItem,
        related_name='material_usages',  # ✅ ĐỔI TÊN
        on_delete=models.CASCADE
    )
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity_used = models.FloatField()
