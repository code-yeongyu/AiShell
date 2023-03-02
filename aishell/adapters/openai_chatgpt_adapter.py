from http.cookiejar import Cookie
from typing import Optional

from yt_dlp.cookies import SUPPORTED_BROWSERS, extract_cookies_from_browser
from yt_dlp.utils import YoutubeDLCookieJar


class OpenAIChatGPTAdapter:

    def __init__(self, browser_name: str):
        if browser_name not in SUPPORTED_BROWSERS:  # type: ignore
            raise ValueError(f'Browser {browser_name} is not supported. Supported browsers are: {SUPPORTED_BROWSERS}')
        self.BROWSER_NAME = browser_name

    def get_openai_cookies(self) -> dict[str, Optional[str]]:
        all_cookies: YoutubeDLCookieJar = extract_cookies_from_browser(self.BROWSER_NAME)
        try:
            openai_cookies: dict[str, Cookie] = all_cookies.__dict__['_cookies']['chat.openai.com']['/']
        except KeyError as error:
            raise ValueError('Could not find OpenAI cookies. Make sure you are logged in to OpenAI.') from error

        cookies: dict[str, Optional[str]] = {key: cookie.value for key, cookie in openai_cookies.items()}

        return cookies

    def get_openai_session_token(self) -> Optional[str]:
        return self.get_openai_cookies()['__Secure-next-auth.session-token']
