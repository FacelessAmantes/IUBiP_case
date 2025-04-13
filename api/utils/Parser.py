import nodriver as uc
import price_script

class Parser:

    def __init__(self):
        self.driver = None 

    async def open(self):
        self.driver = await uc.start(no_sandbox=True)

    async def get_page_content(self, url):
        if self.driver:
            
            page = await self.driver.get(url=url)
            time.sleep(10)
            
            return await page.get_content()
        else:
            raise ValueError('Драйвер не открыт')

    async def close(self):
        if self.driver:
            self.driver.stop()


async def test():

    parser = Parser()

    await parser.open()

    url = "https://market.yandex.ru/product--maska-sfericheskaia-polnolitsevaia-6800-panoramnaia-s-filtrami/1909972184?sku=102203133644&uniqueId=12707986&do-waremd5=AQWmagIiuUGWV4CFjuBXwg&sponsored=1&cpc=yT4SBUOzqcmPpY9DZIJTj93tgS_GXjYeQy6V4vuCJNOiZXpJa7LbfZh-VXYc2aqK10y0Ps0stt-VzOPIj3fz-J_UdPYbEZ9F98yRCy04JY-R1BiCOmBonuJuR8G8r5cQqAzVBoTBilJK27UaSyLlZs3cbqkGV4FziNb46Jzq9VM4ql6Mvxt0OWOoL_Bj7z2Ky2EHB9Sl_S5AzqJ-knbWF0rw8YvoIvue79FIwzgzSiS3pC3BmIE3dTulZA4NIEtse_Yt3IiW_UpYXTNrkxmUNDxgzak3cI31wDVA25EHk_0npcR6UwnGjKFoEH_FGQhWAhM4L8qmiYLsa80qUcSPDQwcp7KkZ3CGURx8BJz4_3-_SK2WHWPIxMWnSXdBwBJX9SQiPbtoETdqDYCFfCOyXTuexN9TOjjWZmS-0Tcp4w3bVc8gKZxUoQFnroKQ-EA_TVM25dNrk9wef3oCjSSyACj-zFHqRCkl94J3jMnF0g1WJjohOn7J6Jz3vpDZPup_5ZWce_ZFdC4%2C"
    resp = await parser.get_page_content(url=url)

    resp = price_script.parse(url=url, html=resp)

    await parser.close()

    print(resp)
    
if __name__ == '__main__':
    import asyncio
    import time
    asyncio.run(test())

