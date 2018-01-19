from flask import Flask, request, current_app, render_template, url_for, abort, redirect
import requests
from requests.auth import HTTPBasicAuth
from itsdangerous import BadSignature, SignatureExpired
from helpers import redis_store, external_serializer


# app setup
app = Flask(__name__)
app.config.from_pyfile('config.py')


@app.route('/url', methods=['POST'])
def get_url():
    data = request.get_json() or request.form
    plunk_id = data.get('plunk_id')
    response_id = data.get('response_id')
    external_token = data.get('external_token')
    token = external_serializer.dumps([plunk_id, response_id, external_token])
    return url_for('item', token=token, _external=True)


@app.route('/item/<token>', methods=['GET', 'POST'])
def item(token):
    try:
        plunk_id, response_id, external_token = external_serializer.loads(token, max_age=7200)
    except (BadSignature, SignatureExpired):
        abort(403)

    if request.method == 'POST':
        # https://run.plnkr.co/plunks/mIt9wGkL7YSo4Rjnez68/
        return redirect(url_for('thank_you'))

    url = 'https://plnkr.co/edit/{0}'.format(plunk_id)
    return render_template('item.html', url=url, token=token)


@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')
