"""
情绪分析服务 — MVP 阶段使用简化实现。
FinBERT 模型加载耗时且体积大，MVP 阶段返回默认情绪值。
后续集成 ProsusAI/finbert 只需替换 analyze_sentiment() 函数。
"""


async def analyze_sentiment(text: str) -> dict:
    """
    分析文本情绪。
    MVP: 基于关键词的简单分析
    后续: 集成 ProsusAI/finbert 替换此函数
    """
    if not text:
        return {"score": 0.0, "label": "neutral"}

    text_lower = text.lower()
    bullish_words = ["bullish", "buy", "growth", "upgrade", "beat", "upside", "strong", "outperform", "positive", "金叉", "买入", "看好"]
    bearish_words = ["bearish", "sell", "decline", "downgrade", "miss", "downside", "weak", "underperform", "negative", "死叉", "卖出", "看空"]

    bull_count = sum(1 for w in bullish_words if w in text_lower)
    bear_count = sum(1 for w in bearish_words if w in text_lower)

    if bull_count > bear_count:
        return {"score": 0.3 + min(bull_count * 0.1, 0.4), "label": "bullish"}
    elif bear_count > bull_count:
        return {"score": -0.3 - min(bear_count * 0.1, 0.4), "label": "bearish"}
    return {"score": 0.0, "label": "neutral"}
