from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
import re
from sendmessage import sendMessage


class findMail:
    def __init__(self, link):
        self.link = link
        self.request_data = requests.get(self.link)
        self.parsed_url = urlparse(self.link)
        self.domain_name = self.parsed_url.netloc
        self.emails = []
        self.links = []
        self.contact_links = []
        self.social_links = []

    def normal_scrape(self, link=''):
        self.links = []
        if link == '':
            link = self.link
        self.request_data = requests.get(link)
        soup = BeautifulSoup(self.request_data.text, 'html.parser')
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', soup.text)
        if len(emails) and isinstance(emails, str) and emails.find('grievance') == -1:
            self.emails.append(emails)
        elif len(emails):
            for i in emails:
                if i.find('grievance') == -1:
                    self.emails.append(i)

        self.links = soup.find_all('a')

    def scrape_links(self):
        for i in self.links:
            try:
                if i.text.lower().find('contact') != -1 or i['href'].find('contact') != -1:
                    if i['href'] not in self.contact_links:
                        self.contact_links.append(i['href'])
                if i['href'].find('twitter.com') != -1 or i['href'].find('instagram.com') != -1 or i['href'].find(
                        'facebook.com') != -1:
                    if i['href'] not in self.social_links:
                        self.social_links.append(i['href'])
            except:
                continue

    def scrape_contact(self):
        if len(self.contact_links):
            contact = self.contact_links[0]
            if contact.find('.com') == -1 or contact.find('.in') == -1:
                self.normal_scrape(self.link + contact)
                self.scrape_links()
            else:
                self.normal_scrape(contact)
                self.scrape_links()

    def scrape_email_on_web(self):
        link = f"https://www.google.com/search?q={self.domain_name}+contact+email"
        self.normal_scrape(link)

    def run(self):
        self.normal_scrape()
        self.scrape_links()
        self.scrape_contact()
        self.scrape_email_on_web()
        print(self.emails)
        print(self.social_links)


cx = findMail('https://www.cricbuzz.com/')
cx.run()
sendMessage('hello there', 'ignore this', cx.emails, cx.social_links).run()
