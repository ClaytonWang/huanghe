# -*- coding: utf-8 -*-
"""
    >File    : rsp.py
    >Author  : YJD
    >Mail    : jindu.yin@digitalbrain.cn
    >Time    : 2022/11/23 13:17
"""
import re
import json
from fastapi import Request, Response


class ReadDataWrap:
    def __init__(self, obj):
        self._it = iter(obj)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            value = next(self._it)
        except StopIteration:
            raise StopAsyncIteration
        return value


async def add_common_response_data(request: Request, call_next) -> Response:
    response = await call_next(request)

    path: str = request.get('path')
    if not re.match('^/v\d+', path):
        return response

    # 注意性能
    resp_body = [section async for section in response.__dict__['body_iterator']]
    response.__setattr__('body_iterator', ReadDataWrap(resp_body))
    response_body = b''
    async for chunk in response.body_iterator:
        response_body += chunk

    fast_rsp_de = response_body.decode()
    try:
        fast_rsp = json.loads(fast_rsp_de)
    except json.JSONDecodeError:
        fast_rsp = fast_rsp_de

    status_code = response.status_code
    message = fast_rsp.get('detail') if fast_rsp and 'detail' in fast_rsp else str(fast_rsp) \
        if status_code > 300 or status_code < 200 else ''
    content = json.dumps(
            dict(
                success=True if 200 <= status_code < 300 else False,
                message=message,
                status=status_code,
                result=fast_rsp,
            ), ensure_ascii=False
        )
    headers = dict(response.headers)
    headers['content-length'] = str(len(content))
    return Response(
        content=content,
        status_code=status_code,
        headers=headers,
        media_type=response.media_type
    )
