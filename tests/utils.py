def str_comp(a: str, b: str, casesense: bool = True):
    if casesense:
        return a == b
    return a.casefold() == b.casefold()


def www_subpath(base: str, subpath: str) -> str:
    if not base:
        raise ValueError("base URL cannot be empty")
    if not subpath:
        return base
    return f"{base.rstrip('/')}/{subpath.lstrip('/')}"


def search_api_video(resp_data: dict, title: str):
    for video_data in resp_data:
        if str_comp(video_data['title'], title, False):
            return video_data
    return None
