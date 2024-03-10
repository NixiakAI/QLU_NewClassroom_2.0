import requests
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5


def login_jw_in_campus(username, password):
    session = requests.Session()
    session.get("http://jw.qlu.edu.cn/jwglxt/xtgl/login_slogin.html")
    session.get("http://jw.qlu.edu.cn/jwglxt/xtgl/login_slogin.html")
    get_public_key = session.get("http://jw.qlu.edu.cn/jwglxt/xtgl/login_getPublicKey.html")
    get_public_key_json = get_public_key.json()

    # 模数和指数的Base64编码值
    modulus_b64 = str(get_public_key_json["modulus"]).replace("/", "\/")
    exponent_b64 = get_public_key_json["exponent"]

    # 使用Base64解码模数和指数
    modulus_bytes = base64.b64decode(modulus_b64)
    exponent_bytes = base64.b64decode(exponent_b64)

    # 创建RSA公钥对象
    rsa_key = RSA.construct(
        (int.from_bytes(modulus_bytes, byteorder='big'), int.from_bytes(exponent_bytes, byteorder='big')))

    # 使用RSA公钥加密数据
    cipher = PKCS1_v1_5.new(rsa_key)
    ciphertext = cipher.encrypt(password.encode())

    # 将加密后的数据进行Base64编码
    encrypted_password_b64 = base64.b64encode(ciphertext).decode()

    data = {
        'csrftoken': '',
        'yhm': username,
        'mm': encrypted_password_b64
    }
    session.post("http://jw.qlu.edu.cn/jwglxt/xtgl/login_slogin.html", data=data)
    res = session.get("http://jw.qlu.edu.cn/jwglxt/xsxxxggl/xsgrxxwh_cxXsgrxx.html?gnmkdm=N100801&layout=default")
    cookies = session.cookies.get_dict()
    jsession, route = cookies['JSESSIONID'], cookies['route']
    cookiess = 'JSESSIONID=' + jsession + '; _ga=GA1.1.143709857.1695195016; ' \
                                          '_ga_8K3LJ62ZVF=GS1.1.1695195015.1.0.1695195017.0.0.0; JSESSIONID=' + \
               jsession + '; route=' + route
    getmessage = res.text
    getmessage.find('成绩信息')
    if getmessage.find('成绩信息') == -1:
        return '0'
    else:
        return cookiess


# 这里使用了齐鲁工业大学的sso认证登录，为了学校网络安全考虑，不使用sso登录
# def sso_login(username,password):
#     # username = "" # sso 平台 学号
#     # password = "" # sso 平台密码 明文
#     get = sso_qlu(username,password)
#     return get
