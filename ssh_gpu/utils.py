import os
import base64

def generate_key_pair(bits=2048):
    """Generate an RSA key pair."""
    # This is a placeholder. In a real implementation, use a proper cryptographic library.
    private_key = os.urandom(bits // 8)
    public_key = base64.b64encode(private_key).decode('utf-8')
    return private_key, public_key

def validate_hostname(hostname):
    """Validate the hostname."""
    if not hostname or len(hostname) > 255:
        return False
    if hostname[-1] == ".":
        hostname = hostname[:-1]
    allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(x) for x in hostname.split("."))

def safe_string(s):
    """Ensure a string is safe for use in commands."""
    return ''.join(c for c in s if c.isalnum() or c in '._-')
