from turtle import position
from django.test import TestCase
import re
from PIL import Image
import base64
from io import BytesIO
from .models import teacher,Experience,honor_award,family_member,assessment
from django.db.models.query_utils import Q
# Create your tests here.
class gbsp_Test(TestCase):
  def test(self):
    src_template='''<?xml version="1.0" encoding="utf-8"?>
<Person>
  <XingMing>{姓名}</XingMing>
  <XingBie>{性别}</XingBie>
  <ChuShengNianYue>{出生年月}</ChuShengNianYue>
  <MinZu>{民族}</MinZu>
  <JiGuan>{籍贯}</JiGuan>
  <ChuShengDi>{出生地}</ChuShengDi>
  <RuDangShiJian>{入党时间}</RuDangShiJian>
  <CanJiaGongZuoShiJian>{参加工作时间}</CanJiaGongZuoShiJian>
  <JianKangZhuangKuang>{健康状况}</JianKangZhuangKuang>
  <ZhuanYeJiShuZhiWu>{专业技术职务}</ZhuanYeJiShuZhiWu>
  <ShuXiZhuanYeYouHeZhuanChang></ShuXiZhuanYeYouHeZhuanChang>
  <QuanRiZhiJiaoYu_XueLi>{全日制教育学历}</QuanRiZhiJiaoYu_XueLi>
  <QuanRiZhiJiaoYu_XueWei>{全日制教育学位}</QuanRiZhiJiaoYu_XueWei>
  <QuanRiZhiJiaoYu_XueLi_BiYeYuanXiaoXi>{全日制学历毕业院校系}</QuanRiZhiJiaoYu_XueLi_BiYeYuanXiaoXi>
  <QuanRiZhiJiaoYu_XueWei_BiYeYuanXiaoXi>
  </QuanRiZhiJiaoYu_XueWei_BiYeYuanXiaoXi>
  <ZaiZhiJiaoYu_XueLi>{在职教育学历}</ZaiZhiJiaoYu_XueLi>
  <ZaiZhiJiaoYu_XueWei>{在职教育学位}</ZaiZhiJiaoYu_XueWei>
  <ZaiZhiJiaoYu_XueLi_BiYeYuanXiaoXi>{在职学历毕业院校系}</ZaiZhiJiaoYu_XueLi_BiYeYuanXiaoXi>
  <ZaiZhiJiaoYu_XueWei_BiYeYuanXiaoXi>
  </ZaiZhiJiaoYu_XueWei_BiYeYuanXiaoXi>
  <XianRenZhiWu>{现任职务}</XianRenZhiWu>
  <NiRenZhiWu>
  </NiRenZhiWu>
  <NiMianZhiWu>
  </NiMianZhiWu>
  <JianLi>{简历}</JianLi>
  <JiangChengQingKuang>{奖惩情况}</JiangChengQingKuang>
  <NianDuKaoHeJieGuo>{年度考核结果}</NianDuKaoHeJieGuo>
  <RenMianLiYou>
  </RenMianLiYou>
  <JiaTingChengYuan>
    {家庭成员}
  </JiaTingChengYuan>
  <ChengBaoDanWei>乐陵第一中学</ChengBaoDanWei>
  <JiSuanNianLingShiJian>20231024</JiSuanNianLingShiJian>
  <TianBiaoShiJian>20231024</TianBiaoShiJian>
  <TianBiaoRen>
  </TianBiaoRen>
  <ShenFenZheng>{身份证}</ShenFenZheng>
  <ZhaoPian>{照片}</ZhaoPian>
  <Version>3.2.1.16</Version>
</Person>
'''
    for t in teacher.objects.filter(
      # Q(job_status='在岗')
      Q(name='高培')
      #  &Q(job_title__name='管理九级')
      ).exclude().reverse():
      if t.first_position() and t.first_position().department == '工会': continue
      if t.first_position() and '校长' in t.first_position().job: continue
      print(t.name,(t.first_position() or t.teach_grade))

      resume = ''
      for e in Experience.objects.filter(teacher=t).order_by('start'):
        if hasattr(e,'study_exp') :
          if not e.study_exp.diploma in ['小学','初中','高中']:
            item = e.start.strftime("%Y.%m") + '--' + ('       ' if(not e.end)or(e.end.year==2024)else e.end.strftime("%Y.%m")) + '  ' + e.study_exp.school            
            if e.study_exp.major!='': item += (e.study_exp.major+'专业')
            if e.study_exp.diploma=='研究生': item += '硕士研究生'
            resume += item+'学习\n' if e.study_exp.categ_of_edu!='在职' else '（其间：'+item+'学习）\n'
        if hasattr(e,'work_exp'):
          end_time = '       ' if(not e.end)or(e.end.year>=2022)else e.end.strftime("%Y.%m")
          job = '教师' if e.work_exp.job=='' else e.work_exp.job
          resume += e.start.strftime("%Y.%m") + '--' + end_time + '  ' + e.work_exp.unit + job + '\n'
        if hasattr(e,'position_exp'):
          end_time = '       ' if(not e.end)or(e.end.year==2024)else e.end.strftime("%Y.%m")
          resume += e.start.strftime("%Y.%m") + '--' + end_time + '  ' + e.position_exp.position.department + e.position_exp.position.job + '\n'
      resume = resume[:-1]
      honor = ''
      for h in honor_award.objects.filter(teacher=t):
        if not h.issuer or '聘'in h.name \
          or '职称'in h.name \
            or '资格'in h.name \
              or '合格'in h.name \
                or '毕业'in h.name \
                  or '学位'in h.name \
                    or '学历'in h.name \
                      :
          continue
        honor += h.date.strftime("%Y{y}%m{m}").format(y='年',m='月')+"，经"+h.issuer+"批准，授予"+h.name+"；"
      if honor!='' : honor = honor[:-1]+"。" 
      else : honor = '无'
      assess = ''
      for a in assessment.objects.filter(Q(teacher=t)&(Q(year=2020)|Q(year=2021)|Q(year=2022))):
        if t.first_work_date.year == a.year:
          assess += a.year + '年参加工作，'
        if t.unit_employ_date.year == a.year:
          assess += a.year + '年调入本单位，'
        assess += a.year + "年年度考核" + a.degree + ';'
      if assess!='': 
        assess = assess[:-1] + "。"
      member = ''
      for m in family_member.objects.filter(teacher=t):
        if m.birth_date:
          生日 = m.birth_date.strftime("%Y%m")
        elif m.id_card_num:
          生日 = m.id_card_num[6:12]
        else :
          生日 = ''
        member += '''<Item>
              <ChengWei>{称谓}</ChengWei>
              <XingMing>{姓名}</XingMing>
              <ChuShengRiQi>{出生年月}</ChuShengRiQi>
              <ZhengZhiMianMao>{政治面貌}</ZhengZhiMianMao>
              <GongZuoDanWeiJiZhiWu>{工作单位及职务}</GongZuoDanWeiJiZhiWu>
            </Item>
        '''.format(
          称谓 = m.call,
          姓名 = m.name,
          出生年月 = 生日,
          政治面貌 = m.politics,
          工作单位及职务 = m.unit + m.position if len(m.unit+m.position)>4 else '乐陵市居民',
        )
      if t.first_position() == None or t.first_position().job == '班主任':
        position = '教师'
      elif t.first_position().department == '中心组'and '校'in t.first_position().job: 
        position = t.first_position().job
      elif t.first_position().department == '中心组':
        position = t.position.last().__str__() if len(t.position.all())>1 else '教师'
      else :
        position = t.first_position().__str__()
      base64_str = '' if not t.person_photo else img_deal(t.person_photo.path)
      # print(str(base64_str)[2:-1])
      target_text = src_template.format(
          姓名 = re.sub('[a-zA-Z]','',t.name if not t.real_name else t.real_name),
          性别 = t.gender,
          出生年月 = t.id_card_num[6:12],
          民族 = t.nation+"族",
          籍贯 = t.native_place,
          出生地 = t.birth_place,
          入党时间 = ''if not t.join_party_date else t.join_party_date.strftime("%Y%m"),
          参加工作时间 = ''if not t.first_work_date else t.first_work_date.strftime("%Y%m"),
          健康状况 = '健康',
          专业技术职务 = t.job_title.name if t.job_title else '',
          全日制教育学历 = t.first_diploma,
          全日制教育学位 = t.final_degree if(t.graduate_date==t.on_job_graduate_date)or \
             not t.on_job_graduate_date else('学士'if t.first_diploma=='大学'else''),
          全日制学历毕业院校系 = t.graduate_college + t.graduate_major,
          在职教育学历 = ''if(t.graduate_date==t.on_job_graduate_date)or \
             not t.on_job_graduate_date else t.final_diploma,
          在职教育学位 = ''if(t.graduate_date==t.on_job_graduate_date)or \
             not t.on_job_graduate_date else t.final_degree,
          在职学历毕业院校系 = ''if(t.graduate_date==t.on_job_graduate_date)or \
             not t.on_job_graduate_date else t.on_job_college+t.on_job_major,
          现任职务 = '乐陵第一中学' + position,
          简历 = resume,
          奖惩情况 = honor,
          年度考核结果 = assess,
          家庭成员 = member,
          身份证 = t.id_card_num,
          照片 = base64_str
      )

      
      with open('..\信息采集\\'+t.name+'.lrmx','w',encoding="utf-8") as f:
        f.write(target_text)
      print('信息采集\\'+t.name+'.lrmx')

def img_deal(path):
    img = Image.open(path)
    fmt = img.format
    w,h = img.size
    if w>h*376/460 :
      w = int(h*376/460)
      img = img.crop(((img.size[0]-w)/2, 0,(img.size[0]+w)/2, h))
    else:
      h = int(w*460/376)
      img = img.crop((0,(img.size[1]-h)/2, w, (img.size[1]+h)/2))
    if h>460:
      w = 376
      h = 460
      img.thumbnail((w, h))
  # 将图片存到buffer中
    output_buffer = BytesIO()
    img.save(output_buffer, format=fmt, quality=90)
  # 判断图片大小
    o_size = len(output_buffer.getvalue()) // 1024
    while o_size > 5120:
      print(1)
      img = Image.open(output_buffer)
      output_buffer.close()
      output_buffer = BytesIO()
    # 存时压缩，并再算大小
      img.save(output_buffer, format=fmt, quality=80)
      o_size = len(output_buffer.getvalue()) // 1024
    # 压缩达标后，转成b64字符串
    b64 = base64.b64encode(output_buffer.getvalue())
    output_buffer.close()
    return str(b64, encoding='utf8')
