import os


def verify_document(filename: str) -> bool:
    try:
        # For TXT files
        if filename.endswith(".txt"):
            with open(filename, "r", encoding="utf-8") as f:
                text = f.read().lower()
                # Check for fraudulent keywords
                fraudulent_keywords = ["fraud", "fake", "forged"]
                if any(keyword in text for keyword in fraudulent_keywords):
                    return False  # Fraudulent
                return True  # Genuine
        # For PDFs (placeholder)
        elif filename.endswith(".pdf"):
            return True  # Abhi ke liye hamesha genuine
        else:
            return False  # Unsupported file type
    except Exception as e:
        print(f"Error verifying document: {e}")
        return False
