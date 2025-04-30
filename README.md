# Launch Pad – Streaming Data Pipeline

This is a Python-based data streaming application that fetches the latest news articles from The Guardian API and publishes them to an AWS SQS queue. It is designed to demonstrate real-time data collection and messaging using a cloud-native approach.

## 📦 Features

- Retrieves articles from The Guardian based on search terms.
- Publishes article data to an AWS SQS queue in JSON format.
- Robust error handling and retry configuration using `botocore`.
- Includes testing with `pytest`, `moto`, and `unittest.mock`.
- Continuous Integration with GitHub Actions.

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Abbeygold/launch-pad-data_streaming.git
cd launch-pad-data_streaming
```

### 2. Set up Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
export PYTHONPATH=$(pwd)
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 4. Set up Environment Variables

Create a `.env` file:

Edit the `.env` file with your API key and AWS details.

```
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=your_aws_region
SQS_QUEUE_URL=your_sqs_queue_url
GUARDIAN_API_KEY=your_guardian_api_key
```

### 5. Run the Application

```bash
python src/main.py "search term" --date_from 2023-01-01    # with an optional date from
python src/main.py "search term" # without a date
```

## Testing

To run the tests:

```bash
make test
```

To check linting and formatting:

```bash
make lint
make format
```

## ⚙️ Makefile Commands

| Command         | Description                  |
| --------------- | ---------------------------- |
| `make install`  | Install dependencies         |
| `make test`     | Run tests                    |
| `make lint`     | Run flake8 on source code    |
| `make format`   | Auto-format with black       |
| `make security` | Run security checks (bandit) |
| `make clean`    | Remove `.pyc` and temp files |

## 📂 Project Structure

```
.
├── src/
│   ├── main.py
│   ├── guardian_api.py
│   ├── sqs_publisher.py
│   └── aws_config.py
├── tests/
│   └── test_guardian_api.py
│   └── test_sqs_publisher.py
├── requirements.txt
├── requirements-dev.txt
├── Makefile
├── .env.example
└── README.md
```
