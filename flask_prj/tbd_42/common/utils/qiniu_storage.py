# -*- coding: utf-8 -*-
# flake8: noqa

from qiniu import Auth, put_file, etag,put_data
import qiniu.config

from flask import current_app

def upload(data):
    # 需要填写你的 Access Key 和 Secret Key
    access_key = current_app.config.get("QINIU_ACCESS_KEY")
    secret_key = current_app.config['QINIU_SECRET_KEY']

    # 构建鉴权对象
    q = Auth(access_key, secret_key)

    # 要上传的空间
    bucket_name = current_app.config.get("QINIU_BUCKET_NAME")

    # 上传后保存的文件名
    key = None

    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 360000)
    # data表示上传文件的二进制流
    ret,info = put_data(token,key,data)
    print('info={}'.format(info))
    print('ret={}'.format(ret))

    return ret['key']

    # 要路径上传文件的本地
    # localfile = './sync/bbb.jpg'

    # ret, info = put_file(token, key, localfile)
    # print(info)
    # assert是python关键字，表示断言，判断结果是否符合预期；
    # assert ret['key'] == key
    # assert ret['hash'] == etag(localfile)


