import random
import requests
from flask import Flask, render_template, request
app = Flask(__name__)


@app.route("/")  # decorator
def hello():
    return "Hello World!"


@app.route('/hello')
def hello_new():
    return 'hello flask'


@app.route('/greeting/<string:name>')
def greeting(name):
    return f'반갑습니다! {name}님!'


@app.route('/cube/<int:num>/')
def cube(num):
    result = num**3  # num*num*num 와같다.
    return str(result)  # return은 string type만 됨


@app.route('/lunch/<int:person>')
def lunch(person):
    # menu 라는 리스트를 만들고
    # 사람 수 만큼 랜덤 아이템을 뽑아서 반환
    menu = ['닭가슴살','아메리카노','스트링치즈','삶은계란','고구마']
    order = random.sample(menu, person) # sample(리스트, 출력갯수)
    return f'{order} 주문할께요!'


@app.route('/html')
def html():
    return '''
    <h1>Happy Hacking!</h1><hr/>
    <p>즐겁게 코딩합시다 :)</p>
    '''


@app.route('/html_file')
def html_file():
    return render_template('html_file.html')


@app.route('/hi/<string:name>')
def hi(name):
    return render_template('hi.html',name=name)


@app.route('/cube_new/<int:number>')
def cube_new(number):
    # 계산
    result = number ** 3
    return render_template('cube_new.html',number=number, result=result)


@app.route('/naver')
def naver():
    return render_template('naver.html')


@app.route('/send')
def send():
    return render_template('send.html')


@app.route('/receive')
def receive():
    username = request.args.get('username')
    message = request.args.get('message')
    return render_template('receive.html',username=username,message=message)


# 사용자의 username 과 password 를 input 으로 받는다.
# form action 을 통해 login_check로 redirect 한다.
@app.route('/login')
def login():
    return render_template('login.html')


# 사용자의 입력이 admin / admin123 이 맞는지 확인한다.
# 맞으면 '환영합니다.' 아니면 '관리자가 아닙니다.'
# 라고 출력한다.
@app.route('/login_check')
def login_check():
    username = request.args.get('username')
    password = request.args.get('password')
    if username == 'admin'and password == 'admin123':
        message = '환영합니다.'
    else:
        message = '관리자가 아닙니다.'
    return render_template('login_check.html',username=username,password=password,message=message)


# 사용자의 로또 인풋을 받는다.
# lotto_result 로 보낸다.
@app.route('/lotto_check')
def lotto_check():
    return render_template('lotto_check.html')


@app.route('/lotto_result')
def lotto_result():
    # lott_check 에서 보낸 lotto_round input을 받는다.
    lotto_round = request.args.get('lotto_round')
    # string을 int로 변환하는 문법(타입변환)
    numbers = [int(num) for num in lotto_round.split()]
    url = 'https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=860'
    response = requests.get(url)
    json = response.json()
    winner = [json[f'drwtNo{i}'] for i in range(1, 7)]
    # 번호 당첨 여부 확인하기
    if len(numbers) != 6:
        result = '번호의 수가 6개가 아닙니다!'
    else:
        matched = len(set(winner) & set(numbers))
        if matched == 6:
            result = '1등입니다.!'
        elif matched == 5:
            if json['bnusNo'] in numbers:
                result = '2등입니다.'
            else:
                result = '3등입니다.'
        elif matched == 4:
            result = '4등입니다.!'
        elif matched == 3:
            result = '5등입니다.!'
        else:
            result = '꽝입니다.!'
    return render_template('lotto_result.html',winner=winner,numbers=numbers,result=result)


# app.py 파일이 'python app.py' 로 시작되었을 때
if __name__ == '__main__':
    app.run(debug=True)  # 자동으로 재시작