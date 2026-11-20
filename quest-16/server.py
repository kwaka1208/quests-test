"""The beta server of Northwind Lunch. It works, but its messages are bad.

Stage 1: write the ERRORS messages and the help texts. Do not change anything else.
Run: python server.py --help
"""
import argparse
import sys

ERRORS = {
    "port_in_use": "PORT USED!!! FATAL ERROR!!!",
    "unknown_env": "Bad env. Are you stupid?",
}


def build_parser():
    parser = argparse.ArgumentParser(prog="server.py", description="Start the beta server of Northwind Lunch.")
    parser.add_argument("--env", default="beta",
                        help="")
    parser.add_argument("--port", type=int, default=8000,
                        help="")
    return parser


def main():
    args = build_parser().parse_args()
    if args.env not in ("staging", "beta"):
        print(ERRORS["unknown_env"].format(env=args.env, port=args.port))
        return 1
    if args.port == 8000:
        print(ERRORS["port_in_use"].format(env=args.env, port=args.port))
        return 1
    print(f"The {args.env} server is running on port {args.port}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
