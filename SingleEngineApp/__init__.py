from flask import Flask, session,render_template

def create_app():
    """应用工厂函数 - 初始化Flask应用，注册蓝图和核心配置"""
    app = Flask(__name__)
    # 必须设置密钥，否则 session 无法使用（必填！）
    app.secret_key = 'bettafish-login-2026-key'  # 任意字符串即可
    
    # 注册认证蓝图（登录/登出路由）
    from .auth import auth_bp
    app.register_blueprint(auth_bp)
    
    # 首页路由（验证登录状态）
    @app.route('/')
    def index():
        if 'username' in session:
            # 登录成功：渲染 templates/index.html 模板，传递用户名
            return render_template('index.html', username=session['username'])
        else:
            # 未登录：直接跳转到登录页（更友好）
            return "请先登录<br><a href='/login'>前往登录</a>" 
    return app




