from flask import Blueprint

root = Blueprint('root', __name__, url_prefix='')

@root.route('/')
def index():
    
    status = {
        'code': 200,
        'message': 'This backend is UP!',
        'version': '1.0'
    }
    
    return status