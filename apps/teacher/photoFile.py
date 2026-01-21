#修改和删除数据时，删除旧图片，保存新图
from django.db.models.signals import post_delete,post_save,post_init,pre_save
from django.dispatch.dispatcher import receiver
# 内部方法，保存旧图用于之后和新图比较
def _save_old_image(instance,fieldImg,attr):
    try:    # 防止旧图片已失效造成的错误
        # 旧图无字段
        if fieldImg.name=='':
            return
        # 是否有旧图, 无文件的会抛出
        fieldImg.file
        # 如果有旧图, 将旧图暂存备用
        instance.old_img = fieldImg
    except FileNotFoundError:
        # 针对图片字段还存在但文件没了，直接删除字段
        # 这里fieldImg是深拷贝，所以.delete(False)没用
        # 
        # fieldImg.delete(False)
        pass
    except ValueError:
        pass
# 和新图比较，检查图片是否需要移入回收站
import inspect
def _check_old_image(instance,fieldImg):

    # 如果新的文件fieldImg._file是None，说明是不带图片的普通保存, 那么图片字段不能动
    # if not fieldImg:
    # 如果新文件与当前文件路径不同，说明是修改，需要删除
    
    try:
        inspect.getmembers(fieldImg)
        if hasattr(instance,'old_img') and fieldImg and fieldImg._file and\
        (instance.old_img and (instance.old_img != fieldImg) and instance.old_img.name!=None):
            _delete_image(instance.old_img)
    except FileNotFoundError:
        return
# 移入回收站
def _delete_image(old_img):
        try:
            if old_img is None or (not hasattr(old_img,'name')) or old_img.name == None: return
            old_img.storage.save(
                '回收站/'+old_img.name,
                old_img.file
            )
            old_img.file.close()
            old_img.delete(False)
        except PermissionError:
            # 针对文件占用，使用.close()后已解决
            return
        except ValueError:
            # 针对删除无图片的对象
            return
        except FileNotFoundError:
            # 针对图片字段还存在但文件没了
            return

# honor_award删除后, 相关图片移入回收站
@receiver(post_delete, sender=study_exp)
@receiver(post_delete, sender=job_title_exp)
@receiver(post_delete, sender=honor_award)
def delete(sender, instance, **kwargs):
    _delete_image(instance.photo)
# honor_award保存前，暂存原图用于接下来判断是否有新图
@receiver(pre_save, sender= study_exp)
@receiver(pre_save, sender= job_title_exp)
@receiver(pre_save, sender= honor_award)
def save_old_image(sender, instance, **kwargs):
    if sender.objects.filter(pk=instance.pk).exists():
        _save_old_image(instance,sender.objects.get(pk=instance.pk).photo,'photo')
# honor_award保存后，检查旧图是否需要删除
@receiver(post_save, sender= study_exp)
@receiver(post_save, sender= job_title_exp)
@receiver(post_save, sender= honor_award)
def delete_old_image(sender, instance, **kwargs):
    _check_old_image(instance,instance.photo)
# teacher删除后, 相关图片移入回收站
@receiver(post_delete, sender=teacher)
def delete(sender, instance, **kwargs):
    _delete_image(instance.person_photo)
    _delete_image(instance.id_card_img1)
    _delete_image(instance.id_card_img0)
 
# teacher保存前
@receiver(pre_save, sender= teacher)
def save_old_image(sender, instance, **kwargs):
    if sender.objects.filter(pk=instance.pk).exists():
        _save_old_image(instance,sender.objects.get(pk=instance.pk).person_photo,'person_photo')
        _save_old_image(instance,sender.objects.get(pk=instance.pk).id_card_img1,'id_card_img1')
        _save_old_image(instance,sender.objects.get(pk=instance.pk).id_card_img0,'id_card_img0')
# teacher保存后
@receiver(post_save, sender= teacher)
def delete_old_image(sender, instance, **kwargs):
    _check_old_image(instance,instance.person_photo)
    _check_old_image(instance,instance.id_card_img1)
    _check_old_image(instance,instance.id_card_img0)