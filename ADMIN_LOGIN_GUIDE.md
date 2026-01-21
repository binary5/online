# Admin 登录问题排查指南

## ✅ 当前状态

### 已创建的超级用户
| 用户名 | 密码 | 邮箱 | 超级管理员 |
|--------|-------|-------|-------|-----------|
| root | hy010112 | admin@example.com | 是 |

### 数据库验证
```bash
python venv\Scripts\test_admin.py
```

输出应该显示：
```
[OK] root 用户存在
 - 用户名: root
 - 邮箱: admin@example.com
 - 超级管理员: True
 - 是否激活: True
 - 密码: 已设置
```

## 🔧 登录步骤

### 1. 访问 Admin 页面
在浏览器中打开：
```
http://127.0.0.1:8000/admin/
```

### 2. 输入凭据
- **用户名**: `root`
- **密码**: `hy010112`

### 3. 点击登录
点击"登录"按钮

## 🚨 如果无法登录

### 解决方案 1: 重启开发服务器

**方法 A: 使用批处理脚本**
```bash
# 双击运行
restart_server.bat
```

**方法 B: 手动重启**
```bash
# 1. 停止当前服务器（Ctrl+C）
# 2. 重新启动
python manage.py runserver
```

**方法 C: 强制重启**
```bash
# Windows
taskkill /F /IM python.exe
python manage.py runserver
```

### 解决方案 2: 清除浏览器缓存

**Chrome**:
1. 按 `Ctrl + Shift + Delete`
2. 清除以下数据：
   - 缓存的图片和文件
   - Cookie 和其他网站数据
3. 重启浏览器
4. 重试登录

**Firefox**:
1. 按 `Ctrl + Shift + Delete`
2. 清除"最近的历史"和"Cookies"
3. 重启浏览器
4. 重试登录

**Edge**:
1. 按 `Ctrl + Shift + Delete`
2. 清除"Cookie 和其他网站数据"
3. 重启浏览器
4. 重试登录

### 解决方案 3: 检查浏览器设置

1. 确认没有安装广告拦截器
2. 确认没有安装隐私插件阻止 Cookie
3. 尝试使用无痕/隐私模式
4. 尝试使用其他浏览器

### 解决方案 4: 使用不同的浏览器

如果当前浏览器问题，尝试：
- Chrome → Firefox
- Edge → Chrome
- 或使用无痕模式

### 解决方案 5: 重置密码（如果忘记）

```bash
python manage.py changepassword
```

或使用管理工具：
```bash
manage.bat
# 选择 [3] 创建超级用户
```

## 📊 管理工具说明

项目提供了完整的管理工具 `manage.bat`：

### 可用功能

**[1] 管理用户**
- 创建超级用户
- 修改密码
- 列出所有用户（需要安装 django-extensions）

**[2] 重启服务器**
- 停止当前 Python 进程
- 重新启动开发服务器

**[3] 创建超级用户**
- 快速创建新的管理员账户

**[4] 数据库操作**
- 重置数据库（清空所有表）
- 创建 PostgreSQL Schema
- 运行数据库迁移

**[5] 运行迁移**
- 创建迁移文件
- 应用数据库迁移

**[6] 测试 Admin**
- 验证用户是否存在
- 检查登录凭据

**[0] 退出**
- 退出管理工具

### 使用方法

```bash
# 运行管理工具
manage.bat

# 或直接运行单个命令
python manage.py [命令] [参数]
```

## 🔍 诊断检查清单

如果仍然无法登录，请检查以下内容：

### 服务器状态
- [ ] 服务器是否运行？
  - 检查: http://127.0.0.1:8000 是否能访问
- [ ] 端口 8000 是否被占用？
  - 运行: `netstat -ano | findstr :8000`

### 数据库状态
- [ ] PostgreSQL 是否运行？
  - 检查: `pg_isready -U postgres`
- [ ] 数据库连接是否正常？
  - 运行: `python venv\Scripts\test_admin.py`

### 用户验证
- [ ] root 用户是否存在？
  - 运行: `python manage.py shell` 然后 `User.objects.filter(username='root')`
- [ ] 密码是否正确？
  - 确认使用 `hy010112`

### Admin 配置
- [ ] admin 是否在 INSTALLED_APPS 中？
  - 检查 settings.py 第 40-50 行
- [ ] admin URL 是否正确？
  - 检查 online/urls.py 第 26 行

### 浏览器问题
- [ ] 是否使用了正确的 URL？
  - 确认是 http://127.0.0.1:8000/admin/
- [ ] 是否清除了缓存？
  - 清除浏览器 Cookie 和缓存
- [ ] 是否有网络问题？
  - 尝试访问其他网站

## 📞 获取帮助

如果以上方法都无法解决问题，请：

1. **检查日志**
   查看服务器终端输出的错误信息

2. **查看浏览器控制台**
   打开浏览器开发者工具（F12）查看错误

3. **提供详细信息**
   - 您使用的浏览器
   - 错误的具体提示
   - 您做的操作步骤

## 📞 快速修复命令

### 重新创建超级用户
```bash
# 删除旧用户
python manage.py shell

User.objects.filter(username='root').delete()

# 重新创建
python manage.py createsuperuser --username root --email admin@example.com --noinput
```

### 重置数据库（最后手段）
```bash
# 清空所有表
python venv\Scripts\reset_db.py

# 重新迁移
python manage.py makemigrations
python manage.py migrate

# 创建用户
python manage.py createsuperuser
```

## 📞 常见错误

### 错误 1: "请输入正确的用户名和密码"
- **原因**: 用户名或密码错误
- **解决**: 检查凭据，重试输入

### 错误 2: "此会话已过期"
- **原因**: Cookie 或 Session 过期
- **解决**: 清除浏览器缓存，重新登录

### 错误 3: "您的账户已被禁用"
- **原因**: 用户被设置为非激活状态
- **解决**: 运行 `python manage.py shell` 然后执行：
```python
user = User.objects.get(username='root')
user.is_active = True
user.save()
```

### 错误 4: "无权限访问"
- **原因**: 不是超级管理员或权限不足
- **解决**: 确保 `is_superuser=True`

---

**更新时间**: 2026-01-20
**Python 版本**: 3.10.11
**Django 版本**: 4.2.6
