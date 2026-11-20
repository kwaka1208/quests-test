"""The daily report tool of Northwind. It works, but its help is empty.

  python report.py sales --days 3

You edit the help texts in build_parser(). Do not change anything else.
"""
import argparse
import sys

KINDS = ["sales", "users", "errors"]
FORMATS = ["text", "csv"]


def build_parser():
    parser = argparse.ArgumentParser(
        prog="report.py",
        description="",
    )
    parser.add_argument("kind", choices=KINDS,
                        help="")
    parser.add_argument("--days", type=int, default=7, metavar="N",
                        help="")
    parser.add_argument("--format", choices=FORMATS, default="text",
                        help="")
    parser.add_argument("--save", metavar="FILE",
                        help="")
    parser.add_argument("--quiet", action="store_true",
                        help="")
    return parser


def make_report(args):
    lines = [f"Report: {args.kind}, the last {args.days} days ({args.format} format)."]
    if args.kind == "errors":
        lines.append("3 errors were found. 2 are already fixed.")
    else:
        lines.append(f"The {args.kind} are going up. Good job, team!")
    return lines


def main():
    args = build_parser().parse_args()
    lines = make_report(args)
    if not args.quiet:
        print("\n".join(lines))
    if args.save:
        with open(args.save, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        print(f"Saved to {args.save}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
