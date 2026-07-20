import argparse


def get_flags() -> argparse.Namespace:
    """Get flags of files parser"""
    parser = argparse.ArgumentParser(exit_on_error=False)

    parser.add_argument('--functions_definition', type=str,
                        default='data/input/functions_definition.json')
    parser.add_argument('--input', type=str,
                        default='data/input/function_calling_tests.json')
    parser.add_argument('--output', type=str,
                        default='data/output/function_calling_results.json')
    args = parser.parse_args()
    return args
