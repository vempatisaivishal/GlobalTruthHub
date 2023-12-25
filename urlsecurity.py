import time
import requests
import ssl
from urllib.parse import urlparse
import whois
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver


class urlSecurity:
    def __init__(self, link):
        self.driver = webdriver.Chrome("C:/Users/vixha/webdriver/chromedriver.exe")
        self.url = link
        self.parsed_url = urlparse(self.url)
        self.domain_name = self.parsed_url.netloc
        self.certificate = ''

    def get_sss_certificate(self):
        try:
            self.certificate = ssl.get_server_certificate((self.domain_name, 443))
        except:
            self.certificate = ''

    def check_valid_sss_certificate(self):
        if self.certificate != '':
            try:
                ssl.create_default_context().load_verify_locations(cadata=self.certificate)
            except:
                self.certificate = ''

    def check_is_safe(self):
        check_domain = self.url.split("//")[0]
        if check_domain == 'http:':
            self.certificate = ''

    def check_is_domain_safe(self):
        try:
            domain_info = whois.whois(self.domain_name)
            expiration_date = domain_info.expiration_date

            if isinstance(expiration_date, list):
                expiration_date = expiration_date[0]

            if expiration_date is not None and expiration_date > datetime.datetime.now():
                print("Domain is registered and not expired")
            else:
                self.certificate = ''

        except:
            self.certificate = ''

    def send_sample_request(self):
        req = requests.get(self.url)
        if req.status_code != 200:
            self.certificate = ''

    def present_on_google_news(self):
        news_link = f"https://news.google.com/search?q={self.domain_name}"
        request_content = requests.get(news_link)
        context = BeautifulSoup(request_content.content, 'html5lib')
        links = context.find_all('a', class_='VDXfz')
        for i in links[:3]:
            request_link = i['href'].replace('.', 'https://news.google.com')
            self.driver.get(request_link)
            time.sleep(1)
            current_domain = self.driver.current_url.split("//")[-1].split("/")[0]
            if current_domain.lower() == self.domain_name.lower():
                return True
        return False

    def run(self):
        self.get_sss_certificate()
        self.check_valid_sss_certificate()
        self.check_is_safe()
        self.check_is_domain_safe()
        self.send_sample_request()
        self.present_on_google_news()

        if self.certificate == '':
            return False
        else:
            return True

