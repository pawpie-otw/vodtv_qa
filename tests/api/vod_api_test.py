import pytest
import requests
try:
    from tests.utils import search_api_video, www_subpath
except ImportError:
    from ..utils import search_api_video, www_subpath

# ======= TEST PARAMS ========
#                     [video_title]
API_VOD_TEST_PARAMS = ['the pickup']

# ======== CONSTS ==========
VOD_URL = "https://vod-tv.pl/"
REQUESTS_HEADERS = {"accept": "application/json, text/plain, */*",
                    "content-type": "application/json",
                    "origin": "https://vod-tv.pl",
                    "referer": VOD_URL,
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"}


@pytest.mark.asyncio
@pytest.mark.parametrize("video_title", API_VOD_TEST_PARAMS)
async def test_api(video_title: str):
    rqt_url = www_subpath(VOD_URL, "search-route")
    data = {"host": "vod-tv.pl",
            "locale": "pl",
            "searchTerm": video_title}
    resp = requests.post(rqt_url, headers=REQUESTS_HEADERS, json=data)
    resp_data = resp.json()['data']
    assert resp.status_code == 200, f"Wrong response code. expected= 200, current code= {resp.status_code}."
    assert search_api_video(resp_data, video_title), \
        "No expected video title in response data."
