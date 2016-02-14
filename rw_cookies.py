import pickle

def filter_cookie(cookies, domain):
    cookies = [i for i in cookies if domain in i[u'domain']]
    return cookies

def store_cookies(driver):
    cookies = driver.get_cookies()
    cookies = filter_cookie(cookies, 'taobao.com')
    pickle.dump(cookies , open("cookies.pkl","wb"))

def load_cookies(driver=None):
    cookies = pickle.load(open("cookies.pkl", "rb"))
    cookies = filter_cookie(cookies, 'taobao.com')
    if driver is not None:
        for cookie in cookies:
            driver.add_cookie(cookie)
    return cookies