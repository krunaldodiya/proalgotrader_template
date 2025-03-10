# ProAlgoTrader Strategy Template

<div align="center">
  <h1>📊</h1>
  <h3>Professional Algorithmic Trading Made Simple</h3>
</div>

## Overview

This is the official template for creating ProAlgoTrader strategies. It provides a structured foundation for developing and deploying your trading algorithms.

## Quick Start Guide

### 1. Environment Setup

First, create your environment configuration:

```bash
# Copy the example environment file
cp .env.example .env
```

Then edit `.env` file and update these essential values:
```ini
ALGO_SESSION_KEY=your_session_key
ALGO_SESSION_SECRET=your_session_secret
```

> 🔑 Get your session credentials from ProAlgoTrader Dashboard

### 2. Running Your Strategy

You can run your strategy in two environments:

#### Development Mode
```bash
python main.py --environment development
```
- Uses development credentials
- Enables detailed logging
- Perfect for testing and debugging

#### Production Mode
```bash
python main.py --environment production
```
- Uses production credentials
- Optimized performance
- For live trading

## Strategy Development

### Key Files
- `main.py` - Entry point for your strategy
- `.env` - Environment configuration
- `requirements.txt` - Python dependencies

### Best Practices
1. Always test in development mode first
2. Keep your credentials secure
3. Regularly backup your strategy
4. Monitor logs for performance

## Support

- 📚 Documentation
- 💬 Community Forum
- 📧 support@proalgotrader.com

## License

This template is provided as part of your ProAlgoTrader subscription.
