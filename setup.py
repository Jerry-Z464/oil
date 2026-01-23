import threading
from application import app
from application.data.collector import read_data


if __name__ == '__main__':
    # 采集处理数据
    data_thread = threading.Thread(target=read_data, daemon=True)
    data_thread.start()
    # 启动Flask服务
    app.run(host=app.config["HOST"], port=app.config["PORT"], debug=False)
