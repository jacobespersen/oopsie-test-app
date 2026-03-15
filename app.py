"""
Minimal app with a deliberate, fixable bug for Oopsie error-ingestion testing.
"""


def get_user_input(raw: str | None) -> str:
    """
    Returns normalized user input. Returns an empty string when raw is None or empty.
    """
    if raw is None or raw == "":
        return ""  # Return empty string so caller can safely call .strip()
    return raw


def process_input(raw: str | None) -> str:
    """Process user input: normalize and strip whitespace."""
    value = get_user_input(raw)
    return value.strip()  # AttributeError when value is None


if __name__ == "__main__":
    process_input(None)
