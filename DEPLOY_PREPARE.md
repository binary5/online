# 线上学校 - 生产环境部署准备指南

将项目迁移到全新服务器作为正式环境，需要完成以下准备工作。本指南涵盖从系统环境搭建到服务启动验证的完整流程。

## 一、服务器要求

### 1.1 操作系统要求

生产环境建议使用以下操作系统之一。Windows Server 2019 或 2022 提供了更好的稳定性和企业级支持，而 Windows 10/11 专业版或企业版也完全能够满足中小型项目的需求。无论选择哪个版本，均需确保系统为 64 位架构，以支持 PostgreSQL 和 Nginx 的正常运行。服务器的硬盘空间建议不低于 50GB，其中系统盘占用约 20GB，数据盘用于存放项目代码、数据库和媒体文件，建议预留 30GB 以上。内存方面，基础配置建议 4GB RAM，如果预期并发用户量较大或需要运行其他服务，8GB 或更多会是更安全的选择。

### 1.2 网络要求

服务器需要具备固定的公网 IP 地址，以便外部用户能够访问系统。如果部署在云服务器上，需要在安全组或防火墙中开放 80 端口（HTTP）和 443 端口（HTTPS，可选）。同时建议开放 22 端口用于 SSH 远程管理（如果使用 Linux 子系统或远程桌面方案）。内网环境中需要确保服务器与数据库服务器之间的网络连通性，如果数据库独立部署，则需额外开放 PostgreSQL 的 5432 端口。域名解析方面，如果需要使用域名访问，需要提前完成域名的 DNS 解析配置，将域名指向服务器的公网 IP 地址。

## 二、软件环境安装

### 2.1 Python 3.10+ 环境安装

首先需要从 Python 官方网站下载 Python 3.10 或更高版本的安装包。访问 https://www.python.org/downloads/ 下载 Python 3.11.x 或 3.12.x 的 Windows 安装程序。运行安装程序时，务必勾选 "Add Python to PATH" 选项，这一步至关重要，否则后续命令将无法正常执行。建议选择 "Customize installation" 方式，在高级选项中勾选 "pip" 和 "py launcher"，同时建议勾选 "Create shortcuts for installed applications" 方便后续操作。安装完成后，打开命令提示符验证安装结果，输入 "python --version" 应显示版本号信息，输入 "pip --version" 应显示 pip 版本和 Python 路径。如果安装过程中出现问题，可以尝试重启命令行窗口或系统以确保环境变量生效。

### 2.2 PostgreSQL 17 数据库安装

PostgreSQL 是本项目使用的数据库系统。生产环境已安装 PostgreSQL 17，数据目录位于 `S:\PostgreSQL\DATABASE`，服务名称为 `postgresql-x64-17`。

### 2.3 Nginx 1.25.3 Web 服务器安装

从 Nginx 官方网站 http://nginx.org/en/download.html 下载 Nginx 1.25.3 的稳定版本（nginx/Windows-1.25.3）。下载后直接将压缩包解压到目标目录即可使用，建议解压到 E 盘根目录并重命名为 nginx-1.25.3 以便于管理。Nginx 的主配置文件位于 conf/nginx.conf，后续章节会详细介绍其配置方法。验证 Nginx 是否正常安装的方法是打开命令行，进入 nginx-1.25.3 目录并执行 "nginx.exe"，然后在浏览器中访问 http://localhost，如果显示 "Welcome to nginx!" 页面则表示安装成功。停止 Nginx 的方法是执行 "nginx.exe -s stop" 或在任务管理器中结束 nginx.exe 进程。建议将 nginx-1.25.3 目录添加到系统 PATH 环境变量中，以便在任何位置都能方便地执行 nginx 命令。

## 三、项目文件迁移

### 3.1 需要迁移的文件清单

将项目从开发环境迁移到生产环境时，需要传输以下文件目录结构。核心项目代码位于 online 目录中，该目录包含了整个 Django 应用的源代码、模板文件、静态资源和 Python 虚拟环境。Web 服务器配置位于 nginx-1.25.3 目录，其中 conf/nginx.conf 是核心配置文件，需要根据生产环境进行相应修改。数据库备份文件位于 db_export 目录中，如果需要在目标服务器上恢复完整数据，需要携带 cloudschool_db.dump 或 cloudschool_db_test.dump 文件。启动脚本包括 start.bat、start_prod.bat 和 stop.bat，这些批处理文件实现了开发环境和生产环境的一键启动停止功能。此外，如果项目中有自定义的配置文档如 DEPLOY.md、README.md 等，也应当一并迁移以便于后续维护。

### 3.2 文件传输方式

根据服务器的可访问性，可以选择不同的文件传输方式。如果目标服务器可以通过局域网访问，可以使用 SMB 文件共享，将开发环境的 E:\NetSiteWorkspace 目录共享后，在目标服务器上通过映射网络驱动器的方式直接访问和复制文件。如果目标服务器是远程云服务器，建议使用 SCP 或 SFTP 协议进行文件传输，可以使用 WinSCP、FileZilla 等图形化工具，或使用 PowerShell 的 Copy-Item 命令配合远程管理功能。对于大型项目的传输，建议先使用压缩工具（如 7-Zip）将整个项目目录打包压缩后再进行传输，可以显著减少传输时间和带宽占用。传输完成后，在目标服务器上解压到相应目录，如 E:\NetSiteWorkspace，确保目录结构与开发环境保持一致。

### 3.3 目录结构验证

文件传输完成后，需要验证目标服务器的目录结构是否完整正确。以下是生产环境部署所需的完整目录结构，应当确保每个目录和文件都正确放置：

```
E:\
├── NetSiteWorkspace\
│   ├── db_export\                 # 数据库备份目录
│   │   ├── cloudschool_db.dump
│   │   └── cloudschool_db_test.dump
│   ├── nginx-1.25.3\              # Nginx 服务器目录
│   │   ├── conf\
│   │   │   └── nginx.conf         # Nginx 配置文件（需修改）
│   │   ├── logs\                  # 日志目录
│   │   ├── html\
│   │   └── nginx.exe
│   ├── online\                    # Django 项目主目录
│   │   ├── apps\                  # 应用模块
│   │   │   ├── courses\
│   │   │   ├── operation\
│   │   │   ├── organizations\
│   │   │   ├── teacher\
│   │   │   ├── users\
│   │   │   └── utils\
│   │   ├── extra_apps\            # 第三方应用
│   │   │   └── xadmin\
│   │   ├── online\                # 项目配置目录
│   │   │   ├── settings\         # 配置文件目录
│   │   │   │   ├── base.py       # 基础配置
│   │   │   │   ├── development.py
│   │   │   │   └── production.py # 生产配置（需修改）
│   │   │   ├── urls.py
│   │   │   └── asgi.py
│   │   ├── static\                # 静态文件目录
│   │   ├── media\                 # 媒体文件目录
│   │   ├── templates\             # 模板文件目录
│   │   ├── venv\                  # Python 虚拟环境
│   │   │   └── Scripts\
│   │   ├── run.py                 # Uvicorn 启动脚本
│   │   ├── manage.py
│   │   └── requirements.txt
│   ├── start.bat                  # 开发环境启动脚本
│   ├── start_prod.bat             # 生产环境启动脚本
│   └── stop.bat                   # 停止服务脚本
```

## 四、Python 虚拟环境配置

### 4.1 创建虚拟环境

如果目标服务器上没有现成的虚拟环境，需要手动创建。首先打开命令提示符，进入项目目录 E:\NetSiteWorkspace\online，然后执行以下命令创建虚拟环境。Python 内置的 venv 模块可以创建一个隔离的 Python 环境，避免与系统全局的 Python 包产生冲突。创建完成后，会在当前目录下生成一个 venv 目录，其中包含了独立的 Python 解释器和 pip 工具。创建虚拟环境的命令是 "python -m venv venv"，其中第一个 venv 是模块名，第二个 venv 是目录名。创建完成后，可以使用 "venv\Scripts\activate.bat" 命令激活虚拟环境，激活后命令行提示符前缀会显示 "(venv)" 表示当前处于虚拟环境中。激活后安装的所有 Python 包都会安装到虚拟环境目录中，不会影响系统全局环境。

### 4.2 安装项目依赖

虚拟环境激活后，需要安装项目运行所需的 Python 包。项目依赖列表定义在 requirements.txt 文件中，其中包含了 Django、uvicorn、Pillow、psycopg2-binary 等所有必要的依赖包。安装命令为 "pip install -r requirements.txt"，pip 会自动读取文件中的所有包名并依次安装。安装过程中可能会遇到某些包编译失败的情况，通常是因为缺少系统级依赖。psycopg2-binary 在安装时需要 PostgreSQL 开发库，如果安装失败可以尝试安装预编译版本或单独下载 wheel 文件安装。Pillow 图像处理库可能需要 Microsoft C++ Build Tools，如果遇到编译错误，可以从 https://www.lfd.uci.edu/~gohlke/pythonlibs/ 下载对应的 wheel 文件进行手动安装。安装完成后，可以使用 "pip list" 命令查看已安装的所有包及其版本，确认 Django、uvicorn 等核心依赖是否正确安装。

### 4.3 验证虚拟环境

依赖安装完成后，需要验证虚拟环境是否配置正确。首先激活虚拟环境，然后依次执行以下命令进行验证。执行 "python manage.py --version" 应该显示 Django 版本号 4.2.6。执行 "python run.py" 应该能够正常启动 Uvicorn 服务，虽然这会占用命令行但可以用来测试应用是否能加载。执行 "python -c "import django; django.setup()"" 应该没有任何输出，表示 Django 能够正常初始化。如果出现模块导入错误，需要检查对应的包是否正确安装。也可以进入 Python 交互模式，尝试导入项目中的模块，如 from online.settings import BASE_DIR，如果能够正常导入则表示项目结构没有问题。虚拟环境配置完成后，建议执行一次完整的数据库迁移以确保应用能够在新的服务器环境中正常运行。

## 五、数据库配置

### 5.1 创建数据库和用户

在目标服务器的 PostgreSQL 中创建项目所需的数据库和用户。首先使用 pgAdmin 或 psql 命令行工具连接到 PostgreSQL 服务器。如果使用 psql，打开命令提示符执行 "psql -U postgres -h localhost" 然后输入 postgres 用户的密码。连接成功后，执行以下 SQL 语句创建数据库用户（请将 'your_strong_password' 替换为实际使用的密码）：

```sql
CREATE USER schooluser WITH PASSWORD 'your_strong_password';
CREATE DATABASE cloudschool_db OWNER schooluser;
GRANT ALL PRIVILEGES ON DATABASE cloudschool_db TO schooluser;
```

创建完成后，可以使用 "\q" 命令退出 psql，然后使用新用户验证连接："psql -U schooluser -d cloudschool_db -h localhost"。如果能够成功连接，说明数据库和用户创建成功。建议在 pgAdmin 中检查数据库的属性设置，确保编码为 UTF-8，这是确保中文数据能够正确存储的必要条件。

### 5.2 恢复数据库数据

如果需要将原服务器上的数据迁移到新服务器，需要使用 pg_dump 导出的备份文件进行恢复。首先确认目标服务器上的 cloudschool_db 数据库已经创建，并且是空数据库。然后使用 psql 命令或 pgAdmin 的恢复功能导入数据。使用命令行恢复的语法是 "psql -U schooluser -d cloudschool_db -h localhost -f E:\NetSiteWorkspace\db_export\cloudschool_db.dump"。如果备份文件较大，恢复过程可能需要几分钟时间，期间请耐心等待直到命令执行完成。恢复完成后，可以使用 "\dt" 命令查看数据库中的所有表，确认数据是否成功导入。也可以在 pgAdmin 中右键点击 cloudschool_db 数据库，选择 "刷新"，然后展开 "schemas" -> "public" -> "Tables" 查看所有数据表。如果在恢复过程中出现权限错误，需要确保 schooluser 用户是数据库的所有者，并且有足够的权限操作所有表。

### 5.3 执行数据库迁移

如果目标数据库中还没有创建表结构，需要执行 Django 的数据库迁移命令。首先激活虚拟环境，进入项目目录，然后依次执行以下命令。执行 "python manage.py makemigrations" 会检查模型的变更并生成迁移文件。执行 "python manage.py migrate" 会将迁移文件应用到数据库，创建所有必要的表结构。如果迁移过程中出现错误，可能是由于数据库中已存在部分表或迁移历史记录与当前代码不同步。可以尝试使用 "python manage.py migrate --fake" 将迁移记录标记为已应用而不实际执行 SQL，或者使用 "python manage.py migrate --fake-initial" 处理初始迁移。如果问题仍然存在，可能需要重置数据库或手动清理有问题的迁移记录后再重新执行迁移。

## 六、生产环境配置修改

### 6.1 修改数据库连接配置

生产环境的数据库连接信息需要根据实际服务器配置进行修改。编辑 online/settings/production.py 文件，找到 DATABASES 配置部分，确保 HOST、PORT、NAME、USER、PASSWORD 等参数与目标服务器的实际配置一致。以下是生产环境数据库配置的标准模板：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'cloudschool_db',
        'USER': 'schooluser',
        'PASSWORD': 'your_actual_password_here',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'OPTIONS': {
            'options': '-c search_path=public'
        }
    }
}
```

如果数据库部署在独立的服务器上，需要将 HOST 修改为数据库服务器的 IP 地址或主机名。同时需要在数据库服务器上配置 pg_hba.conf 文件，允许应用服务器连接到数据库。如果使用云数据库服务，还需要将应用服务器的 IP 添加到数据库的白名单安全组中。

### 6.2 修改安全相关配置

生产环境的 Django 安全配置需要更加严格。编辑 online/settings/production.py 文件，检查并修改以下配置项。首先确保 DEBUG 设置为 False，这将禁用调试模式，防止敏感信息泄露。ALLOWED_HOSTS 需要配置为允许访问的域名或 IP 地址列表，建议只添加实际使用的域名：

```python
DEBUG = False

ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com', 'server-ip']
```

SECRET_KEY 应当使用一个足够长且随机的字符串，不要使用开发环境中的默认密钥。可以使用 Django 自带的密钥生成命令 "python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'" 生成新的密钥。生产环境中还应该启用 HTTPS 支持，如果使用 Nginx 配置 SSL 证书，需要在 settings 中设置 SECURE_PROXY_SSL_HEADER 配置。此外，建议设置 SESSION_COOKIE_SECURE 和 CSRF_COOKIE_SECURE 为 True，确保会话和 CSRF 令牌通过安全连接传输。

### 6.3 配置 Nginx 反向代理

生产环境的 Nginx 配置需要根据实际情况进行调整。编辑 nginx-1.25.3/conf/nginx.conf 文件，确保 upstream 块中的服务器地址指向正确的 Uvicorn 服务地址，server 块中配置正确的域名和 SSL（如已配置）。以下是生产环境 Nginx 配置的关键部分：

```nginx
upstream django {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    
    # HTTP 到 HTTPS 重定向（如果已配置 SSL）
    return 301 https://$server_name$request_uri;
}

# HTTPS server 配置块（需要单独添加）
server {
    listen 443 ssl;
    server_name your-domain.com www.your-domain.com;
    
    ssl_certificate path/to/your/certificate.crt;
    ssl_certificate_key path/to/your/private.key;
    ssl_session_timeout 5m;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:HIGH:!aNULL:!MD5;
    
    location /static/ {
        alias E:/NetSiteWorkspace/online/static/;
        expires 30d;
    }
    
    location /media/ {
        alias E:/NetSiteWorkspace/online/media/;
        expires 30d;
    }
    
    location / {
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

如果使用云服务器并通过负载均衡器或 CDN 访问，还需要添加相应的 X-Forwarded-* 头配置。配置修改完成后，使用 "nginx.exe -t" 命令测试配置文件语法是否正确。

### 6.4 配置静态文件和媒体文件

生产环境中，静态文件和媒体文件应当由 Nginx 直接提供服务，而不是通过 Django 应用。首先确保 online/settings/production.py 中的静态文件配置正确：

```python
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

执行 "python manage.py collectstatic" 命令将所有应用中的静态文件收集到 STATIC_ROOT 目录。Nginx 配置中的 alias 路径必须与 MEDIA_ROOT 和 STATIC_ROOT 的实际路径一致。确保 Nginx 进程对 static 和 media 目录有读取权限，如果权限不足可能会导致静态文件无法加载。可以通过浏览器直接访问静态文件的 URL 来验证配置是否正确，例如访问 http://your-domain.com/static/admin/css/base.css 应能正常显示样式文件。

## 七、服务启动与验证

### 7.1 启动服务

生产环境的服务启动推荐使用 start_prod.bat 脚本，该脚本会按顺序启动 Uvicorn 应用服务器和 Nginx 反向代理。如果需要手动启动，可以按照以下步骤操作。首先打开一个命令行窗口，激活虚拟环境后进入项目目录，执行 "set DJANGO_ENVIRONMENT=production" 设置环境变量，然后执行 "venv\Scripts\python.exe run.py" 启动 Uvicorn。Uvicorn 启动后会在后台监听 8000 端口，可以通过查看控制台输出来确认应用是否正常启动。启动成功后，打开另一个命令行窗口，进入 Nginx 目录执行 "nginx.exe" 启动 Nginx 服务。Nginx 启动后会在前台运行（不会自动退出），可以通过访问 http://localhost 来验证 Nginx 是否正常工作。如果一切正常，访问 http://your-domain.com 应该能够看到网站首页。

### 7.2 验证部署结果

服务启动后需要进行全面的功能验证，确保所有组件都正常工作。依次访问以下地址确认各功能模块的可用性。访问 http://your-domain.com/ 验证网站首页是否正常显示，检查轮播图、机构展示、课程列表等页面元素是否正确加载。访问 http://your-domain.com/admin/ 验证管理后台是否正常，登录管理员账号后检查各数据表的增删改查功能是否正常。访问 http://your-domain.com/accounts/login/ 验证用户登录功能是否正常，测试注册、登录、密码找回等流程。检查静态文件是否正确加载，查看页面源代码确认 CSS、JavaScript、图片等静态资源的 URL 是否正确。如果使用 HTTPS，浏览器地址栏应显示安全连接标志。也可以使用浏览器开发者工具的网络标签页查看各资源的加载状态和响应时间。

### 7.3 常见启动问题排查

服务启动过程中可能会遇到各种问题，以下是常见问题的排查方法。如果访问网站返回 502 Bad Gateway 错误，首先检查 Uvicorn 是否正在运行，可以使用 "netstat -ano | findstr :8000" 命令查看 8000 端口是否有进程监听。然后检查 Nginx 错误日志，路径为 nginx-1.25.3/logs/error.log，日志中通常会包含详细的错误信息。如果 Uvicorn 启动失败，可能是 Python 环境配置问题或依赖包缺失，尝试在命令行中直接运行 Python 并导入项目模块来定位具体错误。如果 Nginx 无法启动，检查配置文件语法是否正确，使用 "nginx.exe -t" 命令进行测试。如果数据库连接失败，检查 settings/production.py 中的数据库配置是否正确，确认数据库服务正在运行且网络连通性正常。如果出现静态文件 404 错误，检查 Nginx 配置中的 alias 路径是否正确，确保 collectstatic 命令已经执行且目录权限正确。

## 八、系统服务化配置（可选）

### 8.1 使用 NSSM 创建系统服务

为了实现生产环境服务器的稳定运行，建议将 Uvicorn 和 Nginx 配置为系统服务，这样可以在服务器重启后自动启动服务。NSSM（Non-Sucking Service Manager）是一个轻量级的 Windows 服务管理工具，可以将任意应用程序包装为系统服务。首先从 https://nssm.cc/download 下载 NSSM，解压后将 nssm.exe 放到系统 PATH 目录或直接使用。配置 Uvicorn 为服务的命令如下：

```
nssm install OnlineSchoolUvicorn "E:\NetSiteWorkspace\online\venv\Scripts\python.exe"
nssm set OnlineSchoolUvicorn AppParameters "E:\NetSiteWorkspace\online\run.py"
nssm set OnlineSchoolUvicorn AppDirectory "E:\NetSiteWorkspace\online"
nssm set OnlineSchoolUvicorn DisplayName "线上学校 - Uvicorn 应用服务器"
nssm set OnlineSchoolUvicorn Description "线上学校 Django 应用的 ASGI 服务器"
nssm set OnlineSchoolUvicorn AppEnvironmentExtra DJANGO_ENVIRONMENT=production
nssm set OnlineSchoolUvicorn Start SERVICE_AUTO_START
```

配置完成后，使用 "nssm start OnlineSchoolUvicorn" 启动服务。Nginx 的服务配置方式类似，但需要注意 Nginx 不支持配置为服务时使用相对路径，必须使用绝对路径。

### 8.2 服务管理命令

配置为系统服务后，可以通过以下命令进行日常管理。查看服务状态："sc query OnlineSchoolUvicorn" 或 "nssm status OnlineSchoolUvicorn"。启动服务："sc start OnlineSchoolUvicorn" 或 "nssm start OnlineSchoolUvicorn"。停止服务："sc stop OnlineSchoolUvicorn" 或 "nssm stop OnlineSchoolUvicorn"。重启服务："sc stop OnlineSchoolUvicorn && sc start OnlineSchoolUvicorn"。删除服务："sc delete OnlineSchoolUvicorn" 或 "nssm remove OnlineSchoolUvicorn"。建议定期检查服务的运行状态和日志，确保系统稳定运行。Nginx 的日志位于 nginx-1.25.3/logs/ 目录下，Uvicorn 的日志可以在启动时重定向到文件或使用系统事件查看器查看。

## 九、数据备份策略

### 9.1 数据库备份

生产环境的数据安全至关重要，建议制定定期的数据库备份策略。可以创建批处理脚本实现自动备份，以下是一个每日凌晨 2 点执行数据库备份的示例脚本 backup_db.bat：

```batch
@echo off
set DATE_STR=%date:~0,4%%date:~5,2%%date:~8,2%
set TIME_STR=%time:~0,2%%time:~3,2%
set BACKUP_DIR=E:\NetSiteWorkspace\db_backup
set BACKUP_FILE=%BACKUP_DIR%\cloudschool_db_%DATE_STR%_%TIME_STR%.dump

mkdir %BACKUP_DIR% 2>nul
"E:\Program Files\PostgreSQL\15\bin\pg_dump.exe" -U schooluser -d cloudschool_db -h localhost > %BACKUP_FILE%

echo Backup completed: %BACKUP_FILE%
```

可以使用 Windows 任务计划程序配置定时执行此脚本。建议保留最近 7 天的每日备份和最近 4 周的每周备份，并定期将备份文件同步到异地存储以防止数据丢失。也可以考虑使用 PostgreSQL 的连续归档功能实现 Point-in-Time 恢复。

### 9.2 文件备份

除数据库外，项目代码、配置文件和用户上传的媒体文件也需要定期备份。可以使用 Windows 的文件历史记录功能或第三方备份工具实现。媒体文件目录（online/media）通常增长较快，建议单独配置备份策略，排除临时文件和缓存文件。以下是一个使用 robocopy 进行增量备份的示例脚本：

```batch
@echo off
set SOURCE_DIR=E:\NetSiteWorkspace\online\media
set BACKUP_DIR=\\backup-server\share\online-media
set LOG_FILE=E:\NetSiteWorkspace\logs\backup_media.log

mkdir E:\NetSiteWorkspace\logs 2>nul
robocopy %SOURCE_DIR% %BACKUP_DIR% /MIR /MT:16 /LOG:%LOG_FILE% /NP
```

建议每天至少执行一次媒体文件备份，并将备份数据传输到独立的存储设备或云存储服务中。

## 十、监控与日志

### 10.1 日志配置

生产环境应当配置适当的日志记录策略，以便于问题排查和运行分析。在 online/settings/production.py 中添加或修改以下日志配置：

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False,
        },
        'apps': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
```

确保项目目录下存在 logs 目录，否则日志文件无法创建。可以使用 Nginx 的 access.log 和 error.log 记录 HTTP 请求信息，这些日志对于分析访问模式和排查问题非常有用。

### 10.2 性能监控

建议部署基本的性能监控以便及时发现和处理问题。可以通过以下方式监控服务器状态。使用 Windows 任务管理器监控 CPU、内存、磁盘和网络使用情况。对于数据库性能，可以定期查询 PostgreSQL 的慢查询日志，分析执行时间较长的 SQL 语句。可以使用第三方监控工具如 Prometheus + Grafana 实现更完善的监控体系，设置告警规则在资源使用率过高或服务异常时及时通知运维人员。Uvicorn 提供了工作进程状态信息，可以通过配置 prometheus-client 来暴露指标数据供监控系统采集。Nginx 同样支持状态监控模块，可以配置 stub_status 来获取当前连接数等信息。

## 十一、部署检查清单

在完成生产环境部署后，使用以下检查清单确认所有配置正确无误：

| 检查项 | 状态 | 说明 |
|--------|------|------|
| Python 3.10+ 安装 | ☐ | 验证 python --version |
| PostgreSQL 15 安装 | ☐ | 验证数据库服务运行 |
| 数据库和用户创建 | ☐ | 验证连接和权限 |
| 数据库恢复/迁移 | ☐ | 验证数据完整性 |
| 虚拟环境创建 | ☐ | 验证 venv 目录 |
| 依赖包安装 | ☐ | pip list 检查 |
| settings/production.py 配置 | ☐ | 数据库、ALLOWED_HOSTS、DEBUG |
| Nginx 配置 | ☐ | nginx -t 测试通过 |
| 静态文件收集 | ☐ | collectstatic 执行 |
| SSL 证书配置（如使用） | ☐ | 证书路径和协议配置 |
| 服务启动测试 | ☐ | 访问首页和管理后台 |
| 功能验证 | ☐ | 登录、注册、数据操作 |
| 日志配置 | ☐ | 日志文件生成 |
| 备份脚本创建 | ☐ | 数据库和媒体文件备份 |
| 监控配置 | ☐ | 服务状态监控 |

完成所有检查项后，生产环境部署工作即告完成。建议在正式上线前进行一段时间的试运行，持续观察系统稳定性和性能表现，及时处理发现的问题。
