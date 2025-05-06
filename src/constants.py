GUARDIAN_API_BASE_URL = "https://content.guardianapis.com"
GUARDIAN_API_SEARCH_ENDPOINT = f"{GUARDIAN_API_BASE_URL}/search"

# Error messages
ERROR_NO_API_KEY = "GUARDIAN_API_KEY not found in environment variables"

# API defaults
DEFAULT_PAGE_SIZE = 10
DEFAULT_ORDER_BY = "newest"

# Preview length
CONTENT_PREVIEW_LENGTH = 1000

# SQS Config
SQS_MAX_RETRIES = 5
SQS_RETRY_MODE = "standard"

# Logging messages
LOG_MESSAGE_SENT = "Message sent: {}"
LOG_MESSAGE_FAILED = "Error sending message to SQS: {}"
