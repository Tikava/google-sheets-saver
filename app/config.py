import os

sheet_link = os.getenv("SHEET_LINK")

token = os.getenv("TELEGRAM_TOKEN")

google_service_creditionals = dict(
    service_account_type = os.getenv("GOOGLE_SERVICE_ACCOUNT_TYPE"),
    project_id = os.getenv("GOOGLE_SERVICE_ACCOUNT_PROJECT_ID"),
    private_key_id = os.getenv("GOOGLE_SERVICE_ACCOUNT_PRIVATE_KEY_ID"),
    private_key = os.getenv("GOOGLE_SERVICE_ACCOUNT_PRIVATE_KEY").replace('__NEWLINE__', '\n'),
    client_email = os.getenv("GOOGLE_SERVICE_ACCOUNT_CLIENT_EMAIL"),
    client_id = os.getenv("GOOGLE_SERVICE_ACCOUNT_CLIENT_ID"),
    auth_uri = os.getenv("GOOGLE_SERVICE_ACCOUNT_AUTH_URI"),
    token_uri = os.getenv("GOOGLE_SERVICE_ACCOUNT_TOKEN_URI"),
    auth_provider_x509_cert_url = os.getenv("GOOGLE_SERVICE_ACCOUNT_AUTH_PROVIDER_X509_CERT_URL"),
    client_x509_cert_url = os.getenv("GOOGLE_SERVICE_ACCOUNT_CLIENT_X509_CERT_URL"),
    universe_domain = os.getenv("GOOGLE_SERVICE_ACCOUNT_UNIVERSE_DOMAIN")
)