from application import db

class Employees(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='员工唯一ID')
    employee_name = db.Column(db.String(50), nullable=False, comment='员工姓名')
    phone_number = db.Column(db.String(20), nullable=False, comment='员工手机号')
    email = db.Column(db.String(100), nullable=False, unique=True, comment='员工邮箱')
    employment_status = db.Column(db.Enum('Employed', 'Resigned'), nullable=False, comment='雇佣状态')
    position = db.Column(db.String(50), nullable=False, comment='职位')
    role = db.Column(db.String(50), nullable=False, comment='角色')

    def to_dict(self):
        return {
            "id": self.id,
            "employee_name": self.employee_name,
            "phone_number": self.phone_number,
            "email": self.email,
            "employment_status": self.employment_status,
            "position": self.position,
            "role": self.role
        }