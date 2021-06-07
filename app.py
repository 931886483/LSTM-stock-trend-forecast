import pandas as pd
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
import os
from concurrent.futures import ThreadPoolExecutor
import pymysql
from sqlalchemy import create_engine
import traceback

executor = ThreadPoolExecutor(10)
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)


# 数据库连接信息
host = '127.0.0.1'
port = 3306
db = 'mysql'
user = 'root'
# TODO 输入密码
password = '1234'

conn = pymysql.connect(
    host=host,
    user=user,
    password=password,
    db=db,
    charset='utf8'
)



@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
def process():
    # if request.method == 'POST':
    #     f = request.files.get('fileupload')
    #     basepath = os.path.dirname(__file__)
    #     if f:
    #         filename = f.filename
    #         types = ['csv']
    #         if filename.split('.')[-1] in types:
    #             uploadpath = os.path.join(basepath, './', filename)
    #             f.save(uploadpath)
    #             cur = conn.cursor()
    #
    #             fname = str(f.filename).split(".")[0]
    #             df = pd.read_csv(f.filename, encoding='utf-8')
    #             engine = create_engine('mysql+pymysql://{}:{}@{}:3306/{}'.format(user, password, host, db))
    #
    #             df.to_sql(fname, engine, index=True)
    #             flash('Upload Load Successful!', 'success')
    #         else:
    #             flash('Unknown Types!', 'danger')
    #     else:
    #         flash('No File Selected.', 'danger')
    #     return redirect(url_for('process'))
    return render_template('index.html')



@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:

            return jsonify({'code': -1, 'filename': '', 'msg': 'No file part'})
        file = request.files['file']
        # if user does not select file, browser also submit a empty part without filename
        if file.filename == '':

            return jsonify({'code': -1, 'filename': '', 'msg': 'No selected file'})
        else:
            try:

                if file :
                    origin_file_name = file.filename

                    # filename = secure_filename(file.filename)
                    filename = origin_file_name
                    file.save(os.path.join("./", filename))
                    df = pd.read_csv(origin_file_name, encoding='utf-8')
                    engine = create_engine('mysql+pymysql://{}:{}@{}:3306/{}'.format(user, password, host, db))

                    df.to_sql(filename.split(".")[0], engine, index=True)

                    print("asfjhdsfdsgfd")





                    return jsonify({'code': 0, 'filename': origin_file_name, 'msg': ''})
                else:

                    return jsonify({'code': -1, 'filename': '', 'msg': 'File not allowed'})
            except Exception as e:
                traceback.print_exc()
                return jsonify({'code': -1, 'filename': '', 'msg': 'Error occurred'})
    else:
        return jsonify({'code': -1, 'filename': '', 'msg': 'Method not allowed'})


@app.route('/line')
def line():

    cur = conn.cursor()
    # fname = request.args.get("fname")
    # get annual sales rank
    sql = "select * from data1 limit 50"
    cur.execute(sql)
    content = cur.fetchall()

    # 获取表头
    sql = "SHOW FIELDS FROM data1"
    cur.execute(sql)
    labels = cur.fetchall()
    labels = [l[0] for l in labels]


    df = pd.read_csv("data1(单支股票).csv", sep=',', nrows =50)

    return render_template('line.html', labels=labels, content=content, fname='data1')





def return_img_stream(img_local_path):
    """
    工具函数:
    获取本地图片流
    :param img_local_path:文件单张图片的本地绝对路径
    :return: 图片流
    """
    import base64
    img_stream = ''
    print(img_local_path)
    with open(img_local_path, 'rb') as img_f:
        img_stream = img_f.read()
        img_stream = base64.b64encode(img_stream)
    return img_stream


if __name__ == '__main__':
    app.run()
