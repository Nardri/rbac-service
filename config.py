"""
Config Module
"""
# default import
from os import getenv, environ
from pathlib import Path  # python3 only

# Third party library
from dotenv import load_dotenv

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path, verbose=True)
defaultDB = 'postgresql://postgres:123456@localhost:5432/nadri-rbac-service'


class Config(object):
    """Base app configuration class"""

    TESTING = False
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URI', default=defaultDB)

    # Wrap the path in an object for enhanced functionality
    private_key = Path('./jwt_key')
    public_key = Path('./jwt_key.pub')

    if private_key.is_file() and public_key.is_file():
        environ['JWT_PRIVATE_KEY'] = open('jwt_key').read()
        environ['JWT_PUBLIC_KEY'] = open('jwt_key.pub').read()


class Development(Config):
    """Configurations for development environment"""

    DEBUG = True


class Production(Config):
    """Configurations for production environment"""

    pass


class Testing(Config):
    """Configurations for testing environment"""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = getenv('TEST_DATABASE_URI')

    environ['JWT_PRIVATE_KEY'] = (
        '-----BEGIN RSA PRIVATE KEY-----\n'
        'MIICXAIBAAKBgQDB1wc3qKUQADs+kfYq6FKY+mcdiwfc'
        'fxH2b7d0cMxWBpZuotcDHzAS6mkXthC+nObdpjt3G7gI'
        'o4ou+QSkTbZlKpHCHeBuINYDC5dasRxs8Z1XR7p3Nf98'
        'ppbdSODM29MG+4XCqc+DY4r8BgoV/Lde0ClHDI8h7U4s'
        'cZL6r5Y6CQIDAQABAoGAbqFnASFDc+pt5bwwnzSRT7Y6'
        'e+YJypLLkbcZIV/vf3mrCeHujV2TdnhLGrlSvTeXnBFw'
        'Bv7O/j84cq61M4EXA48xOngEPHrlml9R46MsPxnbDIVl'
        '4Ps99QfR04CVQogcmevpRULwGcWCCotyYfmCcds3sYeS'
        '6ZlpDIKFi+IaEDECQQDx1KzSa+j0+pF05y3gKo81qmwR'
        'XCofqPshA8mnrkHHKehrYbnUzcyJP3SXHDJNeSFlUVGm'
        'zskPMvgpa0xJPFLHAkEAzTKEoKISW/GjN2NO65xMWWe/'
        'Gvml3MWZU8+4h95kqWeJxFONcZCkt+I82U8YMaK+isga'
        'MmO5O0dSiT4rIXU8rwJBAL1JC1DUuA3whqPrQ4Q/q8KE'
        't3vLGQmY+Z/42AGQqtnaWpqabps7zonrCjYxEsqDMnmc'
        'cf3Pw55K9eVtn9N/DQcCQC8ZkG3apcIrBd7Z0aytNK00'
        '7h2//f1d8eLWBDJTruFfnbTNxOKzY8u9h2AOEqyaAYiT'
        'g8fbMhJUPbK47WeBpIsCQDUCQ9LXblBVxczWidI7WARJ'
        'UQG+qWKV77C50LpSlzSZRw0ZjmcjKXL7sTVnrcNuIlj+'
        'abtR4JUswaZ3oBiMfNQ='
        '\n-----END RSA PRIVATE KEY-----')

    environ['JWT_PUBLIC_KEY'] = (
        'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAAAgQDB1wc3'
        'qKUQADs+kfYq6FKY+mcdiwfcfxH2b7d0cMxWBpZuotcDH'
        'zAS6mkXthC+nObdpjt3G7gIo4ou+QSkTbZlKpHCHeBuIN'
        'YDC5dasRxs8Z1XR7p3Nf98ppbdSODM29MG+4XCqc+DY4r'
        '8BgoV/Lde0ClHDI8h7U4scZL6r5Y6CQ== ')


app_config = {
    'development': Development,
    'production': Production,
    'testing': Testing
}
