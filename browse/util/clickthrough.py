"""Functions to create hashes for Click through links.

These are used to log to the web acccess logs when the bookmarking
links are clicked.

The hash is used to prevent malicious use of the click through
controller to create links that look like they are on arXiv but get
redirected to malware or something.
"""

import mmh3
from typing import Callable


def create_hash(secret: str, url: str) -> str:
    """Creates a hash of the secret and url."""
    # murmer is faster and more random that MD5 which was used in arXiv classic
    return str(mmh3.hash_bytes(secret + url).hex())


def is_hash_valid(secret: str, url: str, ct_hash: str) -> bool:
    """Given the secret and url, check if ct_hash was generated by create_hash."""
    return ct_hash == create_hash(secret, url)


def create_ct_url(secret: str, url_for: Callable[..., str], url: str) -> str:
    """Creates a URL to the clickthrough service with a valid hash."""
    return url_for('browse.clickthrough', url=url, v=create_hash(secret, url))