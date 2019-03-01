from app.api import bp

@bp.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    pass

@bp.route('/user', methods=['GET'])
def get_users():
    pass


@bp.route('/user', methods=['POST'])
def create_user():
    pass

@bp.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    pass
