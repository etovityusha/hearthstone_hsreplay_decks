from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


class ChromeWrapper(webdriver.Chrome):
    def __init__(self, proxy=None, executable_path='/usr/bin/chromedriver'):
        self.proxy = proxy
        desired_capabilities = webdriver.DesiredCapabilities.CHROME.copy()
        if self.proxy:
            desired_capabilities['proxy'] = {
                "httpProxy": self.proxy,
                "ftpProxy": self.proxy,
                "sslProxy": self.proxy,
                "proxyType": "MANUAL",
            }
        super().__init__(
            options=self.chrome_settings(),
            executable_path=executable_path,
            desired_capabilities=desired_capabilities
        )

    def check_ip(self) -> str:
        self.get('https://2ip.ru')
        try:  # accept cookies
            self.find_element(By.XPATH, '/html/body/div[1]/div/p[3]/a[2]').click()
        except NoSuchElementException:
            pass
        return self.find_element(By.XPATH, '//*[@id="d_clip_button"]/span').text

    @staticmethod
    def chrome_settings() -> Options:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--ignore-ssl-errors=yes')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        return chrome_options
