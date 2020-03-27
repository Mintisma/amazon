db = {
    'HOST': '52.82.28.224',
    'USER': 'root',
    'PASSWORD': 'sellermotor',
    'NAME': 'test',
}

proxyHost = 'http-dyn.abuyun.com'
proxyPort = '9020'
proxyUser  = 'HN493748JSXCE76D'
proxyPass = '631CE00CFB1E61BC'

proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host": proxyHost,
    "port": proxyPort,
    "user": proxyUser,
    "pass": proxyPass,
}

proxies = {
    "http": proxyMeta,
    "https": proxyMeta,
}