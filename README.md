# ProAlgoTrader Strategy Template

<div align="center">
  <a href="https://www.proalgotrader.com">
    <img src="https://www.proalgotrader.com/assets/images/logo.png" alt="ProAlgoTrader" width="200">
  </a>
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

> 🔑 Get your session credentials from [ProAlgoTrader Dashboard](https://www.proalgotrader.com/dashboard)

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

- 📚 [Documentation](https://www.proalgotrader.com/docs)
- 💬 [Community Forum](https://www.proalgotrader.com/forum)
- 📧 [Support Email](mailto:support@proalgotrader.com)

## License

This template is provided as part of your ProAlgoTrader subscription.
