import argparse


from pyosint.core import wrapper, reporter


SUPPORTED_FORMATS = ["pdf", "json"]


def log(log_type, text):
    logs_type = {"info": "[I]: ",
                 "good": "[+]: ",
                 "bad": "[-]: ",
                 "error": "[X]: ",
                 "ask": "[?]: "}
    print(f"{logs_type[log_type]}{text}")


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                     description="-d DATA -o OUTPUT_TYPE (pdf or json) -c CATEGORY -f FILENAME")

    parser.add_argument('-d', '--data', type=str, help=argparse.SUPPRESS)
    parser.add_argument('-c', '--category', type=str, help=argparse.SUPPRESS)
    parser.add_argument('-o', '--output', type=str, help=argparse.SUPPRESS)
    parser.add_argument('-f', '--file', type=str, help=argparse.SUPPRESS)

    args = parser.parse_args()

    if args.data:
        if args.output:
            if args.file:
                if args.output in SUPPORTED_FORMATS:
                    category = args.category if args.category else None
                    log('info', f"Starting data parsing")
                    data = wrapper.Wrapper(args.data, category).handle_parsers()
                    log('good', 'Data was parsed.')
                    log('info', f"Starting data writing to {args.file} ({args.output} format)")
                    reporter.write_data(args.file, data, args.output)
                    log('good', f"Data was written to {args.file}")
                else:
                    log('error', 'Unsupported output type provided. Use -o pdf or -o json.')
            else:
                log('error', 'No output file name provided. Please use -f argument.')
        else:
            log('error', 'No output type provided. Please use -o argument.')
    else:
        log('error', 'No data provided. Please use -d argument.')


if __name__ == "__main__":
    main()
