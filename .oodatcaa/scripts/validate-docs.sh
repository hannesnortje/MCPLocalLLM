#!/usr/bin/env bash
# Documentation Quality Validation Script
# Validates markdown links, checks for broken cross-references

set -euo pipefail

DOCS_DIR=".oodatcaa"
EXIT_CODE=0

echo "=== Documentation Quality Validation ==="
echo ""

# Check 1: Validate all markdown files exist
echo "✓ Check 1: Core documentation files exist"
REQUIRED_DOCS=(
    "$DOCS_DIR/START_HERE.md"
    "$DOCS_DIR/RUNBOOK.md"
    "$DOCS_DIR/TROUBLESHOOTING.md"
    "$DOCS_DIR/ONBOARDING.md"
    "$DOCS_DIR/ARCHITECTURE.md"
    "$DOCS_DIR/QUALITY_STANDARDS.md"
    "$DOCS_DIR/OODATCAA_LOOP_GUIDE.md"
    "$DOCS_DIR/AGENT_ROLES_MATRIX.md"
    "$DOCS_DIR/AGENT_INTERACTION_GUIDE.md"
)

for doc in "${REQUIRED_DOCS[@]}"; do
    if [[ ! -f "$doc" ]]; then
        echo "  ❌ Missing: $doc"
        EXIT_CODE=1
    else
        echo "  ✅ $doc"
    fi
done
echo ""

# Check 2: Validate markdown syntax (basic)
echo "✓ Check 2: Markdown syntax validation"
for doc in "${REQUIRED_DOCS[@]}"; do
    if [[ -f "$doc" ]]; then
        # Check for unclosed code blocks
        CODE_BLOCKS=$(grep -c '^```' "$doc" || true)
        if (( CODE_BLOCKS % 2 != 0 )); then
            echo "  ⚠️  $doc: Unclosed code block (odd number of \`\`\`)"
            EXIT_CODE=1
        fi
        
        # Check for table of contents
        if grep -q "## Table of Contents" "$doc" || grep -q "## Quick Navigation" "$doc"; then
            echo "  ✅ $doc: Has navigation"
        fi
    fi
done
echo ""

# Check 3: Cross-reference validation (basic)
echo "✓ Check 3: Cross-reference validation"
CROSS_REF_COUNT=$(grep -r "\[.*\](.*\.md)" "$DOCS_DIR" --include="*.md" | wc -l)
echo "  Found $CROSS_REF_COUNT markdown cross-references"

# Check if START_HERE.md links to key docs
if grep -q "RUNBOOK.md" "$DOCS_DIR/START_HERE.md" && \
   grep -q "TROUBLESHOOTING.md" "$DOCS_DIR/START_HERE.md" && \
   grep -q "ONBOARDING.md" "$DOCS_DIR/START_HERE.md" && \
   grep -q "ARCHITECTURE.md" "$DOCS_DIR/START_HERE.md"; then
    echo "  ✅ START_HERE.md links to all core docs"
else
    echo "  ❌ START_HERE.md missing links to core docs"
    EXIT_CODE=1
fi
echo ""

# Check 4: Navigation sections exist
echo "✓ Check 4: Navigation sections in core docs"
for doc in "$DOCS_DIR/RUNBOOK.md" "$DOCS_DIR/TROUBLESHOOTING.md" "$DOCS_DIR/ONBOARDING.md" "$DOCS_DIR/ARCHITECTURE.md"; do
    if [[ -f "$doc" ]]; then
        if grep -q "Complete Documentation Navigation" "$doc" || grep -q "START_HERE.md" "$doc"; then
            echo "  ✅ $(basename "$doc"): Has navigation section"
        else
            echo "  ⚠️  $(basename "$doc"): Missing navigation section"
            EXIT_CODE=1
        fi
    fi
done
echo ""

# Check 5: Version stamps
echo "✓ Check 5: Version stamps present"
for doc in "${REQUIRED_DOCS[@]}"; do
    if [[ -f "$doc" ]]; then
        if grep -q "Version:" "$doc" || grep -q "**Version:**" "$doc"; then
            echo "  ✅ $(basename "$doc"): Has version stamp"
        else
            echo "  ⚠️  $(basename "$doc"): Missing version stamp"
        fi
    fi
done
echo ""

# Summary
echo "=== Validation Summary ==="
if [[ $EXIT_CODE -eq 0 ]]; then
    echo "✅ All documentation quality checks passed!"
else
    echo "⚠️  Some checks failed - review above"
fi

exit $EXIT_CODE
