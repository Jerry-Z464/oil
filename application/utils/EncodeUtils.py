import base64
from datetime import datetime
from passlib.hash import sha256_crypt


# 生成token
def generate_token(user_id, role):
    token = generate_sha256(str(user_id) + str(datetime.now().time()))
    # 进行 Base64 编码
    return base64_encode(user_id) + "." + str(role) + "." + base64_encode(token)


# 密码加密 sha256
def generate_sha256(password):
    return sha256_crypt.using(salt_size=8, rounds=5000).hash(password)


# base64加密
def base64_encode(encode_str):
    return base64.b64encode(str(encode_str).encode("utf-8")).decode("utf-8")


# base64解密
def base64_decode(encode_str):
    return base64.b64decode(encode_str).decode("utf-8")
