from playwright.async_api import async_playwright  # pylint: disable=unused-import
from playwright.sync_api import ViewportSize, sync_playwright
import cv2
import datetime
import config


# Function to take a screenshot of the news header to add to the video.
def func_take_sitescreenshot(link: str, source: str):

    var_width = 1080
    var_height = 920
    with sync_playwright() as p:
        print(f"{str(datetime.datetime.utcnow().strftime('%m/%d/%Y - %I:%M:%S'))} - Launching Headless Browser to take ScreenShot...")

        browser = p.chromium.launch(
            headless=True,
            slow_mo=500,
            #args=["--disable-http2"]
        )  
        dsf = (1080 // 600) + 1

        ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
        context = browser.new_context(
            locale="en-us",
            color_scheme="dark",
            viewport=ViewportSize(width=var_width, height=var_height),
            #device_scale_factor=dsf,
            java_script_enabled=False,
            extra_http_headers={"sec-ch-ua": '"Chromium";v="125", "Not.A/Brand";v="24", "Google Chrome";v="125"'},
            user_agent=ua
        )

        #context.add_cookies(config.COOKIE_LIST)  # load preference cookies

        context.add_cookies([{"domain": ".nytimes.com", "path": "/", "name": "nyt-geo", "value": "US"},
                {"domain": ".nytimes.com", "path": "/", "name": "nyt-gdpr" ,"value": "0"},
                {"domain": ".nytimes.com", "path": "/", "name": "nyt-traceid" ,"value": "0000000000000000634c4a2bcc36f419"},
                {"domain": ".nytimes.com", "path": "/", "name": "nyt-us" ,"value": "0"}])

        page = context.new_page()
        page.set_viewport_size({'width': var_width, 'height':var_height})
        page.goto(link, timeout=60000)
        #page.wait_for_load_state()

        if(source == 'BBC'):
            locator = page.locator('.bbc-14gqcmb').bounding_box()
        elif(source == 'CNN'):
            locator = page.locator('.layout__top').bounding_box()
        elif(source == 'NYTimes'):
            locator = page.locator("[class='css-1vkm6nb ehdk2mb0']").bounding_box()
        elif(source == 'ThePost'):
            try:
                locator = page.get_by_test_id('article-topper').bounding_box()
            except:
                locator = page.locator("[class='wpds-c-gUgOEq']").bounding_box()

        page.screenshot(clip=locator,path=(config.PATH_TO_SCREENSHOT+'NewsScreenShot.png'))
        print(f"{str(datetime.datetime.utcnow().strftime('%m/%d/%Y - %I:%M:%S'))} - Screenshot taken")
        browser.close()
        if(source == 'NYTimes'):
            var_img = cv2.imread(config.PATH_TO_SCREENSHOT+"NewsScreenShot.png")

            height_cutoff = 400
            s1 = var_img[:height_cutoff, :]

            cv2.imwrite((config.PATH_TO_SCREENSHOT+"NewsScreenShot.png"), s1)

