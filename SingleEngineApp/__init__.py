from flask import Flask

def create_app():
    """应用工厂函数 - 初始化Flask应用，注册蓝图和核心配置"""
    app = Flask(__name__)
    # 会话密钥（生产环境需替换为随机生成的安全密钥，如：os.urandom(24)）
    app.secret_key = 'your-secret-key-here'
    
    # 注册认证蓝图（登录/登出功能）
    from .auth import auth_bp
    app.register_blueprint(auth_bp)
    
    # 首页接口 - 验证登录状态
    @app.route('/')
    def index():
        return "欢迎回来！" if 'username' in session else "请先登录"
    
    return app

