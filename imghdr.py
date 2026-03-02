"""Minimal imghdr compatibility shim for Python 3.14+ where the stdlib module was removed."""

# Tweepy imports imghdr.what, so we provide a simple stub that always returns None.


def what(filename, h=None):
    """Return None for all image files (no detection)."""
    return None
