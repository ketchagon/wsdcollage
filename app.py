from flask import Flask, request, jsonify, abort
from flask_cors import CORS
import nanoid
import cv2
app = Flask(__name__)
CORS(app)
 

@app.route('/', methods=['GET', 'POST'])
def root():
    return '<h1>hello, world</h1>'

@app.route('/greet/<name>')
def greet(name):
    return f'hello, {name}!'

@app.route('/v1/photos', methods=['POST'])
def post_photos():
    if 'file' not in request.files:
        abort(400)
    
    file = request.files['file']
    if file.content_type != 'image/jpeg':
        abort(400)
        
    filename = f'{nanoid.generate(size=4)}.jpg'
    file.save(f'static/{filename}')
    img0 = cv2.imread(f'static/{filename}',1)
    cv2.imwrite(f'static/{filename}', img0)
    
    resp = {'url': f'/static/{filename}'}
    
    # 2つ目の画像の処理
    if 'preset_file' not in request.files:
        abort(400, 'Missing preset_file')

    preset_file = request.files['preset_file']
    if preset_file.content_type != 'image/jpeg':
        abort(400, 'preset_file must be a JPEG')
    preset_filename = f'preset_{nanoid.generate(size=4)}.jpg'
    preset_file.save(f'static/{preset_filename}')
    preset_img0 = cv2.imread(f'static/{preset_filename}', 1)
    cv2.imwrite(f'static/{preset_filename}', preset_img0)
            

    preset_img0 = cv2.resize(preset_img0,(538,413))

    x = 0
    y = 0

    img_dst = img0

    while y < 538:
        x=0
        while x < 413:
            a = preset_img0[x][y][0]
            b = preset_img0[x][y][1]
            c = preset_img0[x][y][2]
            img_dst[x+203][y+52] = [a,b,c]
            x+=1
        y+=1

    collage_name = f'{nanoid.generate(size=4)}.jpg'
    collage_path = f'static/{collage_name}'
    cv2.imwrite(collage_path, img_dst)
    resp = {'url':f'/static/{collage_name}'}

    return jsonify(resp)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
