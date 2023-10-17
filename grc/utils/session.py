import secrets


def generate_session_token():
    return secrets.token_urlsafe(16)

# def is_same_session(str: current_session_token, str: email_address):

