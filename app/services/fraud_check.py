def check_fraud(file_path: str) -> bool:
    with open(file_path, "r") as f:
        content = f.read()
    return "fraud" in content.lower()