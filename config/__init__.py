import yaml

# 读取YAML配置文件
base_config_file_path = 'config/application.yaml'  # 替换为你的配置文件路径

with open(base_config_file_path, 'r', encoding='UTF-8') as file:
    basic_config = yaml.safe_load(file)

environment = basic_config['app']["environment"]
environment_config = 'config/application-' + environment + '.yaml'


def load_config():
    
    with open(environment_config, 'r', encoding='UTF-8') as f:
        config_original = yaml.safe_load(f)
    sqlalchemy_config = config_original['sqlalchemy']
    server_config = config_original['server']
    time_config = config_original['time']

    class Config:
        # 数据库连接字符串
        SQLALCHEMY_DATABASE_URI = sqlalchemy_config['SQLALCHEMY_DATABASE_URI']
        # 是否追踪数据库修改
        SQLALCHEMY_TRACK_MODIFICATIONS = sqlalchemy_config['SQLALCHEMY_TRACK_MODIFICATIONS']
        # 是否显示底层执行的SQL语句
        SQLALCHEMY_ECHO = sqlalchemy_config['SQLALCHEMY_ECHO']

        # 服务器配置
        HOST = server_config["host"]
        PORT = server_config["port"]
        DEBUG = server_config["debug"]

        # token失效时间
        TOKEN_TIME = time_config["token"]
        # 采集数据间隔
        INTERVAL = time_config["interval"]
        # 滚动窗口
        ROLLING_WINDOW = time_config["rolling_window"]

    return config_original, Config


def save_config(config):
    with open(environment_config, 'w', encoding='UTF-8') as f:
        yaml.dump(config, f)

