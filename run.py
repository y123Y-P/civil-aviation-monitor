# run.py（项目根目录，和 SingleEngineApp 同级）
from SingleEngineApp import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

