import requests

client = input('Получаем токен\n1)VK Official\n2)VK Me\n1 или 2:  ')
client = 'me' if client == 2 else 'off'
login = input('Введите логин:  ')
password = input('Введите пароль:  ')


session = requests.Session()


def auth(login: str, password: str, client: str, two_fa: bool = False, code: str=None):
    clients_ids = {'me': '6146827', 'off': '2274003'}
    clients_secrets = {'me': 'qVxWRF1CwHERuIrKBnqe', 'off': 'hHbZxrka2uZ6jB1inYsH'}
    return session.get(f'https://oauth.vk.com/token', params={
        'grant_type': 'password',
        'client_id': clients_ids[client],
        'client_secret': clients_secrets[client],
        'username': login,
        'password': password,
        'v': '5.131',
        '2fa_supported': '1',
        'force_sms': '1' if two_fa else '0',
        'code': code if two_fa else None
    }).json()


response = auth(login, password, client)
if 'validation_sid' in response:
    print('Получить код по смс: 1\nПолучить код из лс администрации по токену: 2')
    type = input('1 или 2:  ')
    if type == '1':
        session.get("https://api.vk.com/method/auth.validatePhone",
                    params={'sid': response['validation_sid'], 'v': '5.131'})
        response = auth(login, password, client)
        code = input('Введите код из смс:  ')
        response = auth(login, password, client, two_fa=True, code=code)
    elif type == '2':
        token = input('Введите токен: ')
        code = requests.get(
            f'https://api.vk.com/method/messages.getHistory?user_id=100&count=1&access_token={token}&v=5.52').json()[
                   'response']['items'][0]['body'].split('\n')[2].split(' ')[3][:-1]
        response = auth(login, password, client, two_fa=True, code=code)
print(f'Токен: {response["access_token"]} \nUser ID: {response["user_id"]}')

# Спасибо https://vk.com/id266287518, https://vk.me/id194861150 и https://github.com/vodka2.
# Если знаете как вызвать капчу во время получения токена - пишите мне https://vk.com/lis_eugene
# Да, я просто добавил автоматическое получение кода из лс администрации и получение токена офф версии, ачё?)
