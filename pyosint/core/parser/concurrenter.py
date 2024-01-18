import concurrent.futures


def process_requests_concurrently(func, reqs=None, while_mode=False):
    index = 0
    should_break = False

    with concurrent.futures.ThreadPoolExecutor() as executor:
        while True:
            futures = [executor.submit(func, index)] if while_mode else [executor.submit(func, req) for req in reqs]

            for future in concurrent.futures.as_completed(futures):
                try:
                    should_break = future.result()
                except TypeError:
                    pass
            else:
                if should_break or not while_mode:
                    break
                else:
                    index += 1
