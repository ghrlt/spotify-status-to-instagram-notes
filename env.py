from dotenv import dotenv_values
import os

config = dotenv_values(".env")
APP_ENVIRONMENT = config.get('APP_ENVIRONMENT', 'development')

env = {
    **config,
    **dotenv_values(".env.local"),
    **dotenv_values(f".env.{APP_ENVIRONMENT}"),
    **dotenv_values(f".env.{APP_ENVIRONMENT}.local")
}

def isDevelopment():
    return APP_ENVIRONMENT == 'development'

def isProduction():
    return not isDevelopment()


SPOTIFY_CLIENT_ID = env.get('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = env.get('SPOTIFY_CLIENT_SECRET')
SPOTIFY_CLIENT_REDIRECT_URI = env.get('SPOTIFY_CLIENT_REDIRECT_URI')
SPOTIFY_CLIENT_SCOPE = env.get('SPOTIFY_CLIENT_SCOPE')

if not all([SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_CLIENT_REDIRECT_URI, SPOTIFY_CLIENT_SCOPE]):
    raise Exception('Missing SPOTIFY_ environment variables')


INSTAGRAM_USERNAME = env.get('INSTAGRAM_USERNAME')
INSTAGRAM_PASSWORD = env.get('INSTAGRAM_PASSWORD')
INSTAGRAM_2FA_SEED = env.get('INSTAGRAM_2FA_SEED')

INSTAGRAM_DEFAULT_AUDIENCE = int(env.get('INSTAGRAM_DEFAULT_AUDIENCE', 0))

if not INSTAGRAM_USERNAME or not INSTAGRAM_PASSWORD:
    raise Exception('Missing INSTAGRAM_ environment variables')

WORKING_DIRECTORY_PATH = env.get('WORKING_DIRECTORY_PATH')
if not WORKING_DIRECTORY_PATH:
    WORKING_DIRECTORY_PATH = os.getcwd()
