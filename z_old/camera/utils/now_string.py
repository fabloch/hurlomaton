from datetime import datetime

def now_string():
    """
    Returns a datetime string
    """
    return datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
