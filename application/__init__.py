import os
import sys
from jinja2 import Environment, FileSystemLoader
from loguru import logger
from flask import Flask, redirect
from flask_cors import CORS
from pymodbus.client.sync import ModbusSerialClient
from application.data.analyzer import TimeWindowDataStore
from config import load_config
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, static_folder='static', static_url_path='/monitor')

# 配置日志
'''
{time}: 记录日志的时间戳。
{level}: 日志级别，例如"INFO"、"WARNING"、"ERROR"等。
{message}: 日志消息内容。
{name}: 记录器（Logger）的名称。
{function}: 记录日志的函数或方法名称。
{line}: 记录日志的代码行号。
{thread}: 执行日志记录的线程名。
{exception}: 如果记录了异常信息，这个占位符将包含异常的详细信息。
'''
log_format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | " \
             "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
logger.add("log/app_{time:YYYY-MM-DD}.log", rotation="1 day", format=log_format, level="INFO")
# 动态扫描所有 mapper 目录 -----------------------------------
base_dir = os.path.dirname(os.path.abspath(__file__))
mapper_paths = []
template_files = {}
# 遍历 application 下的所有子目录
for root, dirs, _ in os.walk(base_dir):
    if "mapper" in dirs:
        mapper_path = os.path.join(root, "mapper")
        mapper_paths.append(mapper_path)
        logger.info(f"Loaded SQL模板目录: {mapper_path}")

        for file_root, _, files in os.walk(mapper_path):
            for file in files:
                if file.endswith(('.j2', '.sql')):
                    # 转换为小写进行比较
                    file_lower = file.lower()
                    if file_lower in template_files:
                        # 发现重复文件
                        logger.warning(f"Duplicate template file found: {file}")
                        logger.warning(f"  First location: {template_files[file_lower]}")
                        logger.warning(f"  Duplicate location: {os.path.join(file_root, file)}")
                        sys.exit(1)
                    else:
                        template_files[file_lower] = os.path.join(file_root, file)

# 初始化 Jinja2 环境
env = Environment(
    loader=FileSystemLoader(mapper_paths),
    autoescape=False,
    cache_size=-1
)

Config = None
# 加载配置文件
try:
    config_original, Config = load_config()
    app.config.from_object(Config)
    db = SQLAlchemy(app)
    # 允许所有来源的跨域请求
    CORS(app)
    # 初始化Modbus客户端
    modbus_client = ModbusSerialClient(
        method='rtu',
        port='/dev/ttyCOM5',
        baudrate=9600,
        parity='N',
        stopbits=1,
        bytesize=8,
        timeout=3
    )
    if not modbus_client.connect():
        logger.error("Modbus init connection failed")
    # max_size = int(Config.ROLLING_WINDOW * 60 / (Config.INTERVAL / 60))
    # # 初始化数据分析器
    # data_analyzer = TimeWindowDataStore(Config.ROLLING_WINDOW)

    # # 配置参数
    # config = {
    #     'smtp_enabled': False,
    #     'alert_recipients': ['admin@example.com'],
    #     'interval_seconds': 60  # 采集间隔
    # }
    #
    # # 1. 创建数据管理器
    # data_manager = TimeWindowDataManager(config)
    #
    # # 2. 创建告警管理器
    # alert_manager = UnifiedAlertManager(config, data_manager)
    #
    # # 3. 创建优化器
    # optimizer = IntegratedOptimizer(config, data_manager, alert_manager)


except Exception as e:
    logger.exception(e)


# 导入路由
from application.api.config import config_bp as prefix_config_bp
from application.api.log import log_bp
from application.api.optimizer import optimizer_bp
from application.api.controller.DeptController import dept_bp
from application.api.controller.AccountController import account_bp
from application.api.controller.SampleController import sample_bp
from application.api.controller.MonitorController import monitor_bp
from application.api.controller.AlarmController import alarm_bp
from application.api.controller.DataController import data_bp

# 将蓝图注册到应用程序
app.register_blueprint(prefix_config_bp)
app.register_blueprint(log_bp)
app.register_blueprint(monitor_bp)
app.register_blueprint(optimizer_bp)
app.register_blueprint(dept_bp)
app.register_blueprint(account_bp)
app.register_blueprint(sample_bp)
app.register_blueprint(alarm_bp)
app.register_blueprint(data_bp)


@app.route('/monitor')
def redirect_to_index():
    return redirect('/monitor/index.html')

