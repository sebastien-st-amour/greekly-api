import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import boto3

FIELD_LOOKUPS = {
    'username_input': (By.ID, "userId"),
    'password_input': (By.ID, "password"),
    'login_button': (By.XPATH, '//button[normalize-space()="Log in"]'),
    '2fa_continue_button': (By.XPATH, '//button[normalize-space()="Continue"]'),
    '2fa_code_input': (By.ID, "Code"),
    '2fa_code_verify_button': (By.XPATH, '//button[normalize-space()="Verify Now"]'),
    'profile_span': (By.XPATH, '//span[normalize-space()="Sebastien"]'),
    "last_login_panel": (By.CLASS_NAME, "qt-last-login_panel"),
    "fullscreen_loader": (By.CLASS_NAME, "fullscreen-loader"),
    'app_hub_link': (By.LINK_TEXT, "App hub"),
    'new_token_link': (By.LINK_TEXT, "Generate new token"),
    'token_value': (By.ID, "spanTokenValue"),
}

class SQSListener:
    
    def __init__(self, queue_url):

        self.queue_url = queue_url
        self.client = boto3.client('sqs')
        self.twofactor_token = None
    
    def __poll(self):
        
        response = self.client.receive_message(
            QueueUrl = self.queue_url,
            MaxNumberOfMessages = 1,
            WaitTimeSeconds = 20
        )
        
        if 'Messages' in response:
            return self.__handle_response(response)
        else:
            return None
    
    def __handle_response(self, response):

        message = response['Messages'][0]
        self.__delete(message['ReceiptHandle'])
        body = json.loads(message['Body'])
        content = json.loads(body['Message'])
        token = content['body']
        return token

    def __delete(self, receipt_handle):
        
        self.client.delete_message(QueueUrl = self.queue_url,ReceiptHandle = receipt_handle)
    
    def get_twofactor_token(self):
    
        while not self.twofactor_token: self.twofactor_token = self.__poll()

        return self.twofactor_token

class QuestradeSession(webdriver.Remote):
    
    
    def __init__(self, sqs_client: SQSListener, chrome_url : str):

        options = webdriver.ChromeOptions()

        options.add_argument("--window-size=1920,1080")

        super().__init__(chrome_url, DesiredCapabilities.CHROME, options=options)

        self.get("https://login.questrade.com/account/login")
        self.implicitly_wait(10)
        self.sqs_client = sqs_client

    def _get_element(self, name):

        return self.find_element(*FIELD_LOOKUPS[name])

    def get_api_token(self, username, password):

        self._get_element('username_input').send_keys(username)

        self._get_element('password_input').send_keys(password)

        self._get_element('login_button').click()

        self._get_element('2fa_continue_button').click()

        twofactor_token = self.sqs_client.get_twofactor_token()

        self._get_element('2fa_code_input').send_keys(twofactor_token)

        self._get_element('2fa_code_verify_button').click()

        WebDriverWait(self, 20).until(EC.invisibility_of_element(FIELD_LOOKUPS['last_login_panel']))

        self.execute_script("arguments[0].click();", WebDriverWait(self, 20).until(EC.element_to_be_clickable(FIELD_LOOKUPS['profile_span'])))

        WebDriverWait(self, 20).until(EC.invisibility_of_element(FIELD_LOOKUPS['fullscreen_loader']))

        self._get_element('app_hub_link').click()

        WebDriverWait(self, 20).until(EC.element_to_be_clickable(FIELD_LOOKUPS['new_token_link'])).click()

        token = WebDriverWait(self, 20).until(EC.visibility_of_element_located(FIELD_LOOKUPS['token_value'])).text

        return token