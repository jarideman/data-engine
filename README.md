# Setup

Run `pip install -r requirements.txt`

run `python main.py`


## Core
- [x] Connect to MT5
- [ ] Receive tick data
- [ ] Receive OHLC/candle data
- [ ] Normalize market data
- [ ] Validate incoming data
- [ ] Detect missing, duplicate and out-of-order data
- [ ] Track bid, ask, spread and volume
- [ ] Manage symbols
- [ ] Handle trading sessions and timezones

## Candle Engine
- [ ] Build candles from ticks
- [ ] Support multiple timeframes
- [ ] Update live candles
- [ ] Emit candle-closed events
- [ ] Keep live and backtest candle generation identical

## Storage
- [ ] Connect to postgresql db
- [ ] Store raw tick data
- [ ] Store historical candles
- [ ] Store symbol information

## API
- [ ] Get latest market data
- [ ] Get historical candles
- [x] Get symbol information
- [ ] Get data/feed status
- [x] Get open/closed positions
