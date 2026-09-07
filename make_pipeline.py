"""Generate a bounded Turbo backfill configuration locally; never deploy it."""
import argparse
import json


def build_pipeline(start, end):
    if isinstance(start, bool) or isinstance(end, bool) or not isinstance(start, int) or not isinstance(end, int):
        raise ValueError('Block bounds must be integers')
    if start < 0 or end < start:
        raise ValueError('Require 0 <= start_block <= end_block')
    return {
        'name': 'polymarket-fills-review', 'resource_size': 's', 'job': True,
        'sources': {'fills': {'type': 'dataset', 'dataset_name': 'polymarket.order_filled',
                             'version': '2.0.0', 'start_at': 'earliest',
                             'filter': f'block_number >= {start} AND block_number <= {end}'}},
        'transforms': {},
        'sinks': {'review': {'type': 'blackhole', 'from': 'fills'}},
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--start-block', required=True, type=int)
    parser.add_argument('--end-block', required=True, type=int)
    args = parser.parse_args()
    print(json.dumps(build_pipeline(args.start_block, args.end_block), indent=2))
    # JSON syntax is also valid YAML. Redirect to backfill.yaml for the Goldsky CLI.
