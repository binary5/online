# 线上学校 - 部署指南

## 环境要求

- Python 3.10+
- PostgreSQL 17+
- Nginx 1.25.3

## 项目结构

```
E:\NetSiteWorkspace\
├── start.bat              # 一键启动（开发环境）
├── start_prod.bat         # 一键启动（生产环境）
├── stop.bat               # 一键停止所有服务
├── nginx-1.25.3/          # Nginx 服务器
│   └── conf/nginx.conf    # Nginx 配置
└── online/                # Django 项目
    ├── run.py             # Uvicorn 启动脚本
    ├── venv/              # Python 虚拟环境
    └── online/settings/   # 环境配置
        ├── base.py        # 通用配置
        ├── development.py # 开发环境
        └── production.py  # 生产环境
```

## 快速启动

### 开发环境

双击运行 `start.bat` 或在终端执行：
```bash
start.bat
```

### 生产环境

双击运行 `start_prod.bat` 或执行：
```bash
start_prod.bat
```

### 停止服务

```bash
stop.bat
```

## 手动启动（可选）

如果一键脚本有问题，可以手动启动：

**终端 1 - Uvicorn（Django 应用）：**
```bash
cd E:\NetSiteWorkspace\online
venv\Scripts\python.exe run.py
```

**终端 2 - Nginx（反向代理）：**
```bash
cd E:\NetSiteWorkspace\nginx-1.25.3
nginx.exe
```

## 架构说明

```
用户请求 (80) → Nginx → Uvicorn (8000) → Django 应用
                           ↓
                    静态文件直接响应
```

| 组件 | 端口 | 作用 |
|------|------|------|
| Nginx | 80 | 反向代理、静态文件服务 |
| Uvicorn | 8000 | Django ASGI 应用服务器 |

## 访问地址

| 环境 | 地址 |
|------|------|
| 网站首页 | http://localhost/ |
| 管理后台 | http://localhost/admin/ |

## 环境配置

### 开发环境 (development.py)
- DEBUG = True
- 使用开发数据库配置

### 生产环境 (production.py)
- DEBUG = False
- ALLOWED_HOSTS = ['*']
- 数据库: cloudschool_db (PostgreSQL 17)
- 用户: postgres
- 密码: hy010112
- 主机: 127.0.0.1:5432

### 切换环境

通过环境变量 `DJANGO_ENVIRONMENT` 切换：
```bash
set DJANGO_ENVIRONMENT=development  # 开发
set DJANGO_ENVIRONMENT=production   # 生产
```

## 常见问题

### 1. 502 Bad Gateway
- 检查 Uvicorn 是否在运行：`netstat -ano | findstr :8000`
- 检查 Nginx 是否在运行：`netstat -ano | findstr :80`
- 重新运行 `stop.bat` 然后 `start.bat`

### 2. 端口被占用
```bash
# 停止占用端口的进程
taskkill /F /IM python.exe /IM nginx.exe
```

### 3. Gunicorn 无法在 Windows 运行
Windows 不支持 Gunicorn，请使用 Uvicorn。

## 技术栈

| 组件 | 版本 | 用途 |
|------|------|------|
| Django | 4.2.6 | Web 框架 |
| uvicorn | 0.40.0 | ASGI 服务器 |
| nginx | 1.25.3 | 反向代理 |
| PostgreSQL | 15 | 数据库 |
| whitenoise | 6.11.0 | 静态文件服务 |
| django-pure-pagination | 0.3.0 | 分页 |
| django-simple-captcha | 0.6.3 | 验证码 |

## 静态文件和媒体文件

| 类型 | 目录 | 说明 |
|------|------|------|
| 静态文件 | `online/static/` | CSS、JS、图片等 |
| 媒体文件 | `online/media/` | 用户上传的文件 |

## 许可证

本项目仅供学习使用。
