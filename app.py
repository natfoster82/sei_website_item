from flask import Flask, request, current_app, render_template, url_for, abort, redirect
import requests
from requests.auth import HTTPBasicAuth
from itsdangerous import BadSignature, SignatureExpired
from helpers import redis_store, external_serializer


# app setup
app = Flask(__name__)
app.config.from_pyfile('config.py')


@app.route('/url', methods=['POST'])
def url():
    data = request.get_json() or request.form
    bin_id = data.get('bin_id')
    bin_version = data.get('bin_version', 1)
    response_id = data.get('response_id')
    external_token = data.get('external_token')
    token = external_serializer.dumps([bin_id, bin_version, response_id, external_token])
    return url_for('item', token=token, _external=True)


@app.route('/item/<token>', methods=['GET', 'POST'])
def item(token):
    try:
        bin_id, bin_version, response_id, external_token = external_serializer.loads(token, max_age=3600)
    except (BadSignature, SignatureExpired):
        abort(403)

    if request.method == 'POST':
        return redirect(url_for('thank_you'))

    start_url = 'http://jsbin.com/{0}/{1}/edit?html,output'.format(bin_id, str(bin_version))

    clone = requests.get('https://jsbin.com/clone', headers={'referer': start_url}, allow_redirects=False)
    fresh_url = 'http://jsbin.com' + clone.headers['Location']

    return render_template('item.html', url=fresh_url, token=token)


@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')
