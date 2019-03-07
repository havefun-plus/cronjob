"""
Copyright (c) 2012, Kenneth Reitz
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

    Redistributions of source code must retain the above copyright notice, this
    list of conditions and the following disclaimer.
    Redistributions in binary form must reproduce the above copyright notice,
    this list of conditions and the following disclaimer in the documentation
    and/or other materials provided with the distribution.
    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
    AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
    IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
    ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
    LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
    CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
            SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
            BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
            NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import logging
from functools import partial
from typing import Optional

import gevent
from cronjob.settings import settings
from cronjob.utils.loaders import load_object
from cronjob.utils.user_agents import replace_user_agent
from requests import Response, Session
from requests.exceptions import RequestException

LOGGER = logging.getLogger(__name__)

if settings.ENABLE_PROXY:
    LOGGER.info('loading proxy')
    proxy_cls = load_object(settings.PROXY_CLASS)
    proxy_obj = proxy_cls()


def request(method: str, url: str, **kwargs) -> Optional[Response]:
    session = kwargs.pop('session', None)
    use_proxy = kwargs.pop('use_proxy', settings.ENABLE_PROXY)
    retry_times = kwargs.pop('retry_times', settings.RETRY_TIMES)
    request_timeout = kwargs.pop('request_timeout', settings.REQUEST_TIMEOUT)
    if settings.ENABLE_REPLACE_USER_AGENT:
        replace_user_agent(kwargs)
    if session is None:
        session = Session()

    for i in range(retry_times):
        try:
            if use_proxy:
                proxy_ip = proxy_obj.get()
                kwargs['proxies'] = dict(http=proxy_ip)
                LOGGER.info(f'Use proxy, ip: {proxy_ip}')
            with gevent.Timeout(request_timeout):
                response = session.request(method, url, **kwargs)
            if response.status_code in settings.RETRY_HTTP_CODE:
                LOGGER.warn(
                    f'Retry {i} times, status_code:{response.status_code}')
            else:
                LOGGER.info(f'Request {url} success')
                return response
        except gevent.timeout.Timeout:
            LOGGER.warn(f'Retry {i} times, timeout')
        except RequestException as err:
            LOGGER.warn(f'Retry {i} times, error:{err}')


get = partial(request, 'GET')
options = partial(request, 'OPTIONS')
head = partial(request, 'HEAD')
post = partial(request, 'POST')
put = partial(request, 'PUT')
patch = partial(request, 'PATCH')
delete = partial(request, 'DELETE')
