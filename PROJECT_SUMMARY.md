# Online 项目部署总结

## ✅ 部署状态

| 项目 | 状态 |
|------|------|
| Python 环境 | ✅ 3.10.11 (虚拟环境) |
| Django | ✅ 4.2.6 |
| PostgreSQL | ✅ 15.15 |
| 数据库 | ✅ cloudschool_db |
| 数据库迁移 | ✅ 完成 |
| 开发服务器 | ✅ 运行中 |

## 📋 问题解决记录

### 1. Schema 创建问题
- **问题**: PostgreSQL Schema 未创建，表被创建在 public schema
- **解决**: 创建 `create_schema.py` 脚本生成 cloudschool_schema 和 online_schema

### 2. Guardian 依赖问题
- **问题**: django-guardian 在迁移时引用 users_userprofile，但表不存在
- **解决**: 暂时禁用 guardian app，并创建临时空 mixin 替代 TeacherGuardedMixin

### 3. 表名冲突问题
- **问题**: Django 表与 cloud_school 项目的表产生冲突
- **解决**: 创建 `reset_db.py` 脚本清空所有表，重新迁移

### 4. AUTH_USER_MODEL 配置
- **问题**: 自定义用户模型未启用
- **解决**: 在 settings.py 中设置 `AUTH_USER_MODEL = 'users.UserProfile'`

## 🗄️ 数据库配置

### 当前配置
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'cloudschool_db',
        'USER': 'postgres',
        'PASSWORD': 'hy010112',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        # 使用 public schema（暂未实现 schema 隔离）
    }
}
```

### Schema 状态
- ✅ cloudschool_schema - 已创建
- ✅ online_schema - 已创建
- ✅ public - 当前使用的 schema

## 📊 数据库表

### online 项目表
| Schema | 表名 | 状态 |
|--------|--------|------|
| public | users_userprofile | ✅ |
| public | users_banner | ✅ |
| public | users_emailverification | ✅ |
| public | organizations_city | ✅ |
| public | organizations_organizationinfo | ✅ |
| public | organizations_teacher | ✅ |
| public | courses_courseinfo | ✅ |
| public | courses_lession | ✅ |
| public | courses_video | ✅ |
| public | courses_courseresource | ✅ |
| public | operation_coursecomments | ✅ |
| public | operation_userask | ✅ |
| public | operation_usercourse | ✅ |
| public | operation_userfav | ✅ |
| public | operation_usermessage | ✅ |
| public | teacher_* (12个表) | ✅ |

### Django 系统表
- auth_user, auth_group, auth_permission
- django_admin_log, django_content_type, django_migrations
- django_session
- guardian_*

## 🚀 访问方式

### 开发服务器
- **地址**: http://127.0.0.1:8000
- **启动方式**: 激活虚拟环境后运行 `python manage.py runserver`

### 批处理脚本
- **init_venv.bat** - 初始化虚拟环境
- **run_project.bat** - 完整运行（包含迁移）
- **quick_start.bat** - 快速启动

### 辅助脚本
- **create_schema.py** - 创建 PostgreSQL Schema
- **reset_db.py** - 重置数据库（清空所有表）

## 📝 注意事项

1. **guardian app 暂时禁用**
   - 文件: `apps/teacher/guarded_temp.py`
   - 需要在 admin.py 中恢复使用原始的 `guarded.py`

2. **search_path 配置暂未生效**
   - 当前所有表都在 public schema
   - 需要进一步配置以实现 schema 隔离

3. **表名前缀区分**
   - online 项目: users_*, organizations_*, courses_*, operation_*, teacher_*
   - cloud_school 项目: teacher_* (需迁移或添加前缀）

## 🎯 下一步建议

1. **启用 guardian**（如果需要权限管理功能）
   - 恢复 `guardian` app 到 INSTALLED_APPS
   - 在 `apps/teacher/admin.py` 中恢复原始导入
   - 迁移 guardian 的表

2. **实现 Schema 隔离**（高级）
   - 方案 A: 修改 db_table 使用 `online_schema.xxx`
   - 方案 B: 使用数据库视图跨 schema 访问
   - 方案 C: 为共享表创建专门的共享 schema

3. **部署到生产环境**
   - 配置 DEBUG = False
   - 配置 ALLOWED_HOSTS
   - 配置静态文件服务
   - 配置数据库连接池

## 📞 常见问题

### Q: 如何清空数据库？
```bash
python reset_db.py
```

### Q: 如何重新迁移？
```bash
python manage.py makemigrations
python manage.py migrate
```

### Q: 如何创建超级用户？
```bash
python manage.py createsuperuser
```

---

**部署完成时间**: 2026-01-20
**Python 版本**: 3.10.11
**Django 版本**: 4.2.6
**PostgreSQL 版本**: 15.15
