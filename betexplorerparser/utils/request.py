import asyncio
import concurrent.futures

import aiohttp
from fake_useragent import UserAgent
from aiohttp import ClientSession
from aiohttp_retry import RetryClient, ExponentialRetry
from tqdm.asyncio import tqdm


class Request:
    def __init__(self, max_workers: int = None):
        self._max_workers = max_workers
        self._start_timeout = 0.5
        self._attempts = 10

    def get(self, urls: list[tuple], desc: str, batch_size: int | None = 2048) -> list:
        """
        The function takes a list of tuples, where each tuple contains the url and the name of the page.
        It makes requests and then returns a list of pages.

        :param self: Refer to the object itself
        :param urls: list[tuple]: Specify the type of urls, which is a list of tuples
        :param desc: str: Describe the url
        :param batch_size: int | None: Specify the batch size of the urls
        :return: A list of pages
        """
        if batch_size:
            urls = self._separate_urls(urls, batch_size)
        pages = []
        with concurrent.futures.ProcessPoolExecutor(max_workers=self._max_workers) as executor:
            for page_set in executor.map(self._async_parse_wrapper, urls, [desc] * len(urls)):
                pages.extend(page_set)
        return pages

    def _async_parse_wrapper(self, urls: list[tuple], desc) -> list:
        return asyncio.run(self._async_parse(urls, desc))

    async def _async_parse(self, urls: list[tuple], desc: str) -> list:
        headers = {"User-Agent": UserAgent().random, 'x-requested-with': 'XMLHttpRequest'}
        retry_options = ExponentialRetry(attempts=self._attempts)
        tasks = []
        # connector = aiohttp.TCPConnector(limit=50)
        async with ClientSession(trust_env=False) as session:
            retry_client = RetryClient(raise_for_status=False,
                                       retry_options=retry_options,
                                       client_session=session,
                                       start_timeout=self._start_timeout)
            for url_set in urls:
                tasks.append(self._get_page(url_set, headers, retry_client))

            return await tqdm.gather(*tasks, desc=desc)

    @staticmethod
    async def _get_page(url_set: tuple, headers: dict, session: ClientSession | RetryClient) -> list:
        pages = []
        for url in url_set:
            async with session.get(url, headers=headers) as response:
                if response.ok:
                    pages.append(await response.text())
                else:
                    break
        return pages

    @staticmethod
    def _separate_urls(urls: list, batch_size: int) -> list[list]:
        batches = []
        for i in range(0, len(urls), batch_size):
            batches.append(urls[i: i + batch_size])
        return batches
