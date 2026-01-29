# 线上学校 - 在线学习平台

## 项目简介

在线学习平台，提供课程展示、机构介绍、教师管理等功能。

## 技术栈

| 组件 | 版本 |
|------|------|
| Python | 3.10+ |
| Django | 4.2.6 |
| PostgreSQL | 17 |
| Uvicorn | 0.40.0 |
| Nginx | 1.25.3 |

## 快速开始

### 方式1：使用 S:/SiteWorkspace 脚本（推荐）

```bash
# 开发环境
S:\SiteWorkspace\start.bat

# 生产环境
S:\SiteWorkspace\start_prod.bat
```

### 方式2：直接使用 Django 命令（跨平台）

```bash
# 进入 online 目录
cd S:\SiteWorkspace\online

# 激活 conda 环境
conda activate online_env

# 首次使用：数据库迁移
python manage.py migrate

# 启动开发服务器
python manage.py runserver

# 或使用 Uvicorn (推荐)
python run.py
```

## 停止服务

```bash
S:\SiteWorkspace\stop.bat
```

## 访问地址

| 页面 | 开发环境 | 生产环境 |
|------|---------|---------|
| 网站首页 | http://127.0.0.1:8000/ | http://192.168.31.6/ |
| 管理后台 | http://127.0.0.1:8000/admin/ | http://192.168.31.6/admin/ |

## 管理员账号

| 用户名 | 密码 | 邮箱 |
|--------|-------|-------|
| root | hy010112 | admin@example.com |

## 项目结构

```
online/
├── apps/              # Django 应用
│   ├── users/         # 用户管理
│   ├── organizations/ # 机构管理
│   ├── courses/       # 课程管理
│   ├── operation/     # 运营管理
│   └── teacher/       # 教师管理
├── online/            # 项目配置
│   ├── settings/      # 环境配置
│   ├── urls.py       # URL 路由
│   └── asgi.py      # ASGI 配置
├── templates/         # 模板文件
├── media/            # 媒体文件
├── logs/             # 日志文件
├── extra_apps/       # 第三方应用
├── run.py           # Uvicorn 启动脚本
├── manage.py        # Django 管理脚本
└── requirements.txt # 依赖列表
```

## 常用命令

### 数据库操作
```bash
python manage.py makemigrations  # 创建迁移
python manage.py migrate         # 应用迁移
python manage.py createsuperuser # 创建管理员
```

### 收集静态文件
```bash
python manage.py collectstatic --noinput
```

## 环境配置

| 环境 | DEBUG | 日志文件 | 日志级别 |
|------|-------|----------|----------|
| 开发 | True | development.log | DEBUG |
| 生产 | False | production.log | INFO |

切换环境通过环境变量 `DJANGO_ENVIRONMENT` 控制。

## 常见问题

### 1. 502 Bad Gateway
确保 Uvicorn 和 Nginx 都在运行：
```bash
# 停止并重启
S:\SiteWorkspace\stop.bat
S:\SiteWorkspace\start_prod.bat
```

### 2. 端口被占用
```bash
# 停止占用端口的进程
taskkill /F /IM python.exe /IM nginx.exe
```

### 3. 数据库连接失败
检查 PostgreSQL 服务是否启动，密码是否正确（hy010112）。

### 4. 管理员登录失败
清除浏览器缓存后重试，或重新创建管理员：
```bash
python manage.py createsuperuser
```

## 详细文档

更多配置信息请查看：`S:\SiteWorkspace\PROJECT_GUIDE.md`

## 许可证

本项目仅供学习使用。
