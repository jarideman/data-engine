# Setup

### 1. Create virtual environment
```bash
python -m venv venv
```

### 2. Activate virtual environment
**Windows:**
```bash
venv\Scripts\activate
```

**Linux / macOS:**
```bash
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
**Windows:**
```bash
copy .env.example .env
```

**Linux / macOS:**
```bash
cp .env.example .env
```

Fill/update the variables in `.env`.

### 5. Start the data engine
```bash
python main.py
```

### 6. Start the API
```bash
python -m uvicorn main:app --app-dir api --host 127.0.0.1 --port 8000
```


## Core
- [x] Connect to MT5
- [ ] Receive tick data
- [ ] Receive OHLC/candle data
- [ ] Normalize market data
- [ ] Validate incoming data
- [ ] Detect missing, duplicate and out-of-order data
- [ ] Track bid, ask, spread and volume

## Candle Engine
- [ ] Build candles from ticks
- [ ] Support multiple timeframes
- [ ] Update live candles
- [ ] Emit candle-closed events
- [ ] Keep live and backtest candle generation identical

## Storage
- [x] Connect to PostgreSQL db
- [ ] Store raw tick data
- [ ] Store historical candles
- [ ] Store symbol information

## API
- [ ] Get latest market data
- [ ] Get historical candles
- [x] Get symbol information
- [ ] Get data/feed status
- [x] Get open/closed positions
