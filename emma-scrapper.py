from bs4 import BeautifulSoup
from time import sleep
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from flask import Flask, request
from flask_cors import CORS, cross_origin

baseUrl = 'https://emma.msrb.org/Security/Details/?id='
driver = webdriver.PhantomJS(
    service_args=['--load-images=no', '--disk-cache=true'])
delay = 5
driver.add_cookie({
    'domain': '.emma.msrb.org',
    'name': "Disclaimer4",
    'value': "msrborg",
    'path': '/',
    'expires': None
})

app = Flask(__name__)
CORS(app)


@app.route("/search")
def search(methods=["GET"]):
    try:
        URL = baseUrl+request.args["id"]
        print(URL)
        driver.get(URL)
        WebDriverWait(driver, delay).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'EMMA-light-blue')))
        box = driver.find_elements_by_class_name("EMMA-light-blue")
        return box[0].get_attribute('outerHTML')
        # with open('out.txt', 'w') as f:
        #     # print(box[0].get_attribute('outerHTML'), file=f)
        #     f.write(box[0].get_attribute('outerHTML'))
    except TimeoutException:
        return "Loading took too much time or the Cusip Id is wrong!"
    driver.quit


# renderedHtml = search("64966FT20")
# print(renderedHtml)
if __name__ == '__main__':
    app.run(debug=True)
