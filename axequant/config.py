import os
import json

with open('/etc/config.json') as config_file:
    config = json.load(config_file)


class Config:
    SECRET_KEY = config.get('SECRET_KEY')
    MONGODB_SETTINGS = config.get('MONGODB_SETTINGS')
    MAIL_SERVER = 'smtp.axequant.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = config.get('EMAIL_USER')
    MAIL_PASSWORD = config.get('EMAIL_PASS')
