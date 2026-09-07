import unittest
from goldsky_client import fetch_resources, decode_graphql
from make_pipeline import build_pipeline


class GuideTests(unittest.TestCase):
    def test_short_rest_page_with_cursor_continues(self):
        calls = []
        def fetch(token):
            calls.append(token)
            return {'data': [1] if token is None else [2],
                    'pagination': {'next_page_token': 'next' if token is None else None}}
        self.assertEqual(fetch_resources(fetch), [1, 2])
        self.assertEqual(calls, [None, 'next'])

    def test_repeated_cursor_and_budget_are_errors(self):
        fetch = lambda _: {'data': [], 'pagination': {'next_page_token': 'x'}}
        with self.assertRaisesRegex(RuntimeError, 'repeated'):
            fetch_resources(fetch)
        with self.assertRaisesRegex(RuntimeError, 'incomplete'):
            fetch_resources(fetch, max_pages=1)

    def test_graphql_partial_success_is_not_complete(self):
        with self.assertRaises(RuntimeError):
            decode_graphql({'data': {'events': []}, 'errors': [{'message': 'query failed'}]})

    def test_backfill_bounds_are_required_and_preserved(self):
        config = build_pipeline(100, 110)
        self.assertEqual(config['sources']['fills']['filter'], 'block_number >= 100 AND block_number <= 110')
        self.assertTrue(config['job'])
        for bounds in [(-1, 2), (3, 2), (True, 2)]:
            with self.assertRaises(ValueError):
                build_pipeline(*bounds)


if __name__ == '__main__':
    unittest.main()
