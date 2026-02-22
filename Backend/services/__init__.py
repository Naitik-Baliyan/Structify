"""
Structify Backend Services Package

Modular service layer for business analysis and AI integration.
"""

from .ai_engine import (
    AIEngine,
    generate_analysis_response,
    SuggestionGenerator,
    RiskClassifier,
    DomainTagger,
    InputValidator
)

from .brd_generator import (
    BRDGenerator,
    BRDExporter,
    BRDFormatter,
    generate_brd
)

__all__ = [
    "AIEngine",
    "generate_analysis_response",
    "SuggestionGenerator",
    "RiskClassifier",
    "DomainTagger",
    "InputValidator",
    "BRDGenerator",
    "BRDExporter",
    "BRDFormatter",
    "generate_brd"
]
