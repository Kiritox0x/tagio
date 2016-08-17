"""User.

user controller
"""

from flask_security import login_required
from flask import Blueprint, render_template


blueprint = Blueprint('user',
                      __name__,
                      url_prefix='/users',
                      static_folder='../static')


@blueprint.route('/')
@login_required
def members():
    """List members."""
    return render_template('users/members.html')
