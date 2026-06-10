"""
FinBERT 情绪分析封装。
MVP: 使用关键词分析
生产: 集成 transformers 加载 ProsusAI/finbert
"""

from app.services.sentiment_service import analyze_sentiment

# Re-export for convenience
__all__ = ["analyze_sentiment"]
