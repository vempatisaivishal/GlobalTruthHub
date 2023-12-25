import time

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class sendMessage:
    def __init__(self, news, title, emails, handles):
        self.true_news = news
        self.fake_news = title
        self.emails = emails
        self.handles = handles
        self.instagram = 'https://www.instagram.com/'
        self.twitter = 'https://twitter.com/'
        self.facebook = 'https://www.facebook.com/'
        self.mail = 'vishalvardhan24816@gmail.com'
        self.instagram_handle = ''
        self.twitter_handle = ''
        self.facebook_handle = ''

    def segregate_handles(self):
        for i in self.handles:
            if i.find('instagram') != -1:
                x = i
                com = i.find('com')
                com += 4
                stc = com
                while com < len(x) and x[com] != '/' and x[com] != '?':
                    com += 1
                x = x[stc:com]
                self.instagram_handle = x

            if i.find('twitter') != -1:
                x = i
                com = i.find('com')
                com += 4
                stc = com
                while com < len(x) and x[com] != '/' and x[com] != '?':
                    com += 1
                x = x[stc:com]
                self.twitter_handle = x

            if i.find('facebook') != -1:
                x = i
                com = i.find('com')
                com += 4
                stc = com
                while com < len(x) and x[com] != '/' and x[com] != '?':
                    com += 1
                x = x[stc:com]
                self.facebook_handle = x

    def segregate_emails(self):
        self.emails = set(self.emails)
        self.emails = list(self.emails)[:3]

    def send_email(self):
        for i in self.emails:
            sender_email = 'vishalvardhan24816@gmail.com'
            sender_password = 'vishal:)09876'
            receiver_email = i
            subject = 'Test Email'
            message = 'This is a test email sent from Python.'

            email_message = MIMEMultipart()
            email_message['From'] = sender_email
            email_message['To'] = receiver_email
            email_message['Subject'] = subject
            email_message.attach(MIMEText(message, 'plain'))

            smtp_server = 'smtp.gmail.com'
            smtp_port = 587
            smtp_connection = smtplib.SMTP(smtp_server, smtp_port)
            smtp_connection.starttls()

            smtp_connection.login(sender_email, sender_password)

            smtp_connection.sendmail(sender_email, receiver_email, email_message.as_string())

            smtp_connection.quit()

    def send_on_instagram(self):
        username = 'vishalvardhan24816@gmail.com'
        password = 'vishal102938'
        driver = Chrome(service=Service(ChromeDriverManager().install()))
        driver.get(self.instagram)
        driver.set_window_size(500, 600)
        time.sleep(3)
        username_element = driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input')
        password_element = driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input')
        login_element = driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]/button')
        username_element.send_keys(username)
        password_element.send_keys(password)

        login_element.send_keys(Keys.ENTER)
        time.sleep(6)
        not_now1 = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/div/div')
        not_now1.send_keys(Keys.ENTER)
        time.sleep(6)
        not_now2 = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]')
        not_now2.send_keys(Keys.ENTER)
        time.sleep(4)
        input_element = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/div[1]/nav/div/header/div/div/div[1]/div/input')
        print(self.instagram_handle)
        input_element.send_keys(self.instagram_handle)
        time.sleep(3)
        input_element = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/div[1]/nav/div/header/div/div/div[1]/div/div[3]/div/div[2]/div/div[1]/a')
        input_element.send_keys(Keys.ENTER)
        time.sleep(5)
        message_element = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/div[3]/div/div[2]/div')
        message_element.send_keys(Keys.ENTER)
        time.sleep(5)
        send_text_element = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div/div/div[1]/div[1]/div/div[2]/div/section/div/div/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea')
        send_text_element.send_keys(self.true_news + ' ' + self.fake_news)
        send_text_element.send_keys(Keys.ENTER)

        time.sleep(2)
        driver.quit()

    def send_on_twitter(self):
        username = 'VishalV24816'
        password = 'vishal102938'
        driver = Chrome(service=Service(ChromeDriverManager().install()))
        driver.get(self.twitter)
        time.sleep(3)
        login_element = driver.find_element(By.XPATH, '/ html / body / div[1] / div / div / div[1] / div / div[1] / div / div / div / div / div[2] / div / div / div[1] / a')
        login_element.send_keys(Keys.ENTER)
        time.sleep(3)
        email_element = driver.find_element(By.XPATH, '/ html / body / div[1] / div / div / div[1] / div[2] / div / div / div / div / div / div[2] / div[2] / div / div / div[2] / div[2] / div / div / div / div[5] / label / div / div[2] / div / input')
        email_element.send_keys(username)
        email_element.send_keys(Keys.ENTER)
        time.sleep(5)
        password_element = driver.find_element(By.NAME, 'password')
        password_element.send_keys(password)
        password_element.send_keys(Keys.ENTER)
        time.sleep(5)
        message_element = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/header/div/div/div/div[1]/div[2]/nav/a[4]')
        message_element.send_keys(Keys.ENTER)
        time.sleep(5)
        news_message_elements = driver.find_elements(By.CSS_SELECTOR, 'a')
        news_message_element = news_message_elements[len(news_message_elements)-2]
        news_message_element.send_keys(Keys.ENTER)
        time.sleep(7)
        input_element = driver.find_element(By.CSS_SELECTOR, 'input')
        input_element.send_keys(self.twitter_handle)
        time.sleep(4)
        user_elements = driver.find_elements(By.CSS_SELECTOR, 'div[role="button"]')
        user_element = user_elements[2]
        user_element.send_keys(Keys.ENTER)
        time.sleep(2)
        next_element = user_elements[1]
        next_element.send_keys(Keys.ENTER)
        time.sleep(3)
        text_input = driver.find_element(By.CSS_SELECTOR, 'div[role="textbox"]')
        text_input.send_keys(self.true_news + ' ' +self.fake_news)
        text_input.send_keys(Keys.ENTER)
        time.sleep(3)
        driver.quit()

    def send_on_facebook(self):
        username = 'vishalvardhan24816@gmail.com'
        password = 'vishal@09876'
        driver = Chrome(service=Service(ChromeDriverManager().install()))
        driver.get(self.facebook)
        email_element = driver.find_element(By.XPATH, '//*[@id="email"]')
        email_element.send_keys(username)
        password_element = driver.find_element(By.XPATH, '//*[@id="pass"]')
        password_element.send_keys(password)
        login_element = driver.find_element(By.CSS_SELECTOR, 'button')
        login_element.send_keys(Keys.ENTER)
        time.sleep(5)
        input_element = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div[2]/div[3]/div/div/div/div/div/label/input')
        input_element.send_keys("Shashank Patnam")
        input_element.send_keys(Keys.ENTER)
        time.sleep(6)
        message_element = driver.find_element(By.CSS_SELECTOR,
                                              'div[aria-label="Message"]')
        message_element.send_keys(Keys.ENTER)
        time.sleep(1)
        text_element = driver.find_element(By.XPATH,
                                           '/html/body/div[1]/div/div[1]/div/div[5]/div/div[1]/div[1]/div/div/div/div/div/div[2]/div[2]/div/div/div[4]/div[2]/div/div/div[1]')
        text_element.send_keys(self.true_news + ' ' + self.fake_news)
        text_element.send_keys(Keys.ENTER)
        time.sleep(2)
        driver.quit()

    def run(self):
        self.segregate_handles()
        # self.send_on_facebook()
        self.send_on_instagram()
        # self.send_on_twitter()
        # self.segregate_emails()
        # self.send_email()


# sendMessage('your account has been deleted by instagram ', 'ignore this', ['prabhakrishnam1976@gmail.com'], ['https://www.instagram.com/vissshhhnuuu/', 'https://twitter.com/cric_mawa_twts', 'https://facebook.com/Shashank Patnam']).run()


