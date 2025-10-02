"""
Integration tests for MCP policy system.

Tests that verify PolicyProcessor can parse policy files, extract rules,
and validate policy structure correctly.
"""

import sys
from pathlib import Path

import pytest

# Add src to path (conftest.py should handle this, but we ensure it here too)
src_path = Path(__file__).absolute().parent.parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from mcp_local.policy_processor import PolicyProcessor  # noqa: E402


@pytest.mark.integration
@pytest.mark.asyncio
async def test_policy_initialization() -> None:
    """
    Test that PolicyProcessor can be initialized successfully.

    Validates:
    - PolicyProcessor instance can be created
    - Required attributes are present
    - Rule ID pattern is configured
    """
    processor = PolicyProcessor()

    assert processor is not None, "PolicyProcessor should be initialized"
    assert hasattr(processor, "rule_id_pattern"), "Should have rule_id_pattern attribute"
    assert hasattr(processor, "required_sections"), "Should have required_sections attribute"
    assert processor.required_sections is not None, "Required sections should be configured"


@pytest.mark.integration
def test_rule_extraction() -> None:
    """
    Test that PolicyProcessor can extract rule IDs from policy content.

    Validates:
    - extract_rule_ids parses rule IDs correctly
    - Rule IDs in format [P-001], [F-101] are found
    - Context text is captured with each rule
    - Line numbers are tracked
    """
    processor = PolicyProcessor()

    # Sample policy content with various rule formats
    test_content = """
# Principles

[P-001] All code must follow consistent style guidelines.
This is additional context for the rule.

[P-002] Error handling should be comprehensive and explicit.

# Forbidden Actions

[F-101] Never commit secrets to version control.
[F-102] Avoid using deprecated APIs.

## Style Rules

[S-001] Use meaningful variable names.
"""

    rules = processor.extract_rule_ids(test_content)

    assert isinstance(rules, list), "Should return a list of rules"
    assert len(rules) >= 5, f"Should extract at least 5 rules, found {len(rules)}"

    # Check rule structure
    for rule_id, context, line_num in rules:
        assert isinstance(rule_id, str), "Rule ID should be a string"
        assert isinstance(context, str), "Context should be a string"
        assert isinstance(line_num, int), "Line number should be an integer"
        assert line_num > 0, "Line number should be positive"

    # Check that expected rule IDs are present
    rule_ids = [rule[0] for rule in rules]
    assert "P-001" in rule_ids, "Should find rule P-001"
    assert "P-002" in rule_ids, "Should find rule P-002"
    assert "F-101" in rule_ids, "Should find rule F-101"
    assert "F-102" in rule_ids, "Should find rule F-102"
    assert "S-001" in rule_ids, "Should find rule S-001"


@pytest.mark.integration
def test_section_parsing() -> None:
    """
    Test that PolicyProcessor can parse sections from policy markdown.

    Validates:
    - parse_sections extracts headers and content
    - Sections are organized by header name
    - Content is associated with correct section
    - Multiple header levels are handled
    """
    processor = PolicyProcessor()

    # Sample policy content with multiple sections
    test_content = """
# Principles

These are the core principles for the project.
All developers must follow these guidelines.

## Sub-Principle

This is a sub-section with additional details.

# Forbidden Actions

These actions should never be performed:
- Never commit secrets
- Never skip tests

# Style Guide

Follow consistent coding style:
- Use 4 spaces for indentation
- Maximum line length: 100 characters
"""

    sections = processor.parse_sections(test_content)

    assert isinstance(sections, dict), "Should return a dictionary of sections"
    assert len(sections) > 0, "Should parse at least one section"

    # Check for expected sections
    section_names = list(sections.keys())
    assert any("Principles" in name for name in section_names), "Should find Principles section"
    assert any(
        "Forbidden" in name for name in section_names
    ), "Should find Forbidden Actions section"
    assert any("Style" in name for name in section_names), "Should find Style Guide section"

    # Check that sections have content
    for section_name, content in sections.items():
        assert isinstance(section_name, str), "Section name should be a string"
        assert isinstance(content, str), "Section content should be a string"
        assert len(content.strip()) > 0, f"Section '{section_name}' should have content"


@pytest.mark.integration
def test_rule_validation() -> None:
    """
    Test that PolicyProcessor validates rule uniqueness correctly.

    Validates:
    - validate_rule_uniqueness detects duplicate rule IDs
    - Unique rules pass validation
    - Duplicate rules are reported with line numbers
    """
    processor = PolicyProcessor()

    # Test unique rules (should pass)
    unique_rules = [
        ("P-001", "Context for rule 1", 10),
        ("P-002", "Context for rule 2", 20),
        ("F-101", "Context for rule 3", 30),
    ]

    unique_result = processor.validate_rule_uniqueness(unique_rules)

    assert isinstance(unique_result, dict), "Should return validation result dictionary"
    assert unique_result["is_valid"] is True, "Unique rules should be valid"
    assert unique_result["total_rules"] == 3, "Should count all rules"
    assert unique_result["unique_rules"] == 3, "All rules should be unique"
    assert len(unique_result["duplicates"]) == 0, "Should have no duplicates"

    # Test duplicate rules (should fail)
    duplicate_rules = [
        ("P-001", "First occurrence", 10),
        ("P-002", "Context for rule 2", 20),
        ("P-001", "Duplicate occurrence", 30),
    ]

    duplicate_result = processor.validate_rule_uniqueness(duplicate_rules)

    assert duplicate_result["is_valid"] is False, "Duplicate rules should be invalid"
    assert duplicate_result["total_rules"] == 3, "Should count all rules"
    assert duplicate_result["unique_rules"] == 2, "Should identify 2 unique rules"
    assert len(duplicate_result["duplicates"]) > 0, "Should report duplicates"
    assert "P-001" in duplicate_result["duplicates"], "Should identify P-001 as duplicate"
