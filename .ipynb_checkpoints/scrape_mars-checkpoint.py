from splinter import Browser
from bs4 import BeautifulSoup


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    # create marsp_data dict that we can insert into mongo
    marsp_data = {}

    # create a soup object from the html
    img_soup = BeautifulSoup(html, "html.parser")
    elem = img_soup.find(id="gridMulti")
    img_src = elem.find("img")["src"]

    # add our src to marsp data with a key of src
    marsp_data["src"] = img_src

    # create soup object from html
    html = browser.html
    report = BeautifulSoup(html, "html.parser")
    marsp_report = report.find_all("p")
    # add it to our marsp data dict
    marsp_data["report"] = build_report(marsp_report)
    # return our marsp data dict

    browser.quit()
    return marsp_data


# helper function to build marsp report
def build_report(marsp_report):
    final_report = ""
    for p in marsp_report:
        final_report += " " + p.get_text()
        print(final_report)
    return final_report