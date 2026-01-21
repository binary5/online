from django.contrib import admin
from django.db import models
from django.db.models.query_utils import Q
import datetime
from django.conf import settings
from django.utils.html import format_html
# Create your models here.
@admin.display(description='')
def img_show(img,):
    # img = slef.photo
    if img.name != '':
        return format_html(u'<img src="{}" width=100px />',img.url)
    return '-'
class Politics(models.TextChoices):
    群众 = '群众'
    中共党员 = '中共党员'
    预备党员 = '预备党员'
    共青团员 = '共青团员'
    无党派 = '无党派'
    民主党派 = '民主党派'
class teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,null=True,blank=True,editable=True)
    # 身份信息
    job_num             =   models.CharField(max_length=10,verbose_name="工号",default='',blank=True)
    id_card_num         =   models.CharField(max_length=18,verbose_name="身份证号",null=True)
    def id_card_path1(instance, filename):
        return 'id_card_img/{0}_身份证人像面.{1}'.format(instance.name,filename.split('.')[-1])
    id_card_img1        =   models.ImageField(upload_to=id_card_path1,verbose_name="身份证人像面",null=True,blank=True)
    def id_card_path0(instance, filename):
        return 'id_card_img/{0}_身份证国徽面.{1}'.format(instance.name,filename.split('.')[-1])
    id_card_img0        =   models.ImageField(upload_to=id_card_path0,verbose_name="身份证国徽面",null=True,blank=True)
    name                =   models.CharField(max_length=10,verbose_name="姓名",help_text='如果其他人与您有重名，请在名字后面加学科首字母')
    real_name           =   models.CharField(max_length=6,verbose_name="身份证姓名",null=True,blank=True,help_text='如果平时使用的姓名与身份证姓名不一致，在此填写身份证姓名')
    gender              =   models.CharField(max_length=2,verbose_name="性别",choices=(('男','男'),('女','女')))
    class Nation(models.TextChoices):
        汉 = '汉'
        回 = '回'
        满 = '满'
        蒙古 = '蒙古'
        其他 = '其他'
    nation              =   models.CharField(max_length=6,verbose_name="民族",choices=Nation.choices)

    # 职业
    politics            =   models.CharField(max_length=4,verbose_name="政治面貌",choices=Politics.choices,blank=True,null=True)
    join_party_date     =   models.DateField(verbose_name="入党时间",blank=True,null=True,help_text='非党员勿填；可直接在框中输入，格式：年/月/日')
    qualifica_type      =   models.CharField(max_length=10,verbose_name="教师资格证类型",blank=True,default='',help_text='教资证上的类型+学科，填写样例：“初中语文”，“高中数学”；教师资格证详细信息和照片填入下面的“证书汇总”')
    unit_employ_date    =   models.DateField(verbose_name='进入本单位日期',null=True,help_text='格式：年/月/日',blank=True)
    first_work_date     =   models.DateField(verbose_name='首次参加工作日期',null=True,help_text='①可直接在框中输入，格式：年/月/日；②来一中以前有工作经历且工龄已经续上的可写连续工龄开始的时间')
    employ_unit         =   models.CharField(max_length=20,verbose_name="任职单位",blank=True,default='乐陵第一中学')
    regist_attribu      =   models.CharField(max_length=20,verbose_name="编制所在单位",blank=True,default='乐陵第一中学')
    salary_scale        =   models.CharField(max_length=4,verbose_name="级别(薪级)",blank=True,default='')

    class Job_status(models.TextChoices):
        在岗 = '在岗'
        在岗借出 = '在岗借出'
        在岗借入 = '在岗借入'
        调走 = '调走'
        离退休 = '离退休'
        病休 = '病休'
        工资停发 = '工资停发'
        辞职 = '辞职'
        离职 = '离职'
    job_status          =   models.CharField(max_length=6,verbose_name="岗位状态",default='在岗',choices=Job_status.choices)
    leave_date          =   models.DateField(verbose_name='变动时间',null=True,blank=True,default=None,help_text='在岗勿填；可直接在框中输入，格式：年/月/日')
    remarks             =   models.TextField(verbose_name='备注',default='',blank=True,help_text='此处可填写特殊情况、产假病假起止情况等')
    cadre_status        =   models.CharField(max_length=6,verbose_name="身份",default='干部',choices=(('干部','干部'),('聘干','聘干')),help_text='自己不了解的默认是干部')
    job_title           =   models.ForeignKey(to='job_title',on_delete=models.CASCADE,verbose_name="技术职称",null=True,blank=True,related_name='teacher',help_text='选择本人当前的职称即可')
    @admin.display(description='现职称聘任日期')
    def now_job_title_date(self):
        return self.job_title_exp.latest('appointment_date').appointment_date
    # 工作职务
    class Job_rank(models.TextChoices):
        副县 = '副县'
        正科 = '正科'
        副科 = '副科'
    position            =   models.ManyToManyField(to='position',verbose_name='现任职务',blank=True,related_name='teacher',help_text='① 非必填，没有兼任职务的不要填； ②')
    position_rank       =   models.CharField(max_length=4,verbose_name='职务级别',blank=True,default='',choices=Job_rank.choices,help_text='非必填，没有兼任行政职务的不要填') 
    class Employ_src(models.TextChoices):
        教体局 = '教体局'
        市机关能效办 = '市机关能效办公室'
        学校 = '学校'
        乐陵市委组织部 = '组织部'
    employ_src          =   models.CharField(max_length=10,verbose_name="任命/批准机关",blank=True,default='',choices=Employ_src.choices,help_text='自己不了解的请勿填写')
    @admin.display(description='第一职务')
    def first_position(self):
        return self.position.first()
    position_start   =   models.DateField(verbose_name="任现行政职务时间",blank=True,null=True,help_text='没有非教学职务的勿填，可直接在框中输入，格式：年/月/日')
    subject             =   models.ForeignKey(to='subject',on_delete=models.CASCADE,verbose_name="任课学科",null=True,blank=True,related_name='teacher')
    week_lessons        =   models.IntegerField(verbose_name='周课时量',blank=True,null=True,)
    teach_grade         =   models.CharField(max_length=7,verbose_name="所属级部",blank=True,default='',help_text='填写样例：“2021级二部”、“2020级一部”，不要写成“高二1部”')
    head_class          =   models.CharField(max_length=8,verbose_name="当前班主任班级",blank=True,default='',help_text='目前担任班主任的请填写，填写样例：“2021级1班”')
    # 学历
    first_diploma       =   models.CharField(max_length=10,verbose_name="全日制学历",blank=True,default='')
    first_degree        =   models.CharField(max_length=10,verbose_name="全日制学位",help_text="不能只写“学士”，要写全称，例如“工学学士”、“教育学硕士”",blank=True,default='')
    graduate_college    =   models.CharField(max_length=16,verbose_name="全日制学历毕业院校",help_text="请写院校全称",blank=True,default='')
    graduate_major      =   models.CharField(max_length=16,verbose_name="全日制专业",blank=True,default='')
    graduate_date       =   models.DateField(verbose_name="全日制学历毕业时间",blank=True,null=True,help_text='可直接在框中输入，格式：年/月/日')
    is_teacher_college  =   models.BooleanField(verbose_name="是否师范院校",blank=True,null=True)
    is_teacher_major    =   models.BooleanField(verbose_name="是否师范专业",blank=True,null=True)

    final_diploma       =   models.CharField(max_length=12,verbose_name="最高学历(工资用)",blank=True,default='')
    final_degree        =   models.CharField(max_length=12,verbose_name="最高学位(工资用)",help_text="不能只写“学士”，要写全称，例如“工学学士”、“教育学硕士”",blank=True,default='无')
    # 函授有学历没有学位，同等学力有学位没有学历，所以在职的院校专业和学历学位信息必须分开
    on_job_college =   models.CharField(max_length=20,verbose_name="在职学历院校",help_text="请写院校全称",blank=True,default='')
    on_job_major =   models.CharField(max_length=20,verbose_name="在职学历专业",blank=True,default='')
    on_job_graduate_date=   models.DateField(verbose_name='在职学历制毕业时间',null=True,blank=True,help_text='可直接在框中输入，格式：年/月/日')
    # 个人信息
    phone               =   models.CharField(max_length=14,verbose_name="手机号码",blank=True,default='')
    home_address        =   models.CharField(verbose_name="原家庭住址",max_length=64,default='',help_text='具体到乡镇或街道，与身份证地址相匹配')
    native_place        =   models.CharField(verbose_name="籍贯(省县)",max_length=12,default='',help_text='具体到省县，例如“山东乐陵”')
    birth_place         =   models.CharField(verbose_name="出生地(省县)",max_length=12,default='',help_text='身份证前六位代码的区划，具体到省县，例如“山东乐陵”')
    current_address     =   models.CharField(verbose_name="现住址",max_length=64,blank=True,default='',help_text='具体到门牌号')
    health_condition    =   models.CharField(verbose_name="健康状况",max_length=18,default='健康',help_text='根据本人的具体情况填写“健康” “一般”或“较差”；有严重疾病、慢性疾病或身体伤残的，要如实简要填写。最多允许输入18个汉字。')
    # 数据
    updated_at          =   models.DateTimeField(verbose_name='最后修改时间', auto_now=True)
    def person_photo_path(instance, filename):
        return 'person_photo/{0}_{1}.{2}'.format(instance.name,instance.id_card_num,filename.split('.')[-1])
    person_photo        =   models.ImageField(upload_to=person_photo_path,verbose_name="个人照片",blank=True,null=True,help_text='一寸或两寸证件照，不要大于1MB')
    @admin.display(description='完成度')
    def degree_of_completion(self):
        cnt = 0
        for k in self.__dict__:
            cnt += 1 if (self.__dict__[k] != None 
                and self.__dict__[k] != '') else 0
        return '%.2f％' % (cnt/len(self.__dict__)*100)
    class Meta:
        db_table = ''
        managed = True
        verbose_name = '教师'
        verbose_name_plural = '★教师信息'
        constraints = [
            models.UniqueConstraint(fields=['id_card_num'],name='id_uni',condition=Q(id_card_num__isnull=False)),
            models.UniqueConstraint(fields=['name'],name='name_uni')
        ]
    @admin.display(description='教师姓名')
    def __str__(self):
        return self.name
    @admin.display(description='是否现任班主任')
    def now_class_head(self):
        # TODO 可能有bug
        today = datetime.date.today()
        years = self.class_head_year.filter(school_year__contains=today.year)
        for y in years:
            if y.start and y.end and today > y.start and today < y.end :
                return '是'
        return '否'
    @admin.display(description='班主任年限')
    def class_head_duration(self):
        sum = datetime.timedelta()
        for year in self.class_head_year.all():
            if year.is_full_year == '是':
                sum += datetime.timedelta(300)
            else :
                # if year.start.month == 9 : year.start -= datetime.timedelta(31)
                # if None == year.end  : year.end = datetime.date.today()
                # elif year.end.month == 6 : year.end += datetime.timedelta(30)
                sum += (year.end-year.start) if year.end and year.start else datetime.timedelta()
        return "%.1f年"%(int(sum.days)/300)
    @admin.display(description='编辑')
    def edit(self):
        return '编辑'
class subject(models.Model):
    name        = models.CharField(max_length=7,verbose_name='学科名称')
    will_gaokao = models.BooleanField(verbose_name='是否高考科目',default=False)
    def __str__(self):
        return self.name
    @admin.display(description='人数')
    def count_num(self):
        return len(self.teacher.all())
    class Meta:
        db_table = ''
        managed = True
        verbose_name = '学科'
        verbose_name_plural = '学科'

class position(models.Model):
    department = models.CharField(max_length=16,verbose_name='所属部门',blank=True)
    job = models.CharField(max_length=16,verbose_name='职务')
    @admin.display(description='人数')
    def count_num(self):
        return len(self.teacher.all())
    def __str__(self) -> str:
        return self.department + self.job
    class Meta:
        db_table = ''
        managed = True
        verbose_name = '职务'
        verbose_name_plural = '职务'
        constraints = [
            models.UniqueConstraint(fields=['department','job'],name='department_job_unique')
        ]

class job_title(models.Model):
    name = models.CharField(max_length=5,verbose_name='职称名')
    job_level = models.CharField(max_length=8,verbose_name='职务层次',blank=True)
    salary_type = models.CharField(max_length=12,verbose_name='工资类型',blank=True)
    salary_position = models.CharField(max_length=7,verbose_name='工资职务(技术等级、岗位)',blank=True)
    Qualification_Code = models.CharField(max_length=8,verbose_name="专业技术资格代码"	,blank=True)
    Qualification_Name = models.CharField(max_length=12,verbose_name="专业技术资格名称",blank=True)
    Acquisition_Pathway = models.CharField(max_length=4,verbose_name="获得资格途径",choices=(('评审','评审'),('考试','考试'),('特批','特批'),('考核认定','考核认定'),('其他','其他')),blank=True)
    def __str__(self):
        return self.name
    @admin.display(description='人数')
    def count_num(self):
        return len(self.teacher.all())
    class Meta:
        db_table = ''
        managed = True
        verbose_name = '职称'
        verbose_name_plural = '职称'

class job_title_exp(models.Model):
    job_title = models.ForeignKey(verbose_name='职称',to='job_title',on_delete=models.PROTECT)
    teacher = models.ForeignKey(verbose_name='教师',to='teacher',on_delete=models.CASCADE,null=True,editable=False)
    issuer = models.CharField(max_length=30,verbose_name='职称评审机构',null=True,blank=True,help_text='要写全称，例如：山东省乐陵市中小学教师初级职称评审委员会')
    date = models.DateField(verbose_name='职称评定时间（获得资格日期）',null=True,help_text='可直接在框中输入，格式：年/月/日；以职称证或职称网站为准，记不清的精确到年，月日都写1')
    appointment_date = models.DateField(verbose_name='职务起始(首次聘任时间)',blank=True,null=True,help_text='未聘可不填，以聘任文件或证明为准；可直接在框中输入，格式：年/月/日')
    def job_title_photo_path(instance, filename):
        return 'award_photo/{0}_{1}.{2}'.format(instance.teacher,instance.job_title.__str__(),filename.split('.')[-1])
    photo = models.ImageField(verbose_name='职称材料',upload_to=job_title_photo_path,null=True,blank=True,help_text='上传职称证，或职称证与聘任材料的拼图；尽量不要大于1M')
    
    def __str__(self) -> str:
        return self.teacher.name + '_' + self.job_title.__str__()

    class Meta:
        verbose_name = '职称经历'
        verbose_name_plural = '职称变化情况'
        constraints = [
            models.UniqueConstraint(fields=['job_title','teacher','date'],name='job_title_exp_uni')
        ]

class Experience(models.Model):
    teacher = models.ForeignKey(to='teacher',on_delete=models.CASCADE,related_name='%(class)s',editable=False)
    start = models.DateField(verbose_name='起始日期',null=True,help_text='格式：年/月/日')
    end = models.DateField(verbose_name='终止日期',null=True,blank=True,help_text='本阶段未结束可不填，格式：年/月/日')
    class Meta:
        verbose_name = '经历'
        verbose_name_plural = '全部经历'
class position_exp(Experience):
    position = models.ForeignKey(verbose_name='职务',to='position',on_delete=models.PROTECT,null=True)
    position_rank = models.CharField(max_length=4,verbose_name='职务级别',blank=True,default='无',choices=[('无','无'),('副县','副县'),('正科','正科'),('副科','副科')],help_text='非必填，不是领导的不要填') 
    unit = models.CharField(verbose_name='工作单位',max_length=20,blank=True)
    class Meta:
        verbose_name = '中心组任职经历'
        verbose_name_plural = '中心组任职经历'
        constraints = [
            models.UniqueConstraint(fields=['experience_ptr_id','position','unit'],name='teacher_position_unique')
        ]
    def __str__(self) -> str:
        return self.teacher.name + self.position.__str__()

class study_exp(Experience):
    def diploma_photo_path(instance, filename):
        return 'award_photo/{0}_{1}.{2}'.format(instance.teacher,instance.diploma,filename.split('.')[-1])
    is_final = models.BooleanField(verbose_name='是最高学历',default=False)
    academic = models.CharField(max_length=4,verbose_name="学制(几年)",choices=(('1年','1年'),('2年','2年'),('3年','3年'),('4年','4年'),('5年','5年')),blank=True,default='')
    categ_of_edu = models.CharField(max_length=4,choices=(('在职','在职'),('全日制','全日制')),verbose_name="学历类别",null=True)
    school = models.CharField(max_length=16,verbose_name="就读学校")
    major = models.CharField(max_length=16,verbose_name="所学专业",blank=True)
    is_teacher_major = models.CharField(max_length=5,choices=(('师范','是师范专业'),('非师范','非师范专业')),verbose_name="是否师范专业",blank=True,null=True)
    diploma = models.CharField(max_length=10,verbose_name="学历",choices=(('初中','初中'),('高中','高中'),('中专','中专'),('大专','大专'),('大学本科','大学本科'),('党校本科','党校本科'),('研究生','研究生')))
    degree  = models.CharField(max_length=10,verbose_name="学位",blank=True,default='无')
    certifier = models.CharField(verbose_name='证明人',blank=True,max_length=10)
    photo = models.ImageField(verbose_name='学历材料',upload_to=diploma_photo_path,null=True,blank=True,help_text='上传毕业证，或毕业证与学位证的拼图；尽量不要大于1M')
    def __str__(self) -> str:
        return self.teacher.name + self.diploma + "阶段"

    class Meta:
        verbose_name = '学业经历（高中开始）'
        verbose_name_plural = '学业经历'
        constraints = [
            models.UniqueConstraint(fields=['experience_ptr_id',],name='study_exp_uni'),
            # 有专业的学历专业必填，填写专业后是否师范必填
            # 因为添加Constraint的前提是已存在的数据符合条件，所以暂时加不了
            # models.CheckConstraint(
            #     check=(Q(diploma__in=['初中','高中']) | ~Q(major='')),
            #     name='专业必填'
            # ),
            # models.CheckConstraint(
            #     check=(Q(major='') | Q(is_teacher_major__isnull=False)),
            #     name='是否师范必填'
            # ),
        ]
class work_exp(Experience):
    at_village = models.BooleanField(verbose_name='在乡镇教学一线',default=False)
    unit = models.CharField(verbose_name='工作单位',max_length=20)
    job = models.CharField(max_length=20,verbose_name='职务',blank=True)
    certifier = models.CharField(verbose_name='证明人',blank=True,max_length=10)
    class Meta:
        verbose_name = '工作经历'
        verbose_name_plural = '工作经历'
        constraints = [
            models.UniqueConstraint(fields=['experience_ptr_id','job','certifier','unit',],name='work_exp_uni')
        ]
    def __str__(self) -> str:
        return self.teacher.name + self.unit 

class honor_award(models.Model):
    def honor_photo_path(instance, filename):
        return 'award_photo/{0}_{1}{2}.{3}'.format(instance.teacher,instance.date.__str__()[:4],instance.name,filename.split('.')[-1])
    class awards(models.TextChoices):
        个人荣誉证书 = '个人荣誉'
        教学与课程证书 = '教学与课程'
        竞赛与考试获奖 = '竞赛与考试'
        科研与论文 = '科研与论文'
        职业资格证书 = '职业资格'
        惩罚认定 = '惩罚认定'
    category    = models.CharField(max_length=30,verbose_name='证书类别',choices=awards.choices,null=True,blank=True,help_text='')
    teacher     = models.ForeignKey(verbose_name='对应教师',to='teacher',on_delete=models.CASCADE,null=True,editable=False)
    name        = models.CharField(max_length=30,verbose_name='证书名称',help_text='必须与证书一致')
    issuer      = models.CharField(max_length=30,verbose_name='落款单位',null=True,help_text='与印章一致')
    date        = models.DateField(verbose_name='颁发日期',help_text='格式：年/月/日')
    number      = models.CharField(max_length=30,verbose_name='证书编号',null=True,blank=True,help_text='证书上有编号的填入编号，比如教师资格证编号')
    degree      = models.CharField(max_length=10,verbose_name='级别',null=True,blank=True,help_text='填写地区级别、奖级、等级、成绩等')
    photo       = models.ImageField(verbose_name='证书图片',upload_to=honor_photo_path,null=True,blank=True,help_text='尽量不要大于1M')
    def __str__(self):
        if self.teacher:
            return self.teacher.name + self.name
        return '-'

    class Meta:
        db_table = ''
        managed = True
        verbose_name = '证书或奖惩'
        verbose_name_plural = '证书或奖惩汇总'
        constraints = [
            models.UniqueConstraint(fields=['name','teacher','issuer','date'],name='award_uni')
        ]

class class_head_year(models.Model):
    class categorys(models.TextChoices):
        正班主任='正班主任'
        副班主任='副班主任'
        备课组长='备课组长'
        学科组长='学科组长'
        主备人='主备人'
        实验班教师='实验班教师'
        # categorys.choices
    teacher = models.ForeignKey(to='teacher',verbose_name='教师',on_delete=models.CASCADE,related_name='%(class)s',editable=False) 
    category = models.CharField(verbose_name='类别',choices=categorys.choices,default='正班主任',max_length=5)
    start = models.DateField(verbose_name='起始日期',null=True,help_text='格式：年/月/日')
    end = models.DateField(verbose_name='终止日期',null=True,blank=True,help_text='格式：年/月/日')
    school_year = models.CharField(verbose_name='学年度',max_length=10,default='2021-2022',help_text='样例：2021-2022')
    certifier = models.CharField(verbose_name='证明人',blank=True,max_length=10)
    head_class = models.CharField(verbose_name='班主任班级',max_length=40,null=True,blank=True,help_text='样例：2000级00班')
    description = models.CharField(verbose_name='备注',max_length=32,null=True,blank=True)
    
    @admin.display(description='是否全年')
    def is_full_year(self):
        if self.end and self.start:
            return '是'if self.end - self.start >= datetime.timedelta(days=300) else '否'
        return '待定'
    def __str__(self) -> str:
        return self.teacher.name + self.school_year + self.category
    class Meta:
        db_table = ''
        managed = True
        verbose_name = '班主任或学科组任职经历'
        verbose_name_plural = '班主任或学科组任职经历'
        constraints = [
            models.UniqueConstraint(fields=['teacher','category','start'],name='class_head_year_uni')
        ]

class assessment(models.Model):
    teacher = models.ForeignKey(to='teacher',verbose_name='教师',on_delete=models.CASCADE,related_name='%(class)s',editable=False)
    year = models.CharField(verbose_name='考核年',max_length=4,help_text='四位阿拉伯数年份')
    class Dgree(models.TextChoices):
        不定等次 = '不定等次'
        合格 = '合格'
        优秀 = '优秀'
        未参加考核 = '未考核'
    position = models.CharField(verbose_name='时任职务',max_length=10,default='教师')
    degree = models.CharField(verbose_name='等次',max_length=4,default='不定等次',choices=Dgree.choices,help_text='如实填写')
    description = models.CharField(verbose_name='备注',max_length=32,null=True,blank=True)
    def __str__(self) -> str:
        return str(self.year) + str(self.teacher.name) + str(self.degree)
    class Meta:
        db_table = ''
        managed = True
        verbose_name = '年度考核情况'
        verbose_name_plural = '年度考核情况'
        constraints = [
            models.UniqueConstraint(fields=['teacher','year',],name='assessment_year_uni')
        ]
class family_member(models.Model):
    living_together = models.BooleanField(verbose_name='是共同居住人',default=False)
    teacher = models.ForeignKey(to='teacher',on_delete=models.CASCADE)
    fm_choices = (
        ('父母','父母'),
        ('配偶及其父母','配偶及其父母'),
        ('本人的兄弟姐妹','本人的兄弟姐妹'),
        ('配偶的兄弟姐妹','配偶的兄弟姐妹'),
        ('子女、子女的配偶及其父母（1）','子女、子女的配偶及其父母（1）'),
        ('子女、子女的配偶及其父母（2）','子女、子女的配偶及其父母（2）'),
        ('直系和三代以内旁系亲属现任或曾任科级及以上职务，以及移居国（境）外的人员','直系和三代以内旁系亲属现任或曾任科级及以上职务，以及移居国（境）外的人员')
    )
    category = models.CharField(verbose_name='类别',max_length=75,choices=fm_choices,default='',blank=True)
    call = models.CharField(verbose_name='称谓',max_length=4,null=True,help_text='例如：妻子，丈夫，儿子，女儿，父亲，母亲，岳父，岳母，公公，婆婆')
    name = models.CharField(verbose_name='姓名',max_length=6)
    phone = models.CharField(max_length=14,verbose_name="手机号码(至少填一个)",blank=True,null=True)
    birth_date = models.DateField(verbose_name='出生年月',null=True,blank=True,help_text='无法确认的可以精确到月')
    id_card_num  =   models.CharField(max_length=18,verbose_name="身份证号",null=True,blank=True)

    politics = models.CharField(max_length=4,verbose_name="政治面貌",choices=Politics.choices)
    unit = models.CharField(verbose_name='工作单位',max_length=20,help_text='尽量写具体，已吊销的单位在名称前加“原”')
    position = models.CharField(verbose_name='职务（职级）',max_length=20,help_text='尽量写具体，已退休的在职务名前加“原”')
    def __str__(self) -> str:
        return self.teacher.name + \
        self.call + \
        self.name
    @admin.display(description='是否成年')
    def is_minor(self):
        if self.birth_date is None :
            return '年龄未知'
        today = datetime.date.today()
        birth_18 = datetime.date(self.birth_date.year+18,self.birth_date.month,self.birth_date.day)
        return '成年' if today >= birth_18 else '未成年'
    class Meta:
        verbose_name = '家庭成员（包括父母、兄弟姐妹）'
        verbose_name_plural = '家庭成员'
        constraints = [
            models.UniqueConstraint(fields=['teacher','name'],name='家庭成员不重复')
        ]


    
    
    # from django.db import connections    
    # 保存完成后释放数据库链接
    # connections.close_all()
