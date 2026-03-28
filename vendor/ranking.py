"""
ranking.py

A production-ready module to evaluate and rank vendor data based on a weighted 
combination of Google Places rating and review count.
"""

import math
import logging
from typing import List, Dict, Any, Optional

# Configure standard logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VendorRanker:
    """
    Ranks vendors based on ratings (0.7 weight) and reviews (0.3 weight).
    """

    def __init__(self, rating_weight: float = 0.7, reviews_weight: float = 0.3):
        # Normalize weights to ensure they sum to 1.0
        total_weight = rating_weight + reviews_weight
        if total_weight <= 0:
            raise ValueError("Total weight must be greater than 0")
        
        self.rating_weight = rating_weight / total_weight
        self.reviews_weight = reviews_weight / total_weight

    def _normalize_reviews(self, review_count: Any) -> float:
        """
        Normalizes the review count to a 0.0 - 1.0 scale.
        Uses a logarithmic scale since the difference between 10 and 100 reviews 
        is more significant than the difference between 1010 and 1100 reviews.
        This prevents massive review counts from overpowering the score.
        """
        try:
            val = float(review_count) if review_count is not None else 0.0
            if val <= 0:
                return 0.0
            
            # log1p safely handles 0. log1p(1000) ~ 6.9
            # Normalizing against an assumed "excellent" count (e.g., 1000 reviews = 1.0)
            max_log = math.log1p(1000)
            normalized = math.log1p(val) / max_log
            return min(normalized, 1.0)
        except (ValueError, TypeError):
            logger.debug(f"Invalid review count encountered: {review_count}. Defaulting to 0.")
            return 0.0

    def _normalize_rating(self, rating: Any) -> float:
        """
        Normalizes a 0-5 rating to a 0.0 - 1.0 scale.
        """
        try:
            val = float(rating) if rating is not None else 0.0
            if val <= 0:
                return 0.0
            
            # Cap rating at 5.0 and normalize
            return min(val / 5.0, 1.0)
        except (ValueError, TypeError):
            logger.debug(f"Invalid rating encountered: {rating}. Defaulting to 0.")
            return 0.0

    def calculate_score(self, vendor: Dict[str, Any]) -> float:
        """
        Calculates the weighted score for a given vendor based on rating and reviews.
        Returns a score from 0.0 to 100.0.
        """
        if not isinstance(vendor, dict):
            logger.error("Vendor data must be a dictionary.")
            return 0.0

        norm_rating = self._normalize_rating(vendor.get("rating"))
        norm_reviews = self._normalize_reviews(vendor.get("reviews"))

        base_score = (norm_rating * self.rating_weight) + (norm_reviews * self.reviews_weight)
        
        # Scale to a 0.0 - 100.0 score format for better readability
        final_score = round(base_score * 100.0, 2)
        return final_score

    def rank_vendors(self, vendors: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Takes a list of vendor dictionaries, calculates their scores,
        adds a "score" key to each, and returns the list sorted descending by score.
        """
        if not vendors:
            return []

        if not isinstance(vendors, list):
            logger.error("Input vendors must be a list of dictionaries.")
            return []

        ranked_list = []
        for vendor in vendors:
            if not isinstance(vendor, dict):
                continue
            
            # Modifying dictionary to add "score"
            vendor['score'] = self.calculate_score(vendor)
            ranked_list.append(vendor)

        # Sort by score descending
        ranked_list.sort(key=lambda x: x.get('score', 0.0), reverse=True)
        return ranked_list


def process_vendors(vendors: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Convenience function to evaluate and rank vendor data.
    """
    ranker = VendorRanker()
    return ranker.rank_vendors(vendors)
