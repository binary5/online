from django.contrib import admin,auth
from django.conf import settings
# Register your models here.
from django.utils.safestring import mark_safe
from django.shortcuts import redirect, render
from django.template.defaultfilters import length
from django.urls import reverse
from django import db
from django.http import HttpResponsePermanentRedirect
from django.forms.widgets import DateInput, TextInput, FileInput
from import_export.admin import ImportExportModelAdmin,ExportActionMixin
from import_export.formats import base_formats
from django.db.models.query_utils import Q
from datetime import date
from .guarded_temp import TeacherGuardedMixin  # 临时使用空 mixin
from . import models, resource

admin.site.site_header = '乐一教职工信息系统'
admin.site.site_title = '乐一职工管理'

class ImageInput(FileInput):
    def render(self, name, value, attrs=None, renderer=None):  # django 2.2+
        output = []
        if value and getattr(value, "url", None):
            image_url = value.url
            file_name = str(value)
            output.append(u'''目前：<a href="%s" target="_blank"><img src="%s" alt="%s" width=50px /></a> 修改：''' % \
                          (image_url, image_url, file_name))
        print(super(FileInput, self).render(name, value, attrs))
        output.append(super(FileInput, self).render(name, value, attrs))
        return mark_safe(u''.join(output))
class TeacheImportExportModelAdmin(ImportExportModelAdmin,ExportActionMixin):
    formfield_overrides = {
        db.models.DateField: {"widget": DateInput(attrs={'type':'date'},format="%Y-%m-%d"),},
        db.models.CharField: {"widget": TextInput(attrs={'cols':10})},
        db.models.ImageField: {"widget": ImageInput()}
        }
    def get_import_formats(self):    #该方法是限制格式
        formats = (
            base_formats.XLSX,
        )
        return [f for f in formats if f().can_import() ]
    def get_export_formats(self):    #该方法是限制格式
        formats = (
            base_formats.XLSX,
        )
        return [f for f in formats if f().can_export()]
    # @admin.display(description='')
    # def img_show(slef, obj):
    #     img = obj.photo
    #     if img.name != '':
    #         return mark_safe(u'<img src="%s" width=100px />'%img.url)
    #     return '-'

    
# 日志记录
@admin.register(admin.models.LogEntry)
class LogEntry_Admin(admin.ModelAdmin):
    list_display = ['__str__','user','action_flag','object_repr','action_time']
    list_filter = ['action_flag']
    readonly_fields = ['__str__','action_flag','object_repr','action_time']
    actions = []
# 内置权限
@admin.register(auth.models.Permission)
class Permission_Admin(admin.ModelAdmin):
    actions = []

# 所有继承TeacherGuardedMixin必须加在TeacheImportExportModelAdmin前面，否则重写方法的原方法调取不到
@admin.register(models.assessment)
class Assess_Admin(TeacherGuardedMixin,TeacheImportExportModelAdmin):
    list_display = ['__str__','year','degree']
    actions = []
    list_filter = ['year']
    search_fields = ['teacher__name']
    readonly_fields = ['teacher','year','position',
            'degree','description']
    ordering = ['year']
    resource_class = resource.AssessResource

@admin.register(models.family_member)
class FamilyMember_Admin(TeacherGuardedMixin,TeacheImportExportModelAdmin,):
    list_display = ['__str__','teacher','call','name','phone','is_minor']
    actions = []
    date_hierarchy = 'birth_date'
    list_filter = ['living_together','politics']
    search_fields = ['teacher__name','name','phone','unit']
    readonly_fields = ['teacher']
    resource_class = resource.FamilyMember_Resource
    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.teacher = request.user.teacher
        super().save_model(request, obj, form, change)

@admin.register(models.Experience)
class Exp_Admin(TeacherGuardedMixin,TeacheImportExportModelAdmin,):
    readonly_fields = ['teacher','start','end','study_exp','work_exp','position_exp']
    list_display = ['__str__','start','end','study_exp','work_exp','position_exp']
    ordering = ['teacher__name','start']
    search_fields = ['teacher__name',]

@admin.register(models.class_head_year)
class HeadYearExp_Admin(Exp_Admin):
    list_display = ['__str__','category','start','end', 'head_class','is_full_year']
    actions = []
    list_filter = ['category','school_year','end']
    search_fields = ['school_year','teacher__name','head_class']
    readonly_fields = ['teacher']
    resource_class = resource.Class_head_yearResource
    ordering = ['start']
    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.teacher = request.user.teacher
        super().save_model(request, obj, form, change)
    
@admin.register(models.study_exp)
class StudyExp_Admin(Exp_Admin):
    list_display = ['__str__','teacher','diploma','degree','certifier','school','start','end','photo']
    list_editable = ['photo']
    search_fields = ['teacher__name','school','major']
    readonly_fields = ['teacher',]
    resource_class = resource.study_exp_Resource
    ordering = ['start']
    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.teacher = request.user.teacher
        super().save_model(request, obj, form, change)

@admin.register(models.work_exp)
class Work_exp_Admin(Exp_Admin):
    readonly_fields = ['teacher',]
    list_display = ['__str__','start','end','unit','job','certifier']
    search_fields = ['teacher__name','unit','job']
    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.teacher = request.user.teacher
        super().save_model(request, obj, form, change)

@admin.register(models.position_exp)
class Position_exp_Admin(Exp_Admin):
    readonly_fields = ['teacher',]
    list_display = ['__str__','start','end','unit','position','position_rank']

@admin.register(models.job_title_exp)
class JobTitleExp_Admin(TeacherGuardedMixin,TeacheImportExportModelAdmin,):
    list_display = ['__str__','job_title','issuer','date','appointment_date','photo']
    list_editable = ['photo']
    readonly_fields = ['teacher',]
    resource_class = resource.JobTitleExpResource
    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.teacher = request.user.teacher
        super().save_model(request, obj, form, change)

@admin.register(models.honor_award)
class HonorAward_Admin(TeacherGuardedMixin,TeacheImportExportModelAdmin,):
    readonly_fields = ['teacher',
                    #    'name','issuer','date','category'
                       ]
    list_filter = ['category',]
    list_display = ['__str__','name','issuer','date','category','photo']
    list_editable = ['photo']
    fields = ('teacher','category','name','issuer','date','number','degree','photo')
    resource_class = resource.Honor_awardResource
    search_fields = ['teacher__name','name','issuer','number']
    date_hierarchy = 'date'
    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.teacher = request.user.teacher
        super().save_model(request, obj, form, change)

def getThroughInline(model):
    global m
    m = model
    class TeacherThroughInline(admin.TabularInline):
        global m
        model = m.teacher.through
        ordering = ['teacher__name']
        # readonly_fields = ['name']
        extra = 0
    return TeacherThroughInline

@admin.register(models.position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('__str__','count_num')
    inlines = [getThroughInline(models.position)]
    ordering = ['department']

@admin.register(models.job_title)
class JobTitleAdmin(admin.ModelAdmin):
    list_display = ('__str__','job_level','count_num')
    exclude = ('teacher',)
    # inlines = [TeacherInline]
    # resource_class = JobTitleResource

# @admin.register(subject)
# class SubjectAdmin(TeacheImportExportModelAdmin):
#     resource_class = SubjectResource
#     list_display = ['name','count_num']


# class TeacherInline(admin.TabularInline):
#     model = models.teacher
#     fields = ['now_job_title_date','salary_scale','subject','job_status']
#     readonly_fields = ['now_job_title_date','salary_scale','subject','job_status']
#     extra = 0

class SinglInline(admin.TabularInline):
    extra = 0
    ordering = ['start']
    formfield_overrides = {
        db.models.DateField: {"widget": DateInput(attrs={'type':'date'},format="%Y-%m-%d"),},
        db.models.CharField: {"widget": TextInput(attrs={'cols':10})},
        db.models.ImageField: {"widget": ImageInput()}
        }
    # @admin.display(description='')
    # def img_show(slef, obj):
    #     img = obj.photo
    #     if img.name != '':
    #         return mark_safe(u'<img src="%s" width=100px />'%img.url)
    #     return '-'
class MultiInline(admin.StackedInline):
    extra = 0
    formfield_overrides = {
        db.models.DateField: {"widget": DateInput(attrs={'type':'date'},format="%Y-%m-%d"),},
        db.models.CharField: {"widget": TextInput(attrs={'cols':10})},
        db.models.ImageField: {"widget": ImageInput()}
        }
    # @admin.display(description='')
    # def img_show(slef, obj):
    #     img = obj.photo
    #     if img.name != '':
    #         return mark_safe(u'<img src="%s" width=100px />'%img.url)
    #     return '-'
class Class_head_yearInline(MultiInline):
    model = models.class_head_year
    extra = 0
    ordering = ['start']
    fields = (
        ('category','start','end',),
        ('school_year','head_class','certifier','description')
    )
class HonorAwardInline(MultiInline):
    model = models.honor_award
    fields = (
        ('name','issuer','date',),
        ('category','degree','number'),('photo',),
    )

class StudyExpInline(MultiInline):
    model = models.study_exp
    ordering = ['start']
    fields = (
        ('start', 'end','academic','categ_of_edu','is_final'),
        ('school','major','is_teacher_major'),
        ('diploma','degree','certifier'),
        ('photo',)
    )
class FamilyMemberInline(MultiInline):
    model = models.family_member
    fields = (
        ('category','call','name','phone','id_card_num'),
        ('living_together','politics','birth_date','unit','position')
    )

class JobTitleExpInline(SinglInline):
    model = models.job_title_exp
    ordering = ['date']
    fields = (
        'job_title','issuer','date','appointment_date',('photo',)
    )
class PositionExpInline(SinglInline):
    model = models.position_exp
class WorkExpInline(SinglInline):
    model = models.work_exp

# 教师信息表中的内容
global view_teach_info
view_teach_info = False
@admin.display(description='切换列表信息内容')
def change_list(modeladmin, request, queryset):
    global view_teach_info
    view_teach_info = not view_teach_info
@admin.display(description='修改所选的 教师信息')
def change_info(modeladmin, request, queryset):
    return HttpResponsePermanentRedirect('%s%d' % (request.path,queryset[0].pk))
@admin.action(permissions=["add"],description='设为新学年班主任')
def set_class_head(modeladmin, request, queryset):
    for t in queryset:
        models.class_head_year.objects.create(
            teacher=t,
            school_year='2021-2022',
            start=date(date.today().year,*settings.SCHOOL_YEAR_START),
            end=date(date.today().year+1,*settings.SCHOOL_YEAR_END)
        )
@admin.action(permissions=["add"],description='将所选教职工设为可登录')
def allow_login(modeladmin, request, queryset):
    g = auth.models.Group.objects.get(name='教职工')
    for t in queryset:
        if not (hasattr(t,'user') and t.user):
            t.user = auth.models.User.objects.create_user( 
                username=t.id_card_num, password=t.id_card_num[-8:], 
                is_staff=True,          first_name=t.name
                )
            t.save()
        t.user.groups.add(g)
@admin.action(permissions=["add"],description='设置被访问权限')
def objs_perms_manage_action(modeladmin, request, queryset):
    obj = queryset.first()
    # 选择的对象只有一个时，跳转到默认处理
    if length(queryset) == 1:
        info = (
            modeladmin.admin_site.name,
            modeladmin.model._meta.app_label,
            modeladmin.model._meta.model_name,
        )
        url = reverse(
            '%s:%s_%s_permissions' % info,
            args=[obj.pk]
        )
        return redirect(url)

    user_form = modeladmin.get_obj_perms_user_select_form(request)()
    group_form = modeladmin.get_obj_perms_group_select_form(request)()
    context = modeladmin.get_obj_perms_base_context(request, obj)
    # 以下是对base_context中部分内容的自定义
    context['user_form'] = user_form
    context['group_form'] = group_form
    context['original'] = context['original']+'等%d人'%length(queryset)
    context['myUrl'] = './%d/permissions/' % obj.pk
    context['names'] = '，'.join([obj.name for obj in queryset]) + '等%d人'%length(queryset)
    context['ids'] = [obj.id for obj in queryset]
    # https://github.com/django/django/commit/cf1f36bb6eb34fafe6c224003ad585a647f6117b
    # 选择完后交给模版去渲染
    return render(request, modeladmin.get_obj_perms_manage_template(), context)


@admin.register(models.teacher)
class TeacherAdmin(TeacherGuardedMixin,TeacheImportExportModelAdmin):
    # 详情表单页
    filter_horizontal=('position',)
    resource_class = resource.TeacherResource
    inlines = [
        HonorAwardInline,
        Class_head_yearInline,
        JobTitleExpInline,
        StudyExpInline,
        WorkExpInline,
        PositionExpInline,
        FamilyMemberInline
    ]
    fieldsets = [
        ('身份信息',{'fields': [
            'name','real_name','gender','nation',
            'id_card_num',
        ]}),
        ('个人信息',{'fields': [
            'phone','current_address',
            'politics','join_party_date',
            'native_place','birth_place','home_address',
            'health_condition'
        ]}),
        ('职业信息', {'fields': [
            'qualifica_type',
            'first_work_date','unit_employ_date',
            'regist_attribu','employ_unit',
            'job_title',
            'job_status','leave_date','remarks',
        ]}),
        ('非教学职务信息', {'fields': [
            'position','position_rank',
            'employ_src','position_start'
        ]}),
        ('教学任课信息', {'fields': [
            'subject','week_lessons','teach_grade','head_class'
        ]}),
        ('全日制学历', {'fields': [
            'graduate_college',
            'graduate_major','is_teacher_major',
            'first_diploma','graduate_date'
        ]}),
        ('在职学历（没有的请误填）', {'fields': [
            'on_job_college','on_job_major','on_job_graduate_date',
        ]}),# 函授有学历没有学位，同等学力有学位没有学历，所以在职的院校专业和学历学位信息必须分开
        ('工资用学历（最高学历）', {'fields': [
            'final_diploma', 'final_degree'
        ]}),
        ('照片上传(请保存完之前的信息之后再上传照片)',{'fields': [
            'person_photo','id_card_img1','id_card_img0',
        ]}),
    ]
    # 列表页
    actions = [change_info,set_class_head,change_list,allow_login,objs_perms_manage_action]
    list_filter = ['position__department','position__job','job_title','subject','teach_grade','employ_src',
                   'job_status','employ_unit','regist_attribu','nation']
    # list_editable = ['teach_grade']
    search_fields = ['name','home_address','id_card_num','remarks','phone','head_class']
    ordering = ['name']
    date_hierarchy = 'unit_employ_date'
    def get_list_display(self, request):
        if view_teach_info:
            return (
            'edit',
            'name',
            'gender',
            'job_title',
            'teach_grade',
            'class_head_duration',
            'head_class',
            'subject',
            'qualifica_type',
            'degree_of_completion',
            'updated_at'
        )
        return (
            'edit',
            'name',
            'first_work_date',
            'phone',
            'politics',
            'job_status',
            'employ_unit',
            'first_position',
            'degree_of_completion',
            'updated_at'
        )
# @admin.register(models.teacher)
class organ_cadre_Admin(TeacherAdmin):
    filter_horizontal=('position',)
    inlines = [
        HonorAwardInline,
        JobTitleExpInline,
        StudyExpInline,
        WorkExpInline,
        # PositionExpInline,
        FamilyMemberInline
    ]
    fieldsets = [
        ('个人身份信息',{'fields': [
            'real_name','gender',
            'nation','native_place','birth_place',
            'join_party_date','first_work_date','health_condition',
            'job_title','subject','person_photo',
        ]}),
        ('补充信息',{'fields': [
            'employ_unit','id_card_num' ,'phone'
        ]}),
        ('职业信息', {'fields': [
            'qualifica_type',
            'unit_employ_date',
            'regist_attribu','employ_unit',
            
            'job_status','leave_date','remarks',
        ]}),
        ('非教学职务信息', {'fields': [
            'position','position_rank',
            'employ_src','position_start'
        ]}),
        ('教学任课信息', {'fields': [
            'week_lessons','teach_grade','head_class'
        ]}),
        ('全日制教育', {'fields': [
            'first_diploma','first_degree',
            'graduate_college','graduate_major',
        ]}),
        ('最高学历或在职教育（没有的请误填）', {'fields': [
            'final_diploma', 'final_degree',
            'on_job_college','on_job_major'
        ]}),
    ]
    ordering = ['name']
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(Q(job_status='在岗'))
        
