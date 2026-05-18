# 📊 DeFiSense AI

> Multi-Agent DeFi Analytics & On-Chain Intelligence Platform powered by MiMo AI

---

## Overview

DeFiSense AI is a real-time decentralized finance analytics engine that leverages **MiMo-V2.5-Pro** long-chain reasoning to process on-chain data, detect trading signals, assess liquidity risks, and generate actionable investment intelligence — across Ethereum, BSC, and Arbitrum simultaneously.

Built for serious DeFi participants who need institutional-grade insights without institutional-grade subscriptions.

---

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                        DeFiSense AI                          │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────────┐ │
│  │  On-Chain   │  │  Sentiment  │  │  Liquidity & Pool    │ │
│  │  Signal     │  │  Analysis   │  │  Health Monitor      │ │
│  │  Agent      │  │  Agent      │  │  Agent               │ │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬───────────┘ │
│         │                │                     │             │
│  ┌──────┴────────────────┴─────────────────────┴───────────┐ │
│  │              Agent Orchestrator (Hermes)                 │ │
│  │         Context-Aware Multi-Agent Coordinator           │ │
│  └─────────────────────────┬────────────────────────────── ┘ │
│                            │                                  │
│  ┌─────────────────────────┴────────────────────────────── ┐ │
│  │              MiMo-V2.5-Pro API                           │ │
│  │          (Deep Reasoning + Long Chain CoT)               │ │
│  └──────────────────────────────────────────────────────── ┘ │
│                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────────┐ │
│  │  Portfolio  │  │  Risk       │  │  Multi-Chain         │ │
│  │  Optimizer  │  │  Scoring    │  │  Data Layer          │ │
│  │  Agent      │  │  Agent      │  │  (Eth/BSC/Arbitrum)  │ │
│  └─────────────┘  └─────────────┘  └──────────────────────┘ │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## Token Consumption Model

Each agent runs continuous or event-driven inference using **MiMo-V2.5-Pro** for reasoning and **MiMo-V2.5** for lighter classification tasks.

| Agent | Model | Tokens/Operation | Frequency | Daily/User |
|---|---|---|---|---|
| On-Chain Signal Agent | MiMo-V2.5-Pro | 1.2M | 12×/day | 14.4M |
| Sentiment Analysis Agent | MiMo-V2.5 | 350K | Continuous (48×/day) | 16.8M |
| Liquidity Monitor Agent | MiMo-V2.5-Pro | 800K | 24×/day | 19.2M |
| Portfolio Optimizer | MiMo-V2.5-Pro | 950K | 6×/day | 5.7M |
| Risk Scoring Agent | MiMo-V2.5 | 200K | 30×/day | 6M |
| Report & Alert Generator | MiMo-V2.5 | 400K | 8×/day | 3.2M |
| **Total** | | | | **~65.3M/day** |

At 200 active users: **~13B tokens/day → ~390B/month**

This is why we're applying for MiMo API credits — our per-user token consumption is high by design. Deep reasoning on financial data cannot be approximate.

---

## Tech Stack

- **AI Models:** MiMo-V2.5-Pro (reasoning, portfolio), MiMo-V2.5 (sentiment, risk)
- **Agent Framework:** Hermes Agent Orchestrator
- **IDE:** Cursor + Claude Code
- **Data Sources:** Etherscan, BSCScan, Arbiscan, DeFiLlama, CoinGecko APIs
- **Backend:** Python (FastAPI) + Node.js event listeners
- **Database:** TimescaleDB (time-series) + Redis (cache)
- **Queue:** RabbitMQ for agent task routing
- **Deploy:** Docker + Kubernetes (GCP)
- **Frontend:** React + TailwindCSS real-time dashboard

---

## Core Features

### 🔍 On-Chain Signal Detection
- Whale wallet movement alerts (>$500K transactions)
- DEX arbitrage opportunity scanner
- Token unlock schedule tracker with price impact prediction

### 📈 Sentiment Intelligence
- Real-time crypto Twitter/X sentiment parsing
- Discord & Telegram community signal extraction
- Fear & Greed index correlation with on-chain activity

### 💧 Liquidity Health Monitor
- Uniswap V3 / Curve / Balancer pool depth analysis
- Impermanent loss calculator with MiMo-powered scenario modeling
- Rug risk scoring for new pools (< 30 days old)

### 🧠 Portfolio Optimization
- Multi-asset rebalancing suggestions based on risk tolerance
- Gas-optimized execution routing
- Historical backtest with MiMo reasoning on market regimes

---

## Roadmap

- [x] Architecture design & agent spec
- [x] MiMo API integration prototype
- [ ] On-Chain Signal Agent — MVP (in progress)
- [ ] Sentiment Agent — training data pipeline
- [ ] Liquidity Monitor — real-time WebSocket feeds
- [ ] Public beta — 500 waitlist users ready
- [ ] Production scale (pending MiMo API credits)

---

## Why MiMo?

We evaluated GPT-4o, Claude 3.5, and Gemini Pro. MiMo-V2.5-Pro's **long-chain reasoning** is uniquely suited for DeFi analysis because:

1. DeFi decisions require multi-step causal chains (price → liquidity → sentiment → action)
2. MiMo handles 200K+ context windows — essential for processing full transaction histories
3. Reasoning traces let us audit *why* an agent made a recommendation
4. Cost efficiency at scale vs. alternatives

---

## Status

🚧 Active development — seeking MiMo API credits to scale from prototype to production.

> Built with Cursor + Claude Code. Agent orchestration logic in `/src/agents/`. API integration in `/src/mimo_client/`.

---

## License

MIT
