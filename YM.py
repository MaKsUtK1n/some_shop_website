import requests
from playwright.async_api import async_playwright
from time import sleep
import json
import asyncio



class Yoomoney:
    async def _init__(self):
        self.playwright = await async_playwright().__aenter__()
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.playwright._loop = self.loop
        self.browser = await self.playwright.firefox.launch(headless=False)
        self.context = await self.browser.new_context()
        headers = {}
        with open("headers.txt") as hdrs:
            for line in hdrs:
                key, value = line.split(": ")
                headers[key] = value

        with open("cookies.json") as ck:
            cookies = json.load(ck)
        await self.context.add_cookies(cookies)
        self.page = await self.context.new_page()
        await self.page.set_extra_http_headers(headers)
        self.balance = await self.get_balance()
        return self


    async def save_cookies(self):
        with open("cookies.json", 'w') as ck:
            cookies = await self.context.cookies()
            print(cookies)
            json.dump(cookies, ck, ensure_ascii=True, indent=4)


    async def get_balance(self):
        await self.page.goto('https://yoomoney.ru/main')
        return int(await self.page.locator("//html/body/div[3]/div/div[1]/div/div[1]/div/div[2]/div[2]/div[1]/div/div/span[1]/span/span[1]").inner_text())


    async def replenish_steam(self, amount, username):
        amount = int(amount)
        assert self.balance >= amount, Exception("NO MONEY")
        await self.page.goto("https://yoomoney.ru/digital-goods/5197")
        self.page.locator("//html/body/div[2]/div/div[3]/div/div[1]/form/div[3]/div[3]/div[1]/div[1]/div/div/div[1]/span/span/input").fill(username)
        self.page.locator("//html/body/div[2]/div/div[3]/div/div[1]/form/div[3]/div[3]/div[1]/div[1]/div/div/div[2]/span/span/input").fill(str(amount))
        self.page.locator("//html/body/div[2]/div/div[3]/div/div[1]/form/div[3]/div[3]/div[1]/div[1]/div/div/div[3]/div/button").click()
        sleep(3)
        self.page.locator("//html/body/div[2]/div/div[1]/div[1]/div[4]/div[3]/div/div/div[2]/div/div/div[1]/button").click()
        self.balance = await self.get_balance()
    


async def main():
    YM = await Yoomoney()._init__()
    print(await YM.get_balance())
    input()
    await YM.save_cookies()



if __name__ == "__main__":
    asyncio.run(main())