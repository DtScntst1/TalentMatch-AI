import pytest
from app import parse_response

def test_parse_response_valid():
    """Test if the AI response parser works correctly with valid input"""
    sample_response = """SCORE: 85
MATCHED_SKILLS: Python, SQL, RAG
MISSING_SKILLS: Docker, CI/CD
SUMMARY: The candidate has strong backend skills but lacks deployment knowledge."""
    
    result = parse_response(sample_response)
    
    assert result["SCORE"] == 85
    assert result["MATCHED_SKILLS"] == "Python, SQL, RAG"
    assert result["MISSING_SKILLS"] == "Docker, CI/CD"
    assert "strong backend skills" in result["SUMMARY"]

def test_parse_response_error_handling():
    """Test if the parser gracefully handles completely invalid AI output"""
    invalid_response = "I couldn't analyze this document."
    result = parse_response(invalid_response)
    
    # It should fallback to default values
    assert result["SCORE"] == 0
    assert result["MATCHED_SKILLS"] == ""
    assert result["MISSING_SKILLS"] == ""
