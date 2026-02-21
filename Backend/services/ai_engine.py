"""
AI Engine Service Layer for Structify Backend

Handles:
- External AI API integration (Gemini/OpenAI)
- Suggestion generation
- Risk classification
- Domain tagging
- Heuristic fallback for MVP
"""

import os
import json
import logging
import asyncio
from typing import Dict, List, Optional
from datetime import datetime

# Configure logger
logger = logging.getLogger(__name__)


class AIEngine:
    """Main AI processing service"""
    
    def __init__(self, api_key: str, api_provider: str = "gemini", timeout: int = 30):
        self.api_key = api_key
        self.api_provider = api_provider
        self.timeout = timeout
        logger.info(f"AIEngine initialized with provider: {api_provider}")
    
    async def generate_analysis_response(
        self,
        idea: str,
        target_market: str,
        problem_statement: str
    ) -> Dict:
        """
        Generate structured business analysis response
        
        Args:
            idea: Business idea description
            target_market: Target market description
            problem_statement: Problem the idea solves
            
        Returns:
            Dict with analysis, scores, suggestions, risk_level, and domain_tags
        """
        
        logger.info(f"Generating analysis for idea: {idea[:50]}...")
        
        try:
            # Try external API first
            if self.api_key:
                response = await self._call_external_ai(idea, target_market, problem_statement)
                if response:
                    logger.info("Successfully generated analysis via external API")
                    return response
        except Exception as e:
            logger.warning(f"External API call failed: {str(e)}. Falling back to heuristics.")
        
        # Fallback to heuristic-based analysis
        logger.info("Using heuristic-based analysis")
        return self._generate_heuristic_analysis(idea, target_market, problem_statement)
    
    async def _call_external_ai(
        self,
        idea: str,
        target_market: str,
        problem_statement: str
    ) -> Optional[Dict]:
        """
        Call external AI API (Gemini or OpenAI)
        
        Args:
            idea: Business idea
            target_market: Target market
            problem_statement: Problem statement
            
        Returns:
            Structured analysis response or None if failed
        """
        
        try:
            if self.api_provider == "gemini":
                return await self._call_gemini_api(idea, target_market, problem_statement)
            elif self.api_provider == "openai":
                return await self._call_openai_api(idea, target_market, problem_statement)
        except asyncio.TimeoutError:
            logger.error("API call timed out")
            raise
        except Exception as e:
            logger.error(f"API call error: {str(e)}")
            raise
    
    async def _call_gemini_api(
        self,
        idea: str,
        target_market: str,
        problem_statement: str
    ) -> Dict:
        """Call Google Gemini API"""
        
        try:
            import google.generativeai as genai
            
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel("gemini-pro")
            
            prompt = f"""
            Analyze this business idea and provide structured feedback in JSON format.
            
            BUSINESS IDEA: {idea}
            TARGET MARKET: {target_market}
            PROBLEM STATEMENT: {problem_statement}
            
            Respond with ONLY valid JSON (no markdown, no code blocks):
            {{
                "analysis": "2-3 paragraph detailed business analysis",
                "compatibility_score": 75,
                "improvement_suggestions": ["suggestion 1", "suggestion 2", "suggestion 3"],
                "risk_level": "medium",
                "domain_tags": ["tech", "saas", "b2b"]
            }}
            """
            
            # Set timeout
            response = await asyncio.wait_for(
                asyncio.to_thread(model.generate_content, prompt),
                timeout=self.timeout
            )
            
            # Parse response
            response_text = response.text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            result = json.loads(response_text)
            logger.info("Gemini API response parsed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
            raise
    
    async def _call_openai_api(
        self,
        idea: str,
        target_market: str,
        problem_statement: str
    ) -> Dict:
        """Call OpenAI API"""
        
        try:
            import aiohttp
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {
                        "role": "user",
                        "content": f"""
                        Analyze this business idea and provide structured feedback in JSON format.
                        
                        BUSINESS IDEA: {idea}
                        TARGET MARKET: {target_market}
                        PROBLEM STATEMENT: {problem_statement}
                        
                        Respond with ONLY valid JSON:
                        {{
                            "analysis": "2-3 paragraph detailed business analysis",
                            "compatibility_score": 75,
                            "improvement_suggestions": ["suggestion 1", "suggestion 2", "suggestion 3"],
                            "risk_level": "medium",
                            "domain_tags": ["tech", "saas", "b2b"]
                        }}
                        """
                    }
                ]
            }
            
            async with aiohttp.ClientSession() as session:
                async with asyncio.timeout(self.timeout):
                    async with session.post(
                        "https://api.openai.com/v1/chat/completions",
                        json=payload,
                        headers=headers
                    ) as resp:
                        data = await resp.json()
                        response_text = data["choices"][0]["message"]["content"]
                        result = json.loads(response_text)
                        logger.info("OpenAI API response parsed successfully")
                        return result
                        
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise
    
    def _generate_heuristic_analysis(
        self,
        idea: str,
        target_market: str,
        problem_statement: str
    ) -> Dict:
        """
        Generate analysis using heuristic rules (MVP fallback)
        
        Args:
            idea: Business idea
            target_market: Target market
            problem_statement: Problem statement
            
        Returns:
            Dict with heuristic-based analysis
        """
        
        # Calculate compatibility score based on keyword matching
        compatibility_score = self._calculate_compatibility_score(
            idea, target_market, problem_statement
        )
        
        # Generate improvement suggestions
        suggestions = SuggestionGenerator.generate(
            idea, target_market, problem_statement
        )
        
        # Classify risk
        risk_level = RiskClassifier.classify(
            idea, target_market, problem_statement
        )
        
        # Extract domain tags
        domain_tags = DomainTagger.extract_tags(
            idea, target_market, problem_statement
        )
        
        analysis_text = f"""
        Your idea '{idea}' targets the {target_market} market by solving: {problem_statement}.
        
        This concept shows potential for addressing market gaps. The business model aligns with current market trends
        and has identifiable customer segments. Success will depend on execution quality and competitive differentiation.
        
        Consider the suggestions below to strengthen your value proposition and market positioning.
        """.strip()
        
        return {
            "analysis": analysis_text,
            "compatibility_score": compatibility_score,
            "improvement_suggestions": suggestions,
            "risk_level": risk_level,
            "domain_tags": domain_tags
        }
    
    def _calculate_compatibility_score(
        self,
        idea: str,
        target_market: str,
        problem_statement: str
    ) -> int:
        """
        Calculate compatibility score using heuristics
        
        Args:
            idea: Business idea
            target_market: Target market
            problem_statement: Problem statement
            
        Returns:
            Compatibility score (0-100)
        """
        
        score = 60  # Base score
        combined_text = f"{idea} {target_market} {problem_statement}".lower()
        
        # Positive keywords
        positive_keywords = [
            "innovative", "efficient", "sustainable", "scalable", "digital",
            "automation", "ai", "machine learning", "market gap", "competitive advantage",
            "revenue model", "customer acquisition", "growth potential"
        ]
        
        for keyword in positive_keywords:
            if keyword in combined_text:
                score += 3
        
        # Negative keyword penalties
        negative_keywords = [
            "maybe", "unclear", "not sure", "limited market", "unknown", "vague"
        ]
        
        for keyword in negative_keywords:
            if keyword in combined_text:
                score -= 5
        
        # Length bonus (completeness)
        if len(problem_statement) > 50:
            score += 5
        if len(target_market) > 30:
            score += 5
        
        return min(max(score, 20), 100)  # Clamp between 20 and 100


class SuggestionGenerator:
    """Generate startup improvement suggestions"""
    
    SUGGESTION_TEMPLATES = {
        "market": [
            "Conduct deeper market research - map competitor pricing and positioning strategies",
            "Define your total addressable market (TAM) and initial serviceable market (SAM)",
            "Identify early adopter segments within your target market for faster validation"
        ],
        "product": [
            "Develop a minimum viable product (MVP) to validate core assumptions",
            "Create a product roadmap with clear milestones and feature prioritization",
            "Build customer feedback loops early to inform product development"
        ],
        "business": [
            "Establish clear unit economics and path to profitability",
            "Define your revenue model and pricing strategy",
            "Identify key partnerships or channels for customer acquisition"
        ],
        "execution": [
            "Assemble a founding team with complementary skills",
            "Set measurable KPIs to track progress and pivot points",
            "Plan your funding strategy (bootstrapping, angel, VC) and timeline"
        ]
    }
    
    @staticmethod
    def generate(idea: str, target_market: str, problem_statement: str) -> List[str]:
        """
        Generate 3-5 suggestions based on the business idea
        
        Args:
            idea: Business idea
            target_market: Target market
            problem_statement: Problem statement
            
        Returns:
            List of 3-5 suggestions
        """
        
        suggestions = []
        combined_text = f"{idea} {target_market} {problem_statement}".lower()
        categories = []
        
        # Determine relevant suggestion categories
        if any(word in combined_text for word in ["market", "customer", "user"]):
            categories.append("market")
        if any(word in combined_text for word in ["product", "solution", "service"]):
            categories.append("product")
        if any(word in combined_text for word in ["revenue", "business", "model", "profit"]):
            categories.append("business")
        if any(word in combined_text for word in ["team", "founder", "build", "develop"]):
            categories.append("execution")
        
        # Default to all categories if nothing matched
        if not categories:
            categories = list(SuggestionGenerator.SUGGESTION_TEMPLATES.keys())
        
        # Select up to 5 suggestions
        import random
        for category in categories[:4]:
            suggestion = random.choice(SuggestionGenerator.SUGGESTION_TEMPLATES[category])
            suggestions.append(suggestion)
        
        return suggestions[:5]


class RiskClassifier:
    """Classify business idea risk level"""
    
    @staticmethod
    def classify(idea: str, target_market: str, problem_statement: str) -> str:
        """
        Classify risk level as: low, medium, high, critical
        
        Args:
            idea: Business idea
            target_market: Target market
            problem_statement: Problem statement
            
        Returns:
            Risk level string
        """
        
        risk_score = 0
        combined_text = f"{idea} {target_market} {problem_statement}".lower()
        
        # High-risk indicators
        high_risk_keywords = [
            "unproven", "speculative", "no market", "impossible", "untested",
            "blockchain", "cryptocurrency", "highly regulated"
        ]
        
        for keyword in high_risk_keywords:
            if keyword in combined_text:
                risk_score += 3
        
        # Medium-risk indicators
        medium_risk_keywords = [
            "competitive", "new technology", "emerging market", "depends on",
            "requires permission", "patent pending"
        ]
        
        for keyword in medium_risk_keywords:
            if keyword in combined_text:
                risk_score += 1
        
        # Low-risk indicators (reduce score)
        low_risk_keywords = [
            "proven", "established", "existing market", "validated", "customer",
            "revenue", "profitable", "sustainable"
        ]
        
        for keyword in low_risk_keywords:
            if keyword in combined_text:
                risk_score -= 2
        
        # Classify based on score
        if risk_score >= 5:
            return "high"
        elif risk_score >= 2:
            return "medium"
        else:
            return "low"


class DomainTagger:
    """Extract domain and industry tags"""
    
    DOMAIN_KEYWORDS = {
        "tech": ["software", "app", "cloud", "data", "ai", "machine learning", "saas", "platform"],
        "fintech": ["payment", "banking", "crypto", "investment", "insurance", "lending"],
        "healthcare": ["medical", "health", "doctor", "patient", "therapy", "diagnosis"],
        "ecommerce": ["retail", "shopping", "store", "marketplace", "product", "sell"],
        "education": ["learning", "course", "student", "school", "training", "skill"],
        "social": ["community", "social", "network", "platform", "interaction", "engagement"],
        "logistics": ["shipping", "delivery", "supply chain", "warehouse", "transport"],
        "energy": ["renewable", "solar", "wind", "battery", "electric", "sustainable"],
        "environment": ["climate", "sustainability", "green", "eco", "carbon", "waste"],
        "entertainment": ["gaming", "streaming", "music", "video", "entertainment", "content"],
        "b2b": ["enterprise", "business", "b2b", "saas", "consulting"],
        "b2c": ["consumer", "b2c", "retail", "direct to consumer", "marketplace"]
    }
    
    @staticmethod
    def extract_tags(idea: str, target_market: str, problem_statement: str) -> List[str]:
        """
        Extract relevant domain tags
        
        Args:
            idea: Business idea
            target_market: Target market
            problem_statement: Problem statement
            
        Returns:
            List of domain tags
        """
        
        tags = set()
        combined_text = f"{idea} {target_market} {problem_statement}".lower()
        
        # Match keywords to domains
        for domain, keywords in DomainTagger.DOMAIN_KEYWORDS.items():
            for keyword in keywords:
                if keyword in combined_text:
                    tags.add(domain)
                    break
        
        # Default tags if no match
        if not tags:
            tags.add("tech")  # Default assumption
            tags.add("b2b" if "enterprise" in combined_text or "business" in combined_text else "b2c")
        
        return sorted(list(tags))[:6]  # Return max 6 tags


# Utility function for synchronous wrapper
def generate_analysis_response(
    idea: str,
    target_market: str,
    problem_statement: str,
    api_key: Optional[str] = None,
    api_provider: str = "gemini",
    timeout: int = 30
) -> Dict:
    """
    Synchronous wrapper for analysis generation
    
    Args:
        idea: Business idea
        target_market: Target market
        problem_statement: Problem statement
        api_key: API key for external service
        api_provider: API provider (gemini or openai)
        timeout: Request timeout in seconds
        
    Returns:
        Dict with complete analysis response
    """
    
    engine = AIEngine(api_key, api_provider, timeout)
    
    # Run async function in sync context
    import asyncio
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    result = loop.run_until_complete(
        engine.generate_analysis_response(idea, target_market, problem_statement)
    )
    
    return result
