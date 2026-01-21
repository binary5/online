# Online 项目开发环境设置

## 快速开始

### 第一次使用

1. **初始化虚拟环境并安装依赖**
   ```bash
   init_venv.bat
   ```
   这将：
   - 创建 Python 虚拟环境
   - 安装所有依赖包
   - 创建 PostgreSQL Schema

2. **运行项目**
   ```bash
   run_project.bat
   ```
   这将：
   - 激活虚拟环境
   - 执行数据库迁移
   - 启动开发服务器

### 日常开发

**快速启动**（跳过数据库迁移）：
```bash
quick_start.bat
```

**完整启动**（包含数据库迁移）：
```bash
run_project.bat
```

## 环境信息

- **Python 版本**: 3.10.11
- **Django 版本**: 4.2.6
- **数据库**: PostgreSQL 15
- **数据库名**: cloudschool_db
- **Schema**: online_schema

## 手动操作

### 激活虚拟环境
```bash
venv\Scripts\activate.bat
```

### 安装新依赖
```bash
pip install package_name
```

### 更新 requirements.txt
```bash
pip freeze > requirements.txt
```

### 数据库操作
```bash
# 创建迁移文件
python manage.py makemigrations

# 应用迁移
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser
```

## 项目配置

### 数据库配置
- 配置文件: `online/settings.py`
- 数据库: PostgreSQL 15
- Schema: online_schema

### 应用列表
- courses - 课程管理
- operation - 用户操作（评论、收藏、消息等）
- organizations - 机构管理
- teacher - 教师信息管理
- users - 用户管理

## 常见问题

### 虚拟环境未激活
确保先执行: `venv\Scripts\activate.bat`

### 数据库连接失败
检查 PostgreSQL 服务是否启动，密码是否正确（hy010112）

### 端口被占用
修改端口: `python manage.py runserver 8001`

## 访问地址
- 开发服务器: http://127.0.0.1:8000
- 管理后台: http://127.0.0.1:8000/admin
