import json
from playwright.sync_api import sync_playwright

FOLLOWERS_PATH = "./connections/followers_and_following/followers_1.json"
FOLLOWING_PATH = "./connections/followers_and_following/following.json"

with open(FOLLOWERS_PATH, "r") as file:
    followers = json.load(file)

with open(FOLLOWING_PATH, "r") as file:
    following = json.load(file)
following = following["relationships_following"]

instagram_opps = []

for potential_opp in following:
    is_opp = True

    for follower in followers:
        if (potential_opp["title"] == follower["string_list_data"][0]["value"]):
            is_opp = False
            break

    if (is_opp == True):
        instagram_opps.append(potential_opp["title"])

# Instagram pages are rendered via JavaScript on the client side so the static HTML is not avaiable with python requests
# instead we use a headless browser like Playwright to simulate the JavaScript rendering and then query the DOM

real_instagram_opps = []
with sync_playwright() as playwright:
    chromium = playwright.chromium
    browser = chromium.launch()
    page = browser.new_page()
    page.set_extra_http_headers({"User-Agent": "Instagram Opps v3 by _nathanau"})
    for instagram_opp in instagram_opps:
        profile_url = "https://www.instagram.com/" + instagram_opp
        page.goto(profile_url)
        content = page.content()
        if ("Profile isn't available" not in content):
            real_instagram_opps.append(instagram_opp)

    browser.close()

print("List of your Instagram opps:")
for real_instagram_opp in real_instagram_opps:
    print(real_instagram_opp)

print("Thank you for using Instagram Opps v3")