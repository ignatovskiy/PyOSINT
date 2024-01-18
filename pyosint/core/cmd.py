import argparse
from pathlib import Path
import json
from time import time
import traceback

from pyosint.core.logger import log


def handle_cmd_args_module(cls):
    class_name = cls.__name__

    parser = argparse.ArgumentParser(description=f'{class_name} Parsing Module')

    parser.add_argument('input_data', type=str, help='Input data for parsing')
    parser.add_argument('--data_type', type=str, default=None, help='Input data type')
    parser.add_argument('--hidden', action='store_true', help='Hide result print')
    parser.add_argument('--debug', action='store_true', help='Activate debug profile')
    parser.add_argument('--json', nargs='?', const=True, type=str, help='Save result to json file')
    parser.add_argument('--dir', type=str, default='.', help='Output dir for saving files')

    args = parser.parse_args()
    if args.debug:
        args = argparse.Namespace(
            input_data=args.input_data,
            data_type=None,
            hidden=True,
            json=True,
            debug=True,
        )

    instance = None

    start_time = time()

    for i in range(3):
        log("info", f"Starting parsing info about {args.input_data} via {class_name} module.")

        try:
            instance = cls(args.input_data, args.data_type).get_complex_data()
            break
        except Exception as e:
            log("bad", f"Parsing is failed.")
            log("bad", f"Error: {e}")

            if args.debug or i == 2:
                if args.debug:
                    traceback.print_exc()
                return None
            else:
                log("info", f"Running {i + 2}/3 attempt")

    processing_time = round(time() - start_time, 2)

    if not args.hidden:
        print(instance)

    result_type = type(instance).__name__
    result_len = len(instance)

    log("good", "Successfully parsed info.")
    log("info",
        f"It takes {processing_time}s. Result is {result_type} with {result_len} high-level items.")

    json_arg = args.json
    if json_arg:
        if isinstance(json_arg, str) and json_arg.endswith(".json"):
            json_arg = json_arg[:-5]
        else:
            json_arg = class_name.lower()

        json_path = str(Path(args.dir) / f"{json_arg}.json")

        with open(json_path, 'w', encoding='UTF-8') as f:
            json.dump({class_name: instance}, f, indent=4, ensure_ascii=False)

        log("good", f"Saved parsed info to {json_path}")
