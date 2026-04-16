import argparse

from marker_tool.pipeline import run_pipeline
from marker_tool.annotate import annotate_marker


def main():
    # create parser
    parser = argparse.ArgumentParser(description="Marker processing tool")

    # create subcommands
    subparsers = parser.add_subparsers(dest="command")

    # run: process multiple markers
    run_parser = subparsers.add_parser("run", help="process markers from file or folder")
    run_parser.add_argument("input", help="input file or folder")
    run_parser.add_argument("-o", "--output", help="output csv file")
    run_parser.add_argument("--direct", action="store_true", help="allow direct gene matching")
    run_parser.add_argument("--recursive", action="store_true", help="search subfolders")

    # query: annotate a single marker
    query_parser = subparsers.add_parser("query", help="annotate a single marker")
    query_parser.add_argument("marker", help="marker name")
    query_parser.add_argument("--direct", action="store_true", help="allow direct gene matching")

    # parse arguments
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return

    # execute command
    if args.command == "run":
        run_pipeline(
            input_path=args.input,
            output_path=args.output,
            allow_direct_gene=args.direct,
            recursive=args.recursive,
        )

    elif args.command == "query":
        result = annotate_marker(
            marker=args.marker,
            allow_direct_gene=args.direct,
        )

        for key, value in result.items():
            print(f"{key}: {value}")

if __name__ == "__main__":
    main()