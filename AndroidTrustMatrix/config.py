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
    http = config.get('proxy','http')
    https = config.get('proxy','https')
    proxy = { "http": http, "https": https}
    return proxy

def get_user_agent():
    agent = config.get('proxy','agent')
    return agent

def get_repo_dir():
    repodir = config.get('repo','repodir')
    return repodir

def get_clam_socket():
    socketadd = config.get('clamav','unixsock')
    return socketadd

def get_adb_config():
    host = config.get('adb','host')
    port = int(config.get('adb','port'))
    return (host,port)

def get_temp_apk_path():
    path = config.get('temp','apk_path')
    return path

def get_tor_admin():
    ip = config.get('tor','ip')
    port = int(config.get('tor','port'))
    password = config.get('tor','auth')
    return (ip,port,password)

def get_appcount():
    count = config.get('AndroidTestMatrix','appcount')
    return int(count)