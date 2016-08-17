"""API.

api
"""
from flask import Blueprint, jsonify, request

from tagio.models.user import User

blueprint = Blueprint('api', __name__, static_folder='../static')


@blueprint.route('/v<string:version>/login', methods=['POST'])
def login(version):
    """Login.

    login to retrieve token.
    """
    if version == '1':
        return _login_first_version()

    return jsonify({'code': 1, 'msg': 'Invalid version'})


def _login_first_version():
    username = request.form.get('username')
    password = request.form.get('password')

    if username is None or password is None:
        return jsonify({'code': 2, 'msg': 'Invalid parameter'})

    username = username.strip().lower()

    user = User.query.filter(User.name == username).first()
    if user is None:
        return jsonify({'code': 2, 'msg': 'Invalid parameter'})

    flag = user.check_password(password)
    if not flag:
        return jsonify({'code': 2, 'msg': 'Invalid parameter'})

    return jsonify({'code': 2, 'token': 'Token'})
