# Order Book Spoof Simulator

A live terminal-based order book simulator that demonstrates how spoof trading works and why it's detectable.

## Requirements

```bash
uv add rich sortedcontainers
```

## Run

```bash
python main.py
```

## Controls

| Key | Action |
|-----|--------|
| `B` | Inject BUY spoof wall |
| `S` | Inject SELL spoof wall |
| `C` | Cancel spoof |
| `SPACE` | Step simulation |
| `Q` | Quit |

## How It Works

1. **Real-time order book** - See bids/asks update continuously
2. **Inject spoof** - Press B or S to place a large (10-20x normal) order
3. **Watch price react** - Market moves toward the spoof "liquidity"
4. **Cancel spoof** - Press C to remove it instantly
5. **Detection explains why** - The panel shows how spoofing is detected

## Spoof Detection Signals

- **Volume anomaly** - Spoof orders are 10-20x larger than normal
- **Price immobile** - Spoof never executes, price retreats
- **Temporal pattern** - Appears → price moves → vanishes (2-10s)
- **Layering** - Creates wall to push price, cancels when it moves
