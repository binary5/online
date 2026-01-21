import psycopg2

print("=" * 60)
print("转换 auth_user 到 users_userprofile")
print("=" * 60)

conn = psycopg2.connect("host=127.0.0.1 port=5432 dbname=cloudschool_db user=postgres password=hy010112")
cur = conn.cursor()

print("\n1. 创建 users_userprofile 表...")
cur.execute("""
    CREATE TABLE IF NOT EXISTS users_userprofile (
        id INTEGER PRIMARY KEY,
        password VARCHAR(128) NOT NULL,
        last_login TIMESTAMP WITH TIME ZONE,
        is_superuser BOOLEAN NOT NULL,
        username VARCHAR(150) NOT NULL UNIQUE,
        first_name VARCHAR(150) NOT NULL DEFAULT '',
        last_name VARCHAR(150) NOT NULL DEFAULT '',
        email VARCHAR(254) NOT NULL DEFAULT '',
        is_staff BOOLEAN NOT NULL DEFAULT FALSE,
        is_active BOOLEAN NOT NULL DEFAULT TRUE,
        date_joined TIMESTAMP WITH TIME ZONE NOT NULL,
        nick_name VARCHAR(50) DEFAULT '',
        birthday DATE,
        gender VARCHAR(10) DEFAULT 'male',
        address VARCHAR(255) DEFAULT '',
        mobile VARCHAR(20),
        image VARCHAR(100),
        add_time TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    )
""")
conn.commit()

print("\n2. 转换用户数据...")
cur.execute("""
    INSERT INTO users_userprofile (
        id, password, last_login, is_superuser, username,
        first_name, last_name, email, is_staff, is_active, date_joined,
        nick_name, birthday, gender, address, mobile, image, add_time
    )
    SELECT 
        id, password, last_login, is_superuser, username,
        first_name, last_name, email, is_staff, is_active, date_joined,
        '', NULL, 'male', '', NULL, NULL, NOW()
    FROM auth_user
    ON CONFLICT (id) DO NOTHING
""")
conn.commit()
print(f"   转换完成")

print("\n3. 验证数据...")
cur.execute("SELECT COUNT(*) FROM auth_user")
auth_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM users_userprofile")
user_count = cur.fetchone()[0]
print(f"   auth_user: {auth_count} 条")
print(f"   users_userprofile: {user_count} 条")

print("\n4. 设置管理员...")
cur.execute("UPDATE users_userprofile SET is_staff=TRUE, is_superuser=TRUE WHERE username='root'")
conn.commit()
print("   用户root已设为超级管理员")

cur.close()
conn.close()

print("\n" + "=" * 60)
print("✅ 用户数据转换完成！")
print("=" * 60)
