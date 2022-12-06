
from .models import Code
from . import db


def deactivate_invite_code(input_invite_code:Code):
    print('hole', input_invite_code)
    print('hole aaaa', input_invite_code.id)
    if not input_invite_code:
        return 

    # invite_code = Code.query.filter_by(id=input_invite_code).first()
    print('hola 2')

    # if invite_code:
    print('hola 3')
    # db.session.query(Code.id).filter(Code.id == str(input_invite_code.id)).update({'active': 0})
    input_invite_code.active = 0
    db.session.commit()