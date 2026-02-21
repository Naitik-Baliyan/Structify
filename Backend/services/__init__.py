"""
Structify Backend Services Package

Modular service layer for business analysis and AI integration.
"""

from .ai_engine import (
    AIEngine,
    generate_analysis_response,
    SuggestionGenerator,
    RiskClassifier,
    DomainTagger
)

from .brd_generator import (
    BRDGenerator,
    BRDExporter,
    generate_brd
)

__all__ = [
    "AIEngine",
    "generate_analysis_response",
    "SuggestionGenerator",
    "RiskClassifier",
    "DomainTagger",
    "BRDGenerator",
    "BRDExporter",
    "generate_brd"
]
