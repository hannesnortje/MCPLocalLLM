#!/usr/bin/env bash
#
# Automatic Log Rotation Script
#
# Rotates OODATCAA log files when they exceed 1000 lines.
# Archives to .oodatcaa/work/archive/sprint_N/ with sequential numbering.
# Preserves recent 400-500 lines in active log.
#
# Usage:
#   ./scripts/rotate-logs.sh                    # Check and rotate all logs
#   ./scripts/rotate-logs.sh --dry-run          # Preview actions without executing
#   ./scripts/rotate-logs.sh --file <path>      # Rotate specific file
#   ./scripts/rotate-logs.sh --threshold 1500   # Custom threshold
#

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORK_DIR="${PROJECT_ROOT}/.oodatcaa/work"
ARCHIVE_BASE="${WORK_DIR}/archive"

# Configuration
THRESHOLD=1000          # Lines threshold for rotation
KEEP_LINES=450         # Lines to keep in active log after rotation
DRY_RUN=false
SPECIFIC_FILE=""
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')

# Log files to monitor
LOG_FILES=(
    "${WORK_DIR}/AGENT_LOG.md"
    "${WORK_DIR}/SPRINT_LOG.md"
    "${WORK_DIR}/SPRINT_PLAN.md"
)

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Usage function
usage() {
    cat << EOF
Usage: $(basename "$0") [OPTIONS]

Automatically rotate OODATCAA log files when they exceed threshold.

Options:
    --dry-run           Preview actions without executing
    --file PATH         Rotate specific file only
    --threshold NUM     Custom line threshold (default: 1000)
    --keep-lines NUM    Lines to keep in active log (default: 450)
    --help              Show this help message

Examples:
    $(basename "$0")                           # Check and rotate all logs
    $(basename "$0") --dry-run                 # Preview rotation
    $(basename "$0") --file AGENT_LOG.md       # Rotate specific file
    $(basename "$0") --threshold 1500          # Custom threshold

EOF
    exit 0
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --file)
            SPECIFIC_FILE="$2"
            shift 2
            ;;
        --threshold)
            THRESHOLD="$2"
            shift 2
            ;;
        --keep-lines)
            KEEP_LINES="$2"
            shift 2
            ;;
        --help|-h)
            usage
            ;;
        *)
            echo "Unknown option: $1"
            usage
            ;;
    esac
done

# Get current sprint number
get_sprint_number() {
    if [ -f "${WORK_DIR}/SPRINT_QUEUE.json" ]; then
        grep -oP '"sprint":\s*\K\d+' "${WORK_DIR}/SPRINT_QUEUE.json" | head -1
    else
        echo "2"  # Default to sprint 2
    fi
}

SPRINT_NUM=$(get_sprint_number)
ARCHIVE_DIR="${ARCHIVE_BASE}/sprint_${SPRINT_NUM}"

# Get next archive number for a file
get_next_archive_num() {
    local filename=$(basename "$1" .md)
    local pattern="${ARCHIVE_DIR}/${filename}_archive_*.md"
    local max_num=0
    
    for file in ${pattern} 2>/dev/null; do
        if [ -f "$file" ]; then
            num=$(echo "$file" | grep -oP 'archive_\K\d+' || echo "0")
            if [ "$num" -gt "$max_num" ]; then
                max_num=$num
            fi
        fi
    done
    
    printf "%03d" $((max_num + 1))
}

# Count lines in file
count_lines() {
    if [ -f "$1" ]; then
        wc -l < "$1"
    else
        echo "0"
    fi
}

# Rotate a single log file
rotate_file() {
    local log_file="$1"
    local filename=$(basename "$log_file")
    local basename_no_ext="${filename%.md}"
    
    if [ ! -f "$log_file" ]; then
        echo -e "${YELLOW}⚠${NC}  File not found: $log_file"
        return 1
    fi
    
    local line_count=$(count_lines "$log_file")
    
    if [ "$line_count" -le "$THRESHOLD" ]; then
        echo -e "${GREEN}✓${NC}  $filename: ${line_count} lines (below threshold)"
        return 0
    fi
    
    echo -e "${YELLOW}⚠${NC}  $filename: ${line_count} lines (exceeds threshold of ${THRESHOLD})"
    
    # Calculate lines to archive
    local archive_lines=$((line_count - KEEP_LINES))
    
    if [ "$archive_lines" -le 0 ]; then
        echo -e "${YELLOW}!${NC}  $filename: File too small to rotate meaningfully"
        return 0
    fi
    
    # Get next archive number
    local archive_num=$(get_next_archive_num "$log_file")
    local archive_file="${ARCHIVE_DIR}/${basename_no_ext}_archive_${archive_num}.md"
    
    echo -e "${BLUE}→${NC}  Rotating $filename..."
    echo "     Archive: ${archive_lines} lines → $(basename "$archive_file")"
    echo "     Keep:    ${KEEP_LINES} lines in active log"
    
    if [ "$DRY_RUN" = true ]; then
        echo -e "${BLUE}[DRY RUN]${NC} Would create: $archive_file"
        return 0
    fi
    
    # Create archive directory
    mkdir -p "$ARCHIVE_DIR"
    
    # Backup original file
    local backup_file="${log_file}.backup.${TIMESTAMP}"
    cp "$log_file" "$backup_file"
    
    # Extract lines to archive
    head -n "$archive_lines" "$log_file" > "$archive_file"
    
    # Keep recent lines in active log
    tail -n "$KEEP_LINES" "$log_file" > "${log_file}.tmp"
    mv "${log_file}.tmp" "$log_file"
    
    # Verify operation
    local new_line_count=$(count_lines "$log_file")
    local archived_line_count=$(count_lines "$archive_file")
    
    if [ "$new_line_count" -eq "$KEEP_LINES" ] && [ "$archived_line_count" -eq "$archive_lines" ]; then
        echo -e "${GREEN}✓${NC}  Rotation complete: $filename"
        echo "     Active log: ${new_line_count} lines"
        echo "     Archived:   ${archived_line_count} lines"
        
        # Clean up backup
        rm -f "$backup_file"
        
        # Log to stats
        log_rotation_stats "$filename" "$line_count" "$new_line_count" "$archived_line_count" "$archive_file"
        
        return 0
    else
        echo -e "${RED}✗${NC}  Rotation verification failed for $filename!"
        echo "     Expected: active=${KEEP_LINES}, archived=${archive_lines}"
        echo "     Got:      active=${new_line_count}, archived=${archived_line_count}"
        echo "     Restoring from backup..."
        mv "$backup_file" "$log_file"
        rm -f "$archive_file"
        return 1
    fi
}

# Log rotation statistics
log_rotation_stats() {
    local filename="$1"
    local old_lines="$2"
    local new_lines="$3"
    local archived_lines="$4"
    local archive_file="$5"
    
    local stats_file="${PROJECT_ROOT}/ROTATION_STATS.md"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    # Create stats file if it doesn't exist
    if [ ! -f "$stats_file" ]; then
        cat > "$stats_file" << 'EOF'
# Log Rotation Statistics

Automatic log rotation tracking for OODATCAA system logs.

## Rotation History

| Timestamp | File | Lines Before | Lines After | Lines Archived | Archive File |
|-----------|------|--------------|-------------|----------------|--------------|
EOF
    fi
    
    # Append rotation entry
    echo "| ${timestamp} | ${filename} | ${old_lines} | ${new_lines} | ${archived_lines} | $(basename "$archive_file") |" >> "$stats_file"
}

# Main execution
main() {
    echo "OODATCAA Log Rotation System"
    echo "============================="
    echo
    
    if [ "$DRY_RUN" = true ]; then
        echo -e "${BLUE}[DRY RUN MODE]${NC} No files will be modified"
        echo
    fi
    
    echo "Configuration:"
    echo "  Threshold:   ${THRESHOLD} lines"
    echo "  Keep recent: ${KEEP_LINES} lines"
    echo "  Sprint:      ${SPRINT_NUM}"
    echo "  Archive:     ${ARCHIVE_DIR}"
    echo
    
    local rotated=0
    local checked=0
    
    if [ -n "$SPECIFIC_FILE" ]; then
        # Rotate specific file
        if rotate_file "$SPECIFIC_FILE"; then
            ((rotated++))
        fi
        ((checked++))
    else
        # Check and rotate all log files
        for log_file in "${LOG_FILES[@]}"; do
            if rotate_file "$log_file"; then
                if [ $(count_lines "$log_file") -lt "$THRESHOLD" ]; then
                    : # File was rotated or doesn't need rotation
                else
                    ((rotated++))
                fi
            fi
            ((checked++))
        done
    fi
    
    echo
    echo "Summary:"
    echo "  Files checked: ${checked}"
    echo "  Files rotated: ${rotated}"
    
    if [ "$rotated" -gt 0 ]; then
        echo
        echo "Next steps:"
        echo "  1. Review archived files in: ${ARCHIVE_DIR}"
        echo "  2. Run: bash scripts/generate-archive-index.sh"
        echo "  3. Check: ROTATION_STATS.md for rotation history"
    fi
}

main

