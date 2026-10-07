## Core
- [x] Connect to MT5
- [ ] Receive tick data
- [ ] Receive OHLC/candle data
- [ ] Normalize market data
- [ ] Validate incoming data
- [ ] Detect missing, duplicate and out-of-order data
- [ ] Track bid, ask, spread and volume
- [ ] Manage instruments/symbols
- [ ] Handle trading sessions and timezones

## Candle Engine
- [ ] Build candles from ticks
- [ ] Support multiple timeframes
- [ ] Update live candles
- [ ] Emit candle-closed events
- [ ] Keep live and backtest candle generation identical

## Storage
- [ ] Store raw tick data
- [ ] Store historical candles
- [ ] Store instrument information
- [ ] Query historical data efficiently
- [ ] Cache recent/current market data

## Events
- [ ] `TickReceived`
- [ ] `CandleUpdated`
- [ ] `CandleClosed`
- [ ] `MarketOpened`
- [ ] `MarketClosed`
- [ ] `DataGapDetected`
- [ ] `FeedDisconnected`

## Backtesting
- [ ] Historical data replay
- [ ] Live/backtest compatible interface
- [ ] Configurable replay speed
- [ ] Deterministic replay
- [ ] Prevent look-ahead bias

## API
- [ ] Get latest market data
- [ ] Get historical candles
- [ ] Subscribe to market events
- [ ] Get instrument information
- [ ] Get data/feed status

## Monitoring
- [ ] Track feed connection
- [ ] Track data latency
- [ ] Track data gaps
- [ ] Track invalid data
- [ ] Track processing errors
