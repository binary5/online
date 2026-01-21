from import_export import resources,widgets
from teacher import models as tm
from .models import class_head_year,assessment, position, teacher,subject,job_title,honor_award
from import_export.fields import Field


class TeacheBooleanWidget(widgets.BooleanWidget):
    def render(self, value, obj):
        if value in self.NULL_VALUES:
            return "未知"
        return '是' if value else '否'
    def clean(self, value, row, *args, **kwargs):
        if value in self.NULL_VALUES:
            return None
        return True if value in ['是','师范'] else False
class degreeCompletionWidget(widgets.CharWidget):
    def render(self, value, obj):
        return obj.degree_of_completion()
class class_head_durationWidget(widgets.CharWidget):
    def render(self, value, obj=None):
        return obj.class_head_duration()
class MyM2MWidget(widgets.ManyToManyWidget):
    """
    解决导入导出中的多对多关系。
    若使用内置的ManyToManyWidget，
    只能对单独一个属性输入输出（默认是id）。
    本类重写了ManyToManyWidget的方法，
    可直接输入输出多个属性（须按格式）。
    为了防止误操作，导入只可添加，不可删改
    :param model: The model the ManyToMany field refers to (required).
    :param _separator: Defaults to ``'，'``.中文逗号分割不同对象, 若要自定义，切勿使用英文逗号
    :param connector: Defaults to ``'-'``.分隔多个属性的连接符
    :param fields: 要针对哪些字段进行匹配，有先后顺序
    """

    def __init__(self, model, separator=None, connector=None, fields=['pk'], reverse_priority=False, *args, **kwargs):
        super().__init__(model, *args, **kwargs)
        # 连接符和分隔符，最好不要用英文逗号和短横线
        if separator is None:
            separator = '，'
        if connector is None:
            connector = '_'
        self._connector = connector
        self._separator = separator
        self.reverse_priority = reverse_priority
        self.fields = fields
        if reverse_priority:
            self.fields.reverse() 

    def clean(self, value, row=None, *args, **kwargs):
        # 先找到对应的教师，记录其多对多关系现在ids
        tc = teacher.objects.filter(id_card_num=row['身份证号']).last()
        tc_m2m = tc.position.all() if tc else []
        ids = {str(o.id) for o in tc_m2m} if len(tc_m2m)!=0 else set()
        # 表格中若为空，继续维持原数据
        if not value:
            return super().clean(','.join(ids))
        # 表格中不为空，把格中数据格式化成二维列表。
        obj_str_sets = [
            list(reversed(item.split(self._connector)))
            if self.reverse_priority 
            else item.split(self._connector)
            for item in value.split(self._separator)
            # 连接符个数应比所需字段数少1，不符合格式的要排除
            if item.count(self._connector) <= self.fields.__len__()-1
        ]

        # 把新旧两个ids集合取并集，取并集是|，补充取并集是|=
        ids |= {    str(obj.id) 
            for obj,newCreate in [
                # 可能是有新的有旧的，所以用get_or_create
                self.model.objects.get_or_create(**{
                    self.fields[i]:item[i] 
                    for i in range(len(item))
                }) # 依据格子中的数据创建。依据self.fields决定要哪些属性
                for item in obj_str_sets
            ]
        }
        return super().clean(','.join(ids))

    def render(self, value, obj=None):
        if len(value.all()) == 0:
            return ''
        items = [widgets.smart_str(
            self._connector.join([
                getattr(obj,k) for k in 
                (list(reversed(self.fields)) 
                if self.reverse_priority 
                else self.fields
                )
            ])
        ) for obj in value.all()]
        map(lambda i:i.pop(0)if i[0]==self._connector else i,items)
        return self._separator.join(items)

class TeacherResource(resources.ModelResource):
    def __init__(self, form_fields=None):
        super(TeacherResource, self).__init__()
        self.form_fields = form_fields
        # 获取模型的字段列表, 
        field_list = teacher._meta.fields
        # 做成一个{字段名:中文名}的字典，作为成员变量
        self.vname_dict = {i.name:i.verbose_name for i in field_list}
    
    # 把英文字段名改为中文表头名
    def get_fields(self, **kwargs):
        fields = super().get_fields(**kwargs)
        for field in fields:
            field_name = self.get_field_name(field)
            # 自定义导出字段里可能有关联关系，但vname_dict肯定没有双下划线，所以必须处理
            if field_name.find("__") > 0:
                # 如果是关联关系的，只取字段名，不找关联，因为关联内容不在vname_dict里
                field_name = field_name.split("__")[0]
            
            if field_name in self.vname_dict.keys():
                field.column_name = self.vname_dict[field_name]
            if field_name == 'position':
                field.column_name = '现任职务'
        return fields
    
    # is_teacher_college = Field(attribute='is_teacher_college', widget=TeacheBooleanWidget())
    # is_teacher_major = Field(attribute='is_teacher_major', widget=TeacheBooleanWidget())
    # graduate_date = Field(attribute='graduate_date', widget=widgets.DateWidget(format="%Y/%m"))
    unit_employ_date = Field(attribute='unit_employ_date', widget=widgets.DateWidget(format="%Y/%m"))
    leave_date = Field(attribute='leave_date', widget=widgets.DateWidget(format="%Y/%m"))
    join_party_date = Field(attribute='join_party_date', widget=widgets.DateWidget(format="%Y/%m"))
    position_start = Field(attribute='position_start', widget=widgets.DateWidget(format="%Y/%m"))
    subject = Field(attribute='subject',widget=widgets.ForeignKeyWidget(subject, 'name'))
    position = Field(attribute='position',widget=MyM2MWidget(position,fields=['department','job'],reverse_priority=True))
    job_title = Field(attribute='job_title',widget=widgets.ForeignKeyWidget(job_title, 'name'))
    degree_of_completion = Field(attribute='id',widget=degreeCompletionWidget(),column_name='完成度')
    class_head_duration = Field(attribute='id',widget=class_head_durationWidget(),column_name='班主任年限')
    class Meta:
        model = teacher
        
        # fields内的模型字段讲会被导入导出, exclude内的会被排除在外
        fields=(
            'id',
            'name',
            'real_name',
            'id_card_num',
            'gender',
            'nation',
            'phone',
            'first_diploma',
            'first_degree',
            'graduate_college',
            'graduate_major',
            'is_teacher_major',
            'graduate_date',
            'final_diploma',
            'final_degree',
            'on_job_college',
            'on_job_major',
            'on_job_graduate_date',
            'job_title',
            'unit_employ_date',
            'leave_date',
            'politics',
            'join_party_date',
            'position',
            'position_rank',
            'position_start',
            'teach_grade',
            'subject',
            'qualifica_type',
            'head_class',
            'home_address',
            'current_address',
            'cadre_status',
            'employ_src',
            'job_status',
            'employ_unit',
            'regist_attribu',
            'remarks',
            'first_work_date',
            'salary_scale',
            'birth_place',
            'native_place',
            'updated_at',
            'person_photo'
        )

        # export_order（自定义） 选项设置导出字段的显式顺序
        export_order = (
            'name',
            'real_name',
            'id_card_num',
            'gender',
            'nation',
            'first_diploma',
            'first_degree',
            'graduate_college',
            'graduate_major',
            'is_teacher_major',
            'graduate_date',
            'final_diploma',
            'final_degree',
            'on_job_college',
            'on_job_major',
            'on_job_graduate_date',
            'job_title',
            'unit_employ_date',
            'leave_date',
            'politics',
            'join_party_date',
            'position',
            'position_rank',
            'position_start',
            'home_address',
            'cadre_status',
            'employ_src',
            'job_status',
            'employ_unit',
            'regist_attribu',
            'remarks',
            'first_work_date',
            'salary_scale',
            'degree_of_completion',
            'class_head_duration',
            'updated_at',
            'person_photo'
        )
        import_id_fields = ['name','id_card_num'] # 这里决定了update_or_create，可以避免重复导入

class BaseResource(resources.ModelResource):
    def __init__(self, mod):
        super().__init__()
        # 获取模型的字段列表, 
        field_list = mod._meta.fields
        # 做成一个{字段名:中文名}的字典，作为成员变量
        self.vname_dict = {i.name:i.verbose_name for i in field_list}
    teacher = Field(attribute='teacher',column_name='教师姓名',widget=widgets.ForeignKeyWidget(teacher,'name'))
    # 把英文字段名改为中文表头名
    def get_fields(self, **kwargs):
        fields = super().get_fields(**kwargs)
        for field in fields:
            field_name = self.get_field_name(field)
            if field_name in self.vname_dict.keys():
                field.column_name = self.vname_dict[field_name]
        return fields
    # class Meta:
        # exclude = ('id',)

class AssessResource(BaseResource):
    def __init__(self):
        super().__init__(assessment)

    # teacher = Field(attribute='teacher',column_name='教师',widget=widgets.ForeignKeyWidget(teacher,'name'))
    class Meta:
        model = assessment
        # exclude = ('id',)
        import_id_fields = ['teacher','year']
        fields=(
            'teacher',
            'year',
            'position',
            'degree',
            'description'
        )
class FamilyMember_Resource(BaseResource):
    def __init__(self):
        super().__init__(tm.family_member)
    living_together = Field(attribute='living_together', widget=TeacheBooleanWidget())
    class Meta:
        model = tm.family_member
        # exclude = ('id',)
        import_id_fields = ['teacher','name']
        # fields=(
        # )
# class class_head_durationWidget(widgets.CharWidget):
#     def render(self, value, obj=None):
#         return obj.class_head_duration()
class Class_head_yearResource(BaseResource):
    def __init__(self):
        super().__init__(class_head_year)
    teacher = Field(attribute='teacher',column_name='教师',widget=widgets.ForeignKeyWidget(teacher,'name'))
    # duration = Field(attribute='年数',column_name='年数',widget=widgets.DurationWidget)
    # def duration(self,start,end):
    #     if start.month == 9 : start -= datetime.timedelta(31)
    #     if None == end  : end = datetime.date.today()
    #     elif end.month == 6 : end += datetime.timedelta(30)
    #     return str((end-start) if end and start else datetime.timedelta())
    class Meta:
        model = class_head_year
        # exclude = ('id',)
        import_id_fields = ['teacher','start','category']
        esxport_order=(
            'id',
            'teacher',
            'category',
            'start',
            'end',
            'school_year',
            'head_class',
            'certifier',
            'description'
        )
# 职称经历导出源，包含姓名、职称、任现职称时间
class JobTitleExpResource(BaseResource):
    def __init__(self):
        super().__init__(tm.job_title_exp)
    # teacher = Field(attribute='teacher',column_name='姓名',widget=widgets.ForeignKeyWidget(teacher, 'name'))
    # id_card_num = Field(attribute='teacher',column_name='身份证号',widget=widgets.ForeignKeyWidget(teacher, 'id_card_num'))
    # attribute必须与模型中的字段名一致
    job_title = Field(attribute='job_title',column_name='职称',widget=widgets.ForeignKeyWidget(job_title, 'name'))
    class Meta:
        model = tm.job_title_exp
        # exclude = ('id','name','')
        import_id_fields = ['id']

class Honor_awardResource(BaseResource):
    def __init__(self):
        super().__init__(honor_award)
    class Meta:
        model = honor_award
        # exclude = ('id',)
        import_id_fields = ['id']
        export_order=(
            'teacher',
            'id',
            'name',
            'number',
            'issuer',
            'date',
            'photo'
        )
class study_exp_Resource(BaseResource):
    def __init__(self):
        super().__init__(tm.study_exp)
    is_final = Field(attribute='is_final', widget=TeacheBooleanWidget())
    class Meta:
        model = tm.study_exp
        exclude = ('experience_ptr',)
        # fields=(
        #     'teacher',
        #     'id',
        #     'start',
        #     'end',
        #     'academic',
        #     'categ_of_edu',
        #     'school',
        #     'major',
        #     'is_final',
        #     'diploma',
        #     'degree',
        #     'certifier',
        #     'photo'
        # )



class JobTitleResource(BaseResource):
    def __init__(self):
        super().__init__(job_title)
    class Meta:
        model = job_title
        # exclude = ('id',)
