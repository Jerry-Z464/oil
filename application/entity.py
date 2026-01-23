from application import db
from sqlalchemy import DECIMAL


# 用户表
class User(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.SmallInteger, nullable=False)
    create_time = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    update_time = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(),
                            onupdate=db.func.current_timestamp())
    valid = db.Column(db.SmallInteger, nullable=False, default=1)

    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

    def __repr__(self):
        return f'<Users {self.username, self.password, self.role}>'


# 用户表
class Account(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    profile_photo = db.Column(db.String, nullable=True)
    phone_number = db.Column(db.String, nullable=False)
    dept_id = db.Column(db.Integer, nullable=True)
    role = db.Column(db.SmallInteger, nullable=False)
    work = db.Column(db.Integer, nullable=False, default=1)
    remark = db.Column(db.String, nullable=True)
    create_time = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    update_time = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(),
                            onupdate=db.func.current_timestamp())
    valid = db.Column(db.SmallInteger, nullable=False, default=1)

    def __init__(self, name, password, email, phone_number, dept_id, role):
        self.name = name
        self.password = password
        self.email = email
        self.phone_number = phone_number
        self.dept_id = dept_id
        self.role = role


# token表
class UserToken(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.Integer, nullable=False)

    def __init__(self, user_id, token, timestamp):
        self.user_id = user_id
        self.token = token
        self.timestamp = timestamp


# 部门表
class Dept(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    parent_id = db.Column(db.Integer, nullable=False)
    full_parent_id = db.Column(db.String, nullable=False)
    level = db.Column(db.SmallInteger, nullable=False)
    principal = db.Column(db.Integer, nullable=False)
    create_time = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    update_time = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(),
                            onupdate=db.func.current_timestamp())
    valid = db.Column(db.SmallInteger, nullable=False, default=1)

    def __init__(self, name, parent_id):
        self.name = name
        self.parent_id = parent_id


class DeviceData(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    code = db.Column(db.String, nullable=False)
    dp = db.Column(DECIMAL(10, 2), nullable=False)
    gvf = db.Column(DECIMAL(10, 2), nullable=False)
    gas_flow_rate = db.Column(DECIMAL(10, 2), nullable=False)
    liquid_flow_rate = db.Column(DECIMAL(10, 2), nullable=False)
    oil_flow_rate = db.Column(DECIMAL(10, 2), nullable=False)
    pressure = db.Column(DECIMAL(10, 2), nullable=False)
    temperature = db.Column(DECIMAL(10, 2), nullable=False)
    water_cut = db.Column(DECIMAL(10, 2), nullable=False)
    water_flow_rate = db.Column(DECIMAL(10, 2), nullable=False)
    create_time = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    update_time = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(),
                            onupdate=db.func.current_timestamp())
    valid = db.Column(db.SmallInteger, nullable=False, default=1)

    def __init__(self, code, dp, gvf, gas_flow_rate, liquid_flow_rate, oil_flow_rate, pressure, temperature, water_cut,
                 water_flow_rate):
        self.code = code
        self.dp = dp
        self.gvf = gvf
        self.gas_flow_rate = gas_flow_rate
        self.liquid_flow_rate = liquid_flow_rate
        self.oil_flow_rate = oil_flow_rate
        self.pressure = pressure
        self.temperature = temperature
        self.water_cut = water_cut
        self.water_flow_rate = water_flow_rate


class WaterCutSample(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    sample = db.Column(db.String, nullable=False)
    rolling_avg = db.Column(DECIMAL(10, 2), nullable=True)
    deviation_threshold = db.Column(DECIMAL(10, 2), nullable=True)
    deviation_avg = db.Column(DECIMAL(10, 2), nullable=True)
    start_sampling_time = db.Column(db.DateTime, nullable=False)
    end_sampling_time = db.Column(db.DateTime, nullable=False)
    create_time = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    update_time = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(),
                            onupdate=db.func.current_timestamp())
    valid = db.Column(db.SmallInteger, nullable=False, default=1)

    def __init__(self, sample, start_sampling_time, end_sampling_time):
        self.sample = sample
        self.start_sampling_time = start_sampling_time
        self.end_sampling_time = end_sampling_time


class Alarm(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    code = db.Column(db.String, nullable=False)
    alarm_type = db.Column(db.String, nullable=False)
    level = db.Column(db.SmallInteger, nullable=False)
    metric = db.Column(db.String, nullable=True)
    current_value = db.Column(db.String, nullable=False)
    threshold = db.Column(db.String, nullable=False)
    suggestion = db.Column(db.String, nullable=False)
    alarm_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.SmallInteger, nullable=False, default=0)
    create_time = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    update_time = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(),
                            onupdate=db.func.current_timestamp())
    valid = db.Column(db.SmallInteger, nullable=False, default=1)

    def __init__(self, code, alarm_type, level, metric, current_value, threshold, suggestion, alarm_time, status):
        self.code = code,
        self.alarm_type = alarm_type,
        self.level = level,
        self.metric = metric,
        self.current_value = current_value,
        self.threshold = threshold,
        self.suggestion = suggestion,
        self.alarm_time = alarm_time,
        self.status = status

    def to_dict(self):
        return {
            "id": self.id,
            "code": self.code,
            "alarmType": self.alarm_type,
            "level": self.level,
            "metric": self.metric,
            "currentValue": self.current_value,
            "threshold": self.threshold,
            "suggestion": self.suggestion,
            "alarmTime": self.alarm_time.strftime('%Y-%m-%d %H:%M:%S'),
            "status": self.status
        }


class OptimizerState(db.Model):
    """优化器状态"""
    __tablename__ = 'optimizer_state'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    enabled = db.Column(db.Boolean, nullable=False, default=False)
    bias_x = db.Column(db.Float, nullable=False, default=0.0)  # 偏差修正值
    activation_time = db.Column(db.DateTime, nullable=True)
    disabled_reason = db.Column(db.String, nullable=True)
    last_sample_time = db.Column(db.DateTime, nullable=True)
    create_time = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    update_time = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(),
                            onupdate=db.func.current_timestamp())
    valid = db.Column(db.SmallInteger, nullable=False, default=1)

    def __init__(self, enabled=False, bias_x=0.0, activation_time=None, disabled_reason=None, last_sample_time=None):
        self.enabled = enabled
        self.bias_x = bias_x
        self.activation_time = activation_time
        self.disabled_reason = disabled_reason
        self.last_sample_time = last_sample_time


class Config(db.Model):
    """配置参数"""
    __tablename__ = 'config'

    key = db.Column(db.String, primary_key=True, nullable=False)
    value = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)

    def __init__(self, key, value, description=None):
        self.key = key
        self.value = value
        self.description = description
