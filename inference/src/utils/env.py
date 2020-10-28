import os


def _get(env_key):
    return os.environ.get(env_key)


def get_secret_access():
    return _get('SECRET_ACCESS')
