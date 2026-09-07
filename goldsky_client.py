"""Goldsky read-only examples, Python 3.10+, standard library. No deployments."""
import json
import os
from urllib.request import Request, urlopen
from urllib.parse import urlencode


def decode_graphql(payload):
    if payload.get('errors'):
        raise RuntimeError('GraphQL returned errors; partial data is not a complete result')
    if 'data' not in payload:
        raise ValueError('Missing GraphQL data envelope')
    return payload['data']


def fetch_resources(fetch_page, *, max_pages=20):
    """Collect a bounded REST scan. Short pages do not imply end of pagination."""
    if max_pages < 1:
        raise ValueError('max_pages must be positive')
    rows, seen, token = [], set(), None
    for _ in range(max_pages):
        page = fetch_page(token)
        if not isinstance(page.get('data'), list) or not isinstance(page.get('pagination'), dict):
            raise ValueError('Unexpected paginated response')
        rows.extend(page['data'])
        if 'next_page_token' not in page['pagination']:
            raise ValueError('Missing next_page_token; cannot establish completeness')
        token = page['pagination']['next_page_token']
        if token is None:
            return rows
        if not isinstance(token, str) or not token or token in seen:
            raise RuntimeError('Invalid or repeated pagination token')
        seen.add(token)
    raise RuntimeError('Page budget exhausted; result is incomplete')


def list_pipelines():
    key = os.environ['GOLDSKY_API_KEY']
    def fetch(token):
        query = {'page_size': 50}
        if token is not None:
            query['page_token'] = token
        request = Request('https://api.goldsky.com/api/v1/pipelines?' + urlencode(query),
                          headers={'Authorization': 'Bearer ' + key,
                                   'Accept': 'application/json'})
        with urlopen(request, timeout=20) as response:
            return json.load(response)
    return fetch_resources(fetch)


def demo_rpc():
    # This is the public demo key documented by Goldsky, not an account credential.
    request = Request('https://edge.goldsky.com/standard/evm/1?key=demo',
                      data=json.dumps({'jsonrpc': '2.0', 'id': 1,
                                       'method': 'eth_blockNumber', 'params': []}).encode(),
                      headers={'Content-Type': 'application/json'})
    with urlopen(request, timeout=20) as response:
        payload = json.load(response)
    if 'error' in payload:
        raise RuntimeError('JSON-RPC returned an error')
    return {'chainId': 1, 'blockNumber': int(payload['result'], 16)}


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--list-pipelines', action='store_true', help='Requires your project API key')
    args = parser.parse_args()
    print(json.dumps(list_pipelines() if args.list_pipelines else demo_rpc(), indent=2))
