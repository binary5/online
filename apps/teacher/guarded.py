from django.contrib.admin.utils import unquote
from django.contrib import messages, auth, admin
from django.utils.translation import gettext
from django.template.defaultfilters import length
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect, render
from guardian.admin import GuardedModelAdminMixin
from guardian.shortcuts import get_objects_for_user, assign_perm, remove_perm, get_users_with_perms, \
    get_groups_with_perms
import ast
from .models import teacher
class TeacherGuardedMixin(GuardedModelAdminMixin):
    # 自定义处理多个对象的被访问权限设置
    def obj_perms_manage_view(self, request, object_pk):
        # 有object_pk说明是走urls过来的单独对象，继续走默认路线
        if request.method == 'GET' or request.POST['ids']=='':
            return super().obj_perms_manage_view(request, object_pk)
        # 只有超管用户才能做此设置，非超管的打回
        if not request.user.is_superuser:
            post_url = reverse('admin:index', current_app=self.admin_site.name)
            return redirect(post_url)

        info = (
            self.admin_site.name,
            self.model._meta.app_label,
            self.model._meta.model_name,
        )
        
        obj = get_object_or_404(self.get_queryset(
            request), pk=unquote(object_pk))
        ids = request.POST['ids']
        if request.method == 'POST' and 'submit_manage_user' in request.POST:
            user_form = self.get_obj_perms_user_select_form(
                request)(request.POST)
            group_form = self.get_obj_perms_group_select_form(
                request)(request.POST)

            if user_form.is_valid():
                user_id = user_form.cleaned_data['user'].pk
                render = self.obj_perms_manage_user_view(request, object_pk, user_id, ids)
                return render
        elif request.method == 'POST' and 'submit_manage_group' in request.POST:
            user_form = self.get_obj_perms_user_select_form(
                request)(request.POST)
            group_form = self.get_obj_perms_group_select_form(
                request)(request.POST)

            if group_form.is_valid():
                group_id = group_form.cleaned_data['group'].id
                url = reverse(
                    '%s:%s_%s_permissions_manage_group' % info,
                    args=[obj.pk, group_id]
                )
                return redirect(url)
        url = reverse(
            '%s:%s_%s' % info,
        )
        return redirect(url)
    # 进入权限修改界面和提交权限修改内容，这里重写为可以处理多个对象
    def obj_perms_manage_user_view(self, request, object_pk, user_id, ids=None):
        if ids is None :
            if 'ids' not in request.POST or request.POST['ids']=='':
                return super().obj_perms_manage_user_view(request, object_pk, user_id)
            ids = request.POST['ids']
        if not self.has_change_permission(request, None):
            post_url = reverse('admin:index', current_app=self.admin_site.name)
            return redirect(post_url)
        
        queryset = self.get_queryset(request).filter(id__in=ast.literal_eval(ids))
        user = get_object_or_404(auth.get_user_model(), pk=user_id)
        obj = get_object_or_404(self.get_queryset(request), pk=object_pk)
        form_class = self.get_obj_perms_manage_user_form(request)
        forms = [form_class(user, obj, request.POST or None) for obj in queryset]
            
        if request.method == 'POST' and 'submit_manage_user'in request.POST:
            context = self.get_obj_perms_base_context(request, obj)
            context['user_obj'] = user
            # context['user_perms'] = get_user_perms(user, obj)
            context['form'] = forms[0]
            context['original'] = context['original']+'等%d人'%length(queryset)
            context['myUrl'] = './user-manage/%d/' % user.pk
            context['object'] = '，'.join([obj.name for obj in queryset]) + '共%d人'%length(queryset)
            context['ids'] = ids
            request.current_app = self.admin_site.name

            return render(request, self.get_obj_perms_manage_user_template(), context)

        if request.method == 'POST' and (False not in (form.is_valid()for form in forms)) :
            for form in forms:
                form.save_obj_perms()
            msg = gettext("Permissions saved.")
            messages.success(request, msg)
            info = (
                self.admin_site.name,
                self.model._meta.app_label,
                self.model._meta.model_name,
            )
            # url = reverse(
            #     '%s:%s_%s' % info,
            # )
            return redirect('../../../../')

    # 此选项开启后用户只能访问与自己账户设置了关联的对象
    user_can_access_owned_objects_only = True

    # 获取该用户的表权限
    def has_module_permission(self, request):
        # return True
        return super().has_module_permission(request)
            
        # return self.get_model_objs(request,'view').exists()

    # 重写，在显示数据列表时候，哪些数据显示，哪些不显示，由该函数控制
    # 如果是教师表，走原来的方法，配置user_can_access_owned_objects_only，这个函数可以实现让user只能访问有对应user的对象
    # 如果不是教师表，则是相关表，超管访问直接通过，其他用户就筛选对应教师是访问用户所对应的教师的那些
    def get_queryset(self, request):
        qs = super(admin.ModelAdmin, self).get_queryset(request)
        # 如果是超管或者组别是观察员，直接通过（未能实现）
        if request.user.is_superuser or request.user.groups.filter(name='观察员').exists():
            return qs
        if request.path[:23] == '/admin/teacher/teacher/':
            return super().get_queryset(request)
        if self.user_can_access_owned_objects_only and hasattr(request.user,'teacher'):
            filters = {'teacher': request.user.teacher}
            qs = qs.filter(**filters)
            return qs
        return ()
    # 在新建教师相关对象时，页面中的教师外键不能使其显示和输入（因为会显示到其他人），而是谁新建的就添加为谁
    # 超管用户在个人详情页添加不受影响，在相关表页面添加会报错，加入not request.user.is_superuser判断
    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser and hasattr(obj,'teacher') and obj.teacher == None:
            obj.teacher = request.user.teacher
        obj.save()
    # 自定义，内部用来获取某个用户有权限访问的对象
    # def get_model_objs(self, request, action=None, klass=None):
    #     opts = self.opts
    #     actions = [action] if action else ['view', 'change', 'delete']
    #     klass = klass if klass else opts.model
    #     model_name = klass._meta.model_name
    #     data = get_objects_for_user(
    #         user=request.user, 
    #         perms=[f'{perm}_{model_name}' for perm in actions],
    #         klass=klass, any_perm=True
    #     )
    #     if hasattr(request.user, 'teacher'):
    #         data = self.get_queryset(request) | data
        # return data
    # 自定义，用来判断某个用户是否有某个对象的查看、修改、删除权限
    # 如果obj为None，则为判断访问的用户是否有默认表的相关权限
    # def has_perm(self, request, obj, action):
    #     opts = self.opts
    #     codename = f'{action}_{opts.model_name}'
    #     if request.user.is_superuser:
    #         return True
    #     if obj and hasattr(request.user, 'teacher'):
    #         if isinstance(obj,teacher)  and obj == request.user.teacher:
    #             return True
    #         return obj.teacher == request.user.teacher
    #         return request.user.has_perm(f'{opts.app_label}.{codename}', obj)
    #     return True
        # return False
    # 是否有查看某个数据行的权限
    # def has_view_permission(self, request, obj=None):
        # if obj and request.user.teacher.pk == obj.teacher.pk:
        #     return True
        # return super().has_view_permission(request, obj)
        # return self.has_perm(request, obj, 'view')

    # 是否有修改某个数据行的权限
    # def has_change_permission(self, request, obj=None):
        # print('change',2)
        # return True
        # return super().has_change_permission(request, obj)
        # return self.has_perm(request, obj, 'change')

    # 是否有删除某个数据行的权限
    # def has_delete_permission(self, request, obj=None):
    #     return self.has_perm(request, obj, 'delete')

    # 用户应该拥有他新增的数据行的所有权限
    # def save_model(self, request, obj, form, change):
    #     result = super().save_model(request, obj, form, change)
    #     if not request.user.is_superuser and not change:
    #         opts = self.opts
    #         actions = ['view', 'add', 'change', 'delete']
    #         [assign_perm(f'{opts.app_label}.{action}_{opts.model_name}', request.user, obj) for action in actions]
    #     return result
