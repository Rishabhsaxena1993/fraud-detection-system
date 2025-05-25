def check_fraud(file_path: str) -> bool:
    # Dummy logic: TXT file ko check karo, fraud ke liye
    try:
        with open(file_path, "r") as f:
            content = f.read().lower()
            # Example: "fraud" word hai to fraud
            return "fraud" in content
    except Exception:
        return False  # Default non-fraud if file read fails