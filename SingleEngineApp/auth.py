from flask import Blueprint, request, redirect, url_for, session

# 认证模块 - 负责用户登录、登出功能（软著申报备注）
auth_bp = Blueprint('auth', __name__)

# 模拟用户数据库（实际项目中建议替换为MySQL/PostgreSQL等持久化存储）
users = {
    "admin": "admin123",
    "user1": "user123"
}

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    登录接口：
    - GET请求：返回登录页面
    - POST请求：验证用户名密码，验证通过则创建会话并跳转首页
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # 用户名密码验证逻辑
        if username in users and users[username] == password:
            session['username'] = username  # 记录登录状态
            return redirect(url_for('index'))  # 登录成功跳首页
        else:
            return "用户名或密码错误，请重试！"

    template_path = "D:/git/bettafish/BettaFish/templates/login.html"
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        return template_content
    except FileNotFoundError:
        return f"模板文件不存在！请检查路径：{template_path}"

@auth_bp.route('/logout')
def logout():
    """登出接口：清除登录会话，返回登录页"""
    session.pop('username', None)
    return redirect(url_for('auth.login'))

