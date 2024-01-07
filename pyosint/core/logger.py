def log(log_type: str, text: str) -> None:
    logs_type: dict = {"info": "[I]: ",
                       "good": "[+]: ",
                       "bad": "[-]: ",
                       "error": "[X]: ",
                       "ask": "[?]: "}
    print(f"{logs_type[log_type]}{text}")
