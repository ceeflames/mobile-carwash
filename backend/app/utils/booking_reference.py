import uuid


def generate_booking_reference() -> str:
    """
    Example:
    MCW-6A2F9C81
    """

    return f"MCW-{uuid.uuid4().hex[:8].upper()}"