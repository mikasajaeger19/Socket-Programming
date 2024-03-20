import requests
from bs4 import BeautifulSoup
import sys
from urllib.parse import urljoin

session = requests.Session()
session.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"

def get_all_forms(url):
    soup = BeautifulSoup(session.get(url).content, "html.parser")
    return soup.find_all("form")

def form_details(form):
    detailsOfForm = {}
    action = form.attrs.get("action")
    method = form.attrs.get("method", "get")
    inputs = []

    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        input_value = input_tag.attrs.get("value", "")
        inputs.append({"type": input_type, "name": input_name, "value": input_value})

    detailsOfForm["action"] = action
    detailsOfForm["method"] = method
    detailsOfForm["inputs"] = inputs
    return detailsOfForm

def vulnerable(response):
    errors = {"quoted string not properly terminated",
              "unclosed quotation mark after the character string",
              "error in SQL syntax"
              }
    for error in errors:
        if error in response.content.decode().lower():
            return True
    return False

def scan_sql_injection(url):
    for form in get_all_forms(url):
        formDetails = form_details(form)
        data = {}
        for input_tag in formDetails["inputs"]:
            if input_tag["type"] == "hidden" or input_tag["value"]:
                data[input_tag["name"]] = input_tag["value"]
            elif input_tag["type"] != "submit":
                data[input_tag["name"]] = f"test"
        url = urljoin(url, formDetails["action"])
        if formDetails["method"] == "post":
            response = session.post(url, data=data)
        elif formDetails["method"] == "get":
            response = session.get(url, params=data)
        if vulnerable(response):
            print(f"[+] SQL Injection vulnerability detected, link: {url}")
        else:
            print(f"[-] No SQL Injection vulnerability detected, link: {url}")
            break

if __name__ == "__main__":
    url = "https://google.com"
    scan_sql_injection(url)
