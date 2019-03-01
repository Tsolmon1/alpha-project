import os
SECRET_KEY = 'p9Bv<3Eid9%$i01'
SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost/dreamteam_db'
ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
LANGUAGES = ['en', 'mn']
POSTS_PER_PAGE = 2

LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
MAIL_SERVER = os.environ.get('MAIL_SERVER')
MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
ADMINS = ['your-email@example.com']
