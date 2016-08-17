"""API.

api
"""
from flask import Blueprint, jsonify, request
from flask_security import auth_token_required

from tagio.models.user import User
from tagio.extensions import csrf_protect

blueprint = Blueprint('api',
                      __name__,
                      url_prefix='/api')


@blueprint.route('/v<string:version>/login', methods=['POST'])
@csrf_protect.exempt
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

    user = User.query.filter(User.username == username).first()
    if user is None:
        return jsonify({'code': 2, 'msg': 'Invalid parameter'})

    flag = user.check_password(password)
    if not flag:
        return jsonify({'code': 2, 'msg': 'Invalid parameter'})

    return jsonify({'code': 0, 'token': user.get_auth_token()})


@blueprint.route('/v<string:version>/users', methods=['GET'])
@auth_token_required
def users(version):
    """Users.

    list all users.
    """
    if version == "1":
        users = User.query.all()
        return jsonify({'code': 0, 'msg': {user.id : {'name': user.username} for user in users}})

    return jsonify({'code': 1, 'msg': 'Invalid version'})
