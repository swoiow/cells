#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import socket
from json import dumps

from six.moves.urllib_parse import ParseResult, parse_qsl, unquote, urlencode, urlparse


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()

    return ip


def add_url_params(url, params):
    """ Add GET params to provided URL being aware of existing.

    :param url: string of target URL
    :param params: dict containing requested params to be added
    :return: string with updated URL

    >> url = 'http://stackoverflow.com/test?answers=true'
    >> new_params = {'answers': False, 'data': ['some','values']}
    >> add_url_params(url, new_params)
    'http://stackoverflow.com/test?data=some&data=values&answers=false'
    """
    # Unquoting URL first so we don't loose existing args
    url = unquote(url)
    # Extracting url info
    parsed_url = urlparse(url)
    # Extracting URL arguments from parsed URL
    get_args = parsed_url.query
    # Converting URL arguments to dict
    parsed_get_args = dict(parse_qsl(get_args))

    if isinstance(params, dict):
        # Merging URL arguments dict with new params
        parsed_get_args.update(params)

        # Bool and Dict values should be converted to json-friendly values
        # you may throw this part away if you don't like it :)
        parsed_get_args.update({k: dumps(v) for k, v in parsed_get_args.items() if isinstance(v, (bool, dict))})

        # Converting URL argument to proper query string
        encoded_get_args = urlencode(parsed_get_args, doseq=True)

    elif isinstance(params, str):
        encoded_get_args = params

    else:
        raise TypeError

    # Creating new parsed result object based on provided with new
    # URL arguments. Same thing happens inside of urlparse.
    new_url = ParseResult(
        parsed_url.scheme,
        parsed_url.netloc,
        parsed_url.path,
        parsed_url.params,
        encoded_get_args,
        parsed_url.fragment,
    ).geturl()

    return new_url


def get_encoding(response):
    """ Figure out charset problem.
    Example:
        is_same_charset, new_charset, old_charset = get_encoding(resp)
        if not is_same_charset:
            resp.encoding = new_charset
            html = resp.text.encode(new_charset)
    """

    # requests.utils.get_encoding_from_headers(res.headers)
    response_encode = response.encoding.upper()
    proposal_encode = response_encode

    def _search_encoding_from_content():
        charset = "ISO-8859-1"

        rule_for_charset = re.compile(r'(?<=charset=)[\w"-]+')
        rule_for_meta = re.compile(r'(?<=<meta)[\w\s=/"-;]+(?=>)')

        for line in response.iter_lines(decode_unicode=True):
            if rule_for_meta.search(line):
                meta_lines = rule_for_meta.findall(line)
                for meta_line in meta_lines:
                    if re.search(rule_for_charset, meta_line):
                        charset = rule_for_charset.findall(meta_line)[0].replace('"', "").upper()
                        break

        return charset.upper()

    if response_encode not in ["GB2312", "UTF-8", "GBK"]:
        proposal_encode = _search_encoding_from_content()

    is_proposal_encode = response_encode == proposal_encode
    return is_proposal_encode, proposal_encode, response_encode


smart_charset = get_encoding


def smart_response(response):
    """ return response body in human readable """
    is_proposal_encode, proposal_encode, response_encode = get_encoding(response)

    if not is_proposal_encode:
        response.encoding = proposal_encode
    return response


def format_chrome_request_headers(raw_header: str) -> dict:
    headers = {}
    raw_headers = raw_header.split("\n")
    for header in raw_headers:
        header = header.strip()
        if not header or header.startswith(":") or header.lower().startswith("if-"):
            continue

        k, v = header.split(":", 1)
        headers[k.strip()] = v.strip()

    return headers
