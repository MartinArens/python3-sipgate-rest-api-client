#!/usr/bin/python3

from flask import Flask, redirect, request, jsonify, render_template
import requests
import urllib.parse

app = Flask(__name__)

config = {
    'client_id': 'WUSt6I1qYB',
    'client_secret': 'o3jsYhwuElCCXGm98IazfECxwV8gDarLi70omrG4k5rk5DQOpq',
    'redirect_uri': 'http://127.0.0.1:5000/callback',
    'api_base_uri': 'https://api.sipgate.com',
    'check_ssl': True,
    'access_token': None,
    'scope': 'all'
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    location = config.get('api_base_uri') + '/v1/authorization/oauth/authorize' + '?' + urllib.parse.urlencode(
        {'client_id': config.get('client_id'),
         'redirect_uri': config.get('redirect_uri'),
         'response_type': 'code',
         'scope': config.get('scope')})

    return redirect(location)


@app.route('/callback')
def callback():
    code = request.args.get('code')

    if code:
        payload = {
            'client_id': config.get('client_id'),
            'client_secret': config.get('client_secret'),
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': config.get('redirect_uri')
        }

        r = requests.post(config.get('api_base_uri') + '/v1/authorization/oauth/token',
                          data=payload, verify=config.get('check_ssl'))

        if r.status_code == 200:
            response = r.json()
            config['access_token'] = response.get('access_token')
            return jsonify(response)

        return str(r.status_code)

    return 'no code'


@app.route('/<get_title>')
def get_request(get_title):
    if not config.get('access_token'):
        return login()

    r = requests.get(config.get('api_base_uri') + '/v1/' + get_title,
                     headers={'Authorization': 'Bearer ' + config.get('access_token')},
                     verify=config.get('check_ssl'))

    if r.status_code == 200:
        return jsonify(r.json())

    return str(r.status_code)


if __name__ == '__main__':
    app.run(debug=True)
