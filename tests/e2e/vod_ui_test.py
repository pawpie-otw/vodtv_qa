import pytest
import logging
import pytest_asyncio

from functools import wraps
from urllib.parse import urlparse
try:
    from tests.utils import www_subpath, str_comp
except ImportError:
    from ..utils import www_subpath, str_comp

from playwright.async_api import async_playwright, Page, Locator, expect, TimeoutError

# ========= TEST PARAMS ======
#                    [(video_title, exists),]
HEADLESS = True
UI_VOD_TEST_PARAMS = [("The Pickup", True),
                      ("nieistniejacy film 12345", False)]

# ========= CONSTS =========

VOD_MAIN_PAGE_H1 = "VODtv - Obejrzyj Darmowe Filmy i Seriale Online na Najwyższym Poziomie"

# ======= PATHS ======
VOD_URL = "https://vod-tv.pl/"
SEARCH_EL = 'input.input__Input-sc-dbb50d3a-2.klesmZ'
ARTICLE_EL = "article.production__ProductionCard-sc-77f87755-0.kqTFZd"
PLAY_BTN_EL = "button.plyr__control.plyr__control--overlaid"
PLAY_BTN_2_EL = 'button.plyr__controls__item.plyr__control'
ARTILE_TITLE_EL_RELPATH = "p a"
POPUP_REGISTER_BTN_EL = 'span#register-now.FinalMessage__StyledButton-sc-14cea9d8-4.LAnxm.bg-green'


# ======== help functions =========

async def get_title(article: Locator):
    title_el = article.locator("p.production__Title-sc-77f87755-7 a")
    return (await title_el.inner_text()).strip()


async def get_video_href(video_article: Locator):
    return await video_article.locator(ARTILE_TITLE_EL_RELPATH).get_attribute('href')


class VodPage:
    HOME_URL = "https://vod-tv.pl/"
    SEARCH_EL = 'input.input__Input-sc-dbb50d3a-2.klesmZ'
    ARTICLE_EL = "article.production__ProductionCard-sc-77f87755-0.kqTFZd"
    PLAY_BTN_EL = "button.plyr__control.plyr__control--overlaid"
    PLAY_BTN_2_EL = 'button.plyr__controls__item.plyr__control'
    ARTILE_TITLE_EL_RELPATH = "p a"
    POPUP_REGISTER_BTN_EL = 'span#register-now.FinalMessage__StyledButton-sc-14cea9d8-4.LAnxm.bg-green'

    def __init__(self, page: Page):
        self._page = page

    # PROPERTIES ~ DATA

    @property
    def url(self):
        return self._page.url

    # MAIN METHODS

    async def search_video(self, video_title: str):
        await self._page.fill(SEARCH_EL, video_title)
        return await self._any_video_found()

    async def goto_homepage(self):
        await self._page.goto(self.HOME_URL)
        await self._reject_userdata_usage()
        await self._wait_for_selector(SEARCH_EL)

    async def goto_subpage(self, subpath: str):
        await self._page.goto(www_subpath(self.HOME_URL, subpath))

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

    # SUBMETHODS

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
        await self._page.wait_for_selector("video", timeout=10000)
        await self._page.wait_for_selector(PLAY_BTN_EL, state="visible", timeout=10000)
        await self._page.locator(PLAY_BTN_EL).scroll_into_view_if_needed()
        await self._page.locator(PLAY_BTN_EL).click(force=True)

    async def wait_for_popup(self):
        await self._wait_for_selector('#popup', timeout=60000, state='visible')

    @classmethod
    async def _get_article_title(cls, article: Locator, timeout=3_000):
        title_el = article.locator("p.production__Title-sc-77f87755-7 a")
        return (await title_el.inner_text(timeout)).strip()


# ======== fixtures =========


@pytest_asyncio.fixture()
async def vod_page():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=HEADLESS)
        page = VodPage(await browser.new_page())
        await page.goto_homepage()
        await page._wait_for_selector(SEARCH_EL, timeout=10_000)
        yield page
        await browser.close()


# ======= subtests functions ========

async def ui_subtest_search_video(page: VodPage, video_title: str):
    return await page.search_video(video_title)


async def ui_subtest_h1_match_text(page: VodPage, expected_txt: str):
    return expected_txt in await page.get_h1_text()


async def ui_subtest_title_is_available(page: VodPage,
                                        video_title: str):
    return await page.get_video_article(video_title)


async def ui_subtest_video_el_exists(page: VodPage):
    return await page.video_exists()


async def ui_subtest_popup_before_timeout(page: VodPage):
    await page.play_video()
    try:
        await page.wait_for_popup()
        return True
    except TimeoutError:
        return False


async def ui_subtest_log_popup_redirect_link(vod_page: VodPage):
    await vod_page._wait_for_dom()
    await vod_page.click_pop_register()
    if urlparse(VOD_URL).hostname != urlparse(vod_page.url).hostname:
        logger.warning(
            f'Register btn redirect to external domain {vod_page.url}')
    return True


# ======== test ========
@pytest.mark.asyncio
@pytest.mark.parametrize("video_title,video_exists", UI_VOD_TEST_PARAMS)
async def test_ui_e2e(vod_page: VodPage,
                      video_title: str,
                      video_exists: bool):

    # Sprawdzenie H1 na głównej stronie
    h1_txt = await vod_page.get_h1_text()
    assert await ui_subtest_h1_match_text(vod_page, VOD_MAIN_PAGE_H1), \
        f"Main page H1 doesnt match expected text '{VOD_MAIN_PAGE_H1}' != '{h1_txt}'"
    is_title_available = await ui_subtest_search_video(vod_page, video_title)
    if not video_exists:
        assert is_title_available is False, "Title should not be available..."
        return
    else:
        article = await ui_subtest_title_is_available(vod_page, video_title)
        assert isinstance(article, Locator), "No video with matched title."

        subpath = await get_video_href(article)
        await vod_page.goto_subpage(subpath)
        assert await ui_subtest_h1_match_text(vod_page, video_title), "H1 on video page does not contain title."
        assert await ui_subtest_video_el_exists(vod_page), "no video player detected on video page."
        assert await ui_subtest_popup_before_timeout(vod_page), "No popup detected for 60s video watching."
        assert await ui_subtest_log_popup_redirect_link(vod_page)
