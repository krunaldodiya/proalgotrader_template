# ProAlgoTrader

https://www.proalgotrader.com

```
This is a default template for ProAlgoTrader strategy.

To get started, follow simple step given below.
```

### Step 1

Clone strategy

```bash
git clone <PROJECT_REPOSITORY_URL> <PROJECT_DIRECTORY>
```

You can find your PROJECT_REPOSITORY_URL from ProAlgoTrader Project Dashboard.

### Step 2

Create and activate virtual environment

```bash
cd <PROJECT_DIRECTORY>

python -m venv .venv

source .venv/bin/activate
```

### Step 3

Install required packages

```bash
pip install -r requirements.txt
```

### Step 4

Run strategy

```bash
docker-compose up <ENVIRONMENT>

# for development environment
docker-compose up development

# for production environment
docker-compose up production
```
