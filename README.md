# 线上学校

该平台的课程由各授课机构提供，授课机构中的各授课老师将录制的视频上传至平台，由平台进行呈现，学员通过平台进行在线学习。

## 主要功能

- 账号注册、激活、登录、密码找回等功能
- 个人中心页面支持`个人信息`、`我的课程`、`我的收藏`、`我的消息`管理
- 首页轮播图、机构、课程展示
- 支持讲师、课程、机构选项的全局搜索
- 侧边栏提供热门课程推荐、机构/讲师排名、课程咨询
- 支持授课机构按类别、按地区筛选，按学习人数、课程数排序

## 技术栈

| 组件 | 版本 |
|------|------|
| Python | 3.10+ |
| Django | 4.2.6 |
| PostgreSQL | 15 |
| uvicorn | 0.40.0 |
| Nginx | 1.25.3 |

## 快速启动

### 1. 创建虚拟环境

```bash
cd E:\NetSiteWorkspace\online
python -m venv venv
venv\Scripts\activate
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置数据库

确保 PostgreSQL 数据库 `cloudschool_db` 已创建。

### 4. 运行服务

**一键启动（推荐）：**
```bash
# 开发环境
start.bat

# 或生产环境
start_prod.bat
```

**或手动启动：**
```bash
# 终端 1 - Uvicorn
cd E:\NetSiteWorkspace\online
venv\Scripts\python.exe run.py

# 终端 2 - Nginx
cd E:\NetSiteWorkspace\nginx-1.25.3
nginx.exe
```

### 5. 访问地址

| 地址 | 说明 |
|------|------|
| http://localhost/ | 网站首页 |
| http://localhost/admin/ | 管理后台 |

## 停止服务

```bash
stop.bat
```

## 架构说明

```
用户请求 (80) → Nginx → Uvicorn (8000) → Django 应用
                           ↓
                    静态文件直接响应
```

## 环境配置

项目支持多环境配置，配置文件位于 `online/settings/` 目录：

| 文件 | 说明 |
|------|------|
| `base.py` | 通用配置 |
| `development.py` | 开发环境（DEBUG=True） |
| `production.py` | 生产环境（DEBUG=False） |

切换环境通过环境变量 `DJANGO_ENVIRONMENT` 控制，默认为 `development`。

## 项目结构

```
online/
├── apps/              # Django 应用
│   ├── users/         # 用户模块
│   ├── courses/       # 课程模块
│   ├── organizations/ # 机构模块
│   ├── operation/     # 操作模块
│   └── teacher/       # 教师模块
├── online/            # 项目配置
│   ├── settings/      # 环境配置
│   ├── urls.py        # URL 路由
│   └── wsgi.py        # WSGI 配置
├── templates/         # HTML 模板
├── static/            # 静态文件
├── media/             # 媒体文件
├── extra_apps/        # 第三方应用
├── run.py             # Uvicorn 启动脚本
├── manage.py          # Django 管理脚本
└── requirements.txt   # 依赖列表
```

## 常见问题

### 502 Bad Gateway
- 确保 Uvicorn 和 Nginx 都在运行
- 运行 `stop.bat` 然后 `start.bat`

### 端口被占用
```bash
taskkill /F /IM python.exe /IM nginx.exe
```

### Gunicorn 无法运行
Windows 不支持 Gunicorn，请使用项目配置的 Uvicorn。

## 许可证

本项目仅供学习使用。
