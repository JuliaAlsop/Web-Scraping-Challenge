from splinter import Browser
from bs4 import BeautifulSoup


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    # create mars_data dict that we can insert into mongo
    mars_data = {}

    # visit nasa.com
    nasa = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(nasa)
    browser.is_element_present_by_id("gridMulti", 1)
    html = browser.html

    # create a soup object from the html
    img_soup = BeautifulSoup(html, "html.parser")
    elem = img_soup.find(id="gridMulti")
    img_src = elem.find("img")["src"]

    # add our src to mars data with a key of src
    mars_data["src"] = img_src

    # visit nasa to get weather report
    weather = (
        "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    )
    browser.visit(weather)

    # grab our new html from nasa
    browser.is_element_present_by_css(".sl-premium-analysis-link", 1)
    analysis_url = browser.find_link_by_partial_href("premium-analysis").first["href"]
    browser.visit(analysis_url)
    browser.is_element_present_by_css(".sl-feed-article", 1)

    # create soup object from html
    html = browser.html
    report = BeautifulSoup(html, "html.parser")
    mars_report = report.find_all("p")
    # add it to our mars data dict
    mars_data["report"] = build_report(mars_report)
    # return our mars data dict

    browser.quit()
    return mars_data


# helper function to build mars report
def build_report(mars_report):
    final_report = ""
    for p in mars_report:
        final_report += " " + p.get_text()
        print(final_report)
    return final_report