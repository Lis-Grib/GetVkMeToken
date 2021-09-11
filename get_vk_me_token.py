import requests

login = input('Введите логин:  ')
password = input('Введите пароль:  ')
session = requests.Session()


def auth(login: str, password: str, two_fa: bool = False, code: str=None):
    return session.get(f'https://oauth.vk.com/token', params={
        'grant_type': 'password',
        'client_id': '6146827',
        'client_secret': 'qVxWRF1CwHERuIrKBnqe',
        'username': login,
        'password': password,
        'v': '5.131',
        '2fa_supported': '1',
        'force_sms': '1' if two_fa else '0',
        'code': code if two_fa else None
    }).json()


response = auth(login, password)

if 'validation_sid' in response:
    print('Получить код по смс: 1\nПолучить код из лс администрации по токену: 2')
    type = input('1 или 2:  ')
    if type == '1':
        session.get("https://api.vk.com/method/auth.validatePhone", params={'sid': response['validation_sid'], 'v': '5.131'})
        response = auth(login, password)
        code = input('Введите код из смс:  ')
        response = auth(login, password, two_fa=True, code=code)
    elif type == '2':
        token = input('Введите токен: ')
        code = requests.get(
            f'https://api.vk.com/method/messages.getHistory?user_id=100&count=1&access_token={token}&v=5.52').json()[
                   'response']['items'][0]['body'].split('\n')[2].split(' ')[3][:-1]
        response = auth(login, password, two_fa=True, code=code)


print(response)

# Спасибо https://vk.com/id266287518 и https://vk.me/id194861150.
# Если знаете как вызвать капчу во время получения токена - пишите мне https://vk.com/lis_eugene
# Да, я просто добавил автоматическое получение кода из лс администрации, ачё?)
