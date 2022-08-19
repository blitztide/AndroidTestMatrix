from configparser import ConfigParser


config = ConfigParser()
config.read('config/config.ini')

def get_db_config():
    username = config.get('db','username')
    password = config.get('db','password')
    host = config.get('db','host')
    port = config.get('db','port')
    database = config.get('db','database')
    return (username, password, host, port, database)

def get_proxy_config():
    proxy = config.get('proxy','proxies')
    return proxy
