"""
DeFiSense AI - Agent Orchestrator (Hermes)
Multi-agent coordinator for on-chain DeFi intelligence
"""

import asyncio
import logging
from dataclasses import dataclass
from typing import Any

import httpx

logger = logging.getLogger(__name__)

MIMO_API_BASE = "https://api.xiaomimimo.com/v1"
MIMO_MODEL_PRO = "mimo-v2.5-pro"
MIMO_MODEL_BASE = "mimo-v2.5"


@dataclass
class AgentTask:
    agent_name: str
    task_type: str
    payload: dict
    priority: int = 1  # 1=high, 2=medium, 3=low


@dataclass
class AgentResult:
    agent_name: str
    success: bool
    data: Any
    token_usage: int
    reasoning_trace: str | None = None


class MiMoClient:
    """Async client for MiMo API with retry logic."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = httpx.AsyncClient(
            base_url=MIMO_API_BASE,
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=120.0,
        )

    async def complete(
        self,
        prompt: str,
        model: str = MIMO_MODEL_PRO,
        max_tokens: int = 4096,
        system: str | None = None,
    ) -> dict:
        messages = [{"role": "user", "content": prompt}]
        body = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "stream": False,
        }
        if system:
            body["system"] = system

        for attempt in range(3):
            try:
                resp = await self.client.post("/chat/completions", json=body)
                resp.raise_for_status()
                return resp.json()
            except httpx.HTTPStatusError as e:
                logger.warning(f"MiMo API error (attempt {attempt+1}): {e}")
                if attempt == 2:
                    raise
                await asyncio.sleep(2 ** attempt)

    async def close(self):
        await self.client.aclose()


class OnChainSignalAgent:
    """
    Detects whale movements, arbitrage signals, and token unlock events.
    Uses MiMo-V2.5-Pro for multi-step causal chain reasoning.
    """

    def __init__(self, mimo: MiMoClient):
        self.mimo = mimo
        self.name = "OnChainSignalAgent"

    async def analyze(self, chain: str, block_data: dict) -> AgentResult:
        prompt = f"""
You are an expert DeFi on-chain analyst. Analyze the following blockchain data and identify:
1. Whale wallet movements (>$500K)
2. DEX arbitrage opportunities
3. Unusual token flow patterns
4. Token unlock events and expected price impact

Chain: {chain}
Block data summary: {block_data}

Provide a structured analysis with:
- Signal type and confidence score (0-100)
- Estimated price impact
- Recommended action (buy/sell/watch/avoid)
- Reasoning chain (step by step)
"""
        system = (
            "You are DeFiSense AI's on-chain signal detection engine. "
            "Think step by step. Be precise with numbers. Flag high-risk signals clearly."
        )

        result = await self.mimo.complete(prompt, model=MIMO_MODEL_PRO, system=system)
        tokens_used = result.get("usage", {}).get("total_tokens", 0)
        content = result["choices"][0]["message"]["content"]

        return AgentResult(
            agent_name=self.name,
            success=True,
            data={"raw_analysis": content, "chain": chain},
            token_usage=tokens_used,
            reasoning_trace=content,
        )


class SentimentAgent:
    """
    Processes social media signals from X/Twitter, Discord, Telegram.
    Uses MiMo-V2.5 (lighter) for high-frequency sentiment classification.
    """

    def __init__(self, mimo: MiMoClient):
        self.mimo = mimo
        self.name = "SentimentAgent"

    async def analyze(self, token_symbol: str, social_data: list[str]) -> AgentResult:
        combined_text = "\n".join(social_data[:50])  # cap at 50 posts
        prompt = f"""
Analyze the following social media posts about {token_symbol}.

Posts:
{combined_text}

Return JSON with:
- sentiment_score: float between -1.0 (bearish) and 1.0 (bullish)
- dominant_narrative: string (1-2 sentences)
- key_concerns: list of strings
- momentum: "rising" | "falling" | "neutral"
- confidence: float 0-1
"""
        result = await self.mimo.complete(
            prompt, model=MIMO_MODEL_BASE, max_tokens=1024
        )
        tokens_used = result.get("usage", {}).get("total_tokens", 0)
        content = result["choices"][0]["message"]["content"]

        return AgentResult(
            agent_name=self.name,
            success=True,
            data={"raw": content, "token": token_symbol},
            token_usage=tokens_used,
        )


class LiquidityMonitorAgent:
    """
    Monitors DEX pool health: depth, IL risk, rug scoring.
    Uses MiMo-V2.5-Pro for scenario modeling.
    """

    def __init__(self, mimo: MiMoClient):
        self.mimo = mimo
        self.name = "LiquidityMonitorAgent"

    async def analyze(self, pool_data: dict) -> AgentResult:
        prompt = f"""
Analyze this DeFi liquidity pool and assess its health and risk:

Pool data: {pool_data}

Provide:
1. Liquidity depth score (0-100)
2. Impermanent loss estimate for 24h, 7d, 30d under 3 price scenarios
3. Rug risk score (0-100) with reasoning
4. LP yield sustainability assessment
5. Recommended action for LPs: add/remove/hold/avoid
"""
        result = await self.mimo.complete(
            prompt, model=MIMO_MODEL_PRO, system="You are a DeFi liquidity expert."
        )
        tokens_used = result.get("usage", {}).get("total_tokens", 0)
        content = result["choices"][0]["message"]["content"]

        return AgentResult(
            agent_name=self.name,
            success=True,
            data={"analysis": content, "pool": pool_data.get("address")},
            token_usage=tokens_used,
            reasoning_trace=content,
        )


class HermesOrchestrator:
    """
    Central coordinator for all DeFiSense AI agents.
    Routes tasks, aggregates results, generates final reports.
    """

    def __init__(self, api_key: str):
        self.mimo = MiMoClient(api_key)
        self.agents = {
            "signal": OnChainSignalAgent(self.mimo),
            "sentiment": SentimentAgent(self.mimo),
            "liquidity": LiquidityMonitorAgent(self.mimo),
        }
        self.total_tokens_used = 0

    async def run_full_analysis(
        self,
        token_symbol: str,
        chain: str,
        block_data: dict,
        social_posts: list[str],
        pool_data: dict,
    ) -> dict:
        """Run all agents in parallel and synthesize results."""
        logger.info(f"Starting full DeFiSense analysis for {token_symbol} on {chain}")

        tasks = await asyncio.gather(
            self.agents["signal"].analyze(chain, block_data),
            self.agents["sentiment"].analyze(token_symbol, social_posts),
            self.agents["liquidity"].analyze(pool_data),
            return_exceptions=True,
        )

        results = {}
        for task in tasks:
            if isinstance(task, AgentResult):
                results[task.agent_name] = task
                self.total_tokens_used += task.token_usage

        # Synthesis pass â MiMo-Pro aggregates all agent outputs
        synthesis_prompt = f"""
You are the DeFiSense AI master analyst. Synthesize these agent reports into a final investment brief:

On-Chain Signals: {results.get('OnChainSignalAgent', {}).data if 'OnChainSignalAgent' in results else 'unavailable'}
Sentiment: {results.get('SentimentAgent', {}).data if 'SentimentAgent' in results else 'unavailable'}
Liquidity: {results.get('LiquidityMonitorAgent', {}).data if 'LiquidityMonitorAgent' in results else 'unavailable'}

Token: {token_symbol} | Chain: {chain}

Output a concise investment brief: overall signal, risk level, confidence, and 1-paragraph recommendation.
"""
        final = await self.mimo.complete(synthesis_prompt, model=MIMO_MODEL_PRO)
        self.total_tokens_used += final.get("usage", {}).get("total_tokens", 0)

        return {
            "token": token_symbol,
            "chain": chain,
            "agent_results": {k: v.data for k, v in results.items()},
            "final_brief": final["choices"][0]["message"]["content"],
            "total_tokens_used": self.total_tokens_used,
        }

    async def close(self):
        await self.mimo.close()


async def main():
    import os

    orchestrator = HermesOrchestrator(api_key=os.getenv("MIMO_API_KEY", ""))

    # Example run
    result = await orchestrator.run_full_analysis(
        token_symbol="ARB",
        chain="arbitrum",
        block_data={"latest_block": 12345678, "whale_txns": [], "dex_volume_24h": 0},
        social_posts=["ARB looking bullish today", "Arbitrum TVL just hit ATH"],
        pool_data={"address": "0xabc...", "tvl": 5_000_000, "age_days": 45},
    )

    print(result["final_brief"])
    print(f"Total tokens used: {result['total_tokens_used']:,}")
    await orchestrator.close()


if __name__ == "__main__":
    asyncio.run(main())
