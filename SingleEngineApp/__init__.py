from flask import Flask, session  # 🔴 关键：添加 session 导入！

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
        # 现在 session 已导入，不会报错
        return "欢迎回来！<br><a href='/logout'>退出登录</a>" if 'username' in session else "请先登录<br><a href='/login'>前往登录</a>"
    
    return app

