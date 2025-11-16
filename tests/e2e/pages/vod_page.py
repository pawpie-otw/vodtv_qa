from tests.utils import www_subpath, str_comp
from playwright.async_api import Page, Locator, expect, TimeoutError

HOME_URL = "https://vod-tv.pl/"
SEARCH_EL = 'input.input__Input-sc-dbb50d3a-2.klesmZ'
ARTICLE_EL = "article.production__ProductionCard-sc-77f87755-0.kqTFZd"
PLAY_BTN_EL = "button.plyr__control.plyr__control--overlaid"
PLAY_BTN_2_EL = 'button.plyr__controls__item.plyr__control'
ARTILE_TITLE_EL_RELPATH = "p a"
POPUP_REGISTER_BTN_EL = 'span#register-now.FinalMessage__StyledButton-sc-14cea9d8-4.LAnxm.bg-green'


async def get_title(article: Locator):
    title_el = article.locator("p.production__Title-sc-77f87755-7 a")
    return (await title_el.inner_text()).strip()


async def get_video_href(video_article: Locator):
    return await video_article.locator(ARTILE_TITLE_EL_RELPATH).get_attribute('href')


class VodPage:

    def __init__(self, page: Page):
        self._page = page

    @property
    def url(self):
        return self._page.url

    async def search_video(self, video_title: str):
        await self._page.fill(SEARCH_EL, video_title)
        return await self._any_video_found()

    async def goto_homepage(self):
        await self._page.goto(HOME_URL)
        await self._reject_userdata_usage()
        await self._wait_for_selector(SEARCH_EL)

    async def goto_subpage(self, subpath: str):
        await self._page.goto(www_subpath(HOME_URL, subpath))

    async def get_h1_text(self, timeout: float = 3_000) -> str:
        await self._wait_for_selector('h1', timeout)
        return (await self._page.locator('h1').inner_text()).strip()

    async def video_exists(self, timeout: float = 3_000) -> bool:
        if timeout:
            await self._wait_for_video_el()
        count = await self._page.locator('video').count()
        return count == 1

    async def get_video_article(self, video_title):
        articles = self._page.locator(ARTICLE_EL)
        for i in range(await articles.count()):
            article = articles.nth(i)
            art_title = await get_title(article)
            if str_comp(art_title, video_title, False):
                return article
        return None

    async def _wait_for_video_el(self, timeout=3_000):
        await self._wait_for_selector('video', timeout)

    async def _any_video_found(self):
        try:
            await self._wait_for_selector(ARTICLE_EL, timeout=5_000)
            return True
        except TimeoutError:
            no_video_txt = "Nie znaleziono filmów i seriali dla podanej frazy"
            await expect(self._page.get_by_text(no_video_txt)).to_have_count(1)
            return False

    async def _wait_for_selector(self, element: str, timeout: float = None, state: str = None):
        "timeout: timeout in seconds"
        await self._page.wait_for_selector(element, timeout=timeout, state=state)

    async def _reject_userdata_usage(self):
        await self._page.get_by_text("Nie zgadzam się").click()

    async def _wait_for_dom(self):
        await self._page.wait_for_load_state('domcontentloaded')

    async def click_pop_register(self):
        await self._page.locator(POPUP_REGISTER_BTN_EL).click(force=True)

    async def play_video(self):
        await self._page.wait_for_load_state('domcontentloaded')
        video = await self._page.locator('video').element_handle()
        await self._page.evaluate("(video) => video.readyState >= 3", video)
        await self._wait_for_selector(PLAY_BTN_EL, timeout=5_000)
        await self._page.locator(PLAY_BTN_EL).scroll_into_view_if_needed()
        # V z jakiegoś powodu nie uruchamia poprawnie player'a
        # await vod_page.locator(PLAY_BTN_EL).click(force=True)
        # V a tu dochodzi do wiecznego buforowania filmu... ale popup się pojawia
        await self._page.evaluate(f'document.querySelector("{PLAY_BTN_EL}").click()')

    async def wait_for_popup(self):
        await self._wait_for_selector('#popup', timeout=60000, state='visible')

    @classmethod
    async def _get_article_title(cls, article: Locator, timeout=3_000):
        title_el = article.locator("p.production__Title-sc-77f87755-7 a")
        return (await title_el.inner_text(timeout)).strip()
