import random
import string
from database.user import User

def randomStringwithDigits(stringLength=10):
    """Generate a random string of letters, digits and special characters """
    password_characters = string.ascii_letters + string.digits
    return ''.join(random.choice(password_characters) for i in range(stringLength))


def check_user_exists(username, db):
    return db.session.query(User.id).filter_by(username=username).scalar() is not None

