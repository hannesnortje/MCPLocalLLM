# Product Objective — Small Coder Model Training with MCP Integration

> **Building a locally fine-tuned coding assistant with context preservation and daily learning capabilities**

---

## Vision (Why)
Developers need a **small, fast, locally-trained coding model** that follows project-specific rules and patterns while integrating seamlessly with Cursor IDE. Current solutions either require cloud dependencies, lack context preservation, or can't learn project-specific patterns. We need a **7B parameter model** optimized for M1 Max that embeds procedural knowledge, custom definitions, and architectural patterns while providing **dual-layer context preservation** through MCP integration.

---

## Outcome (What)
Build **MCPLocalLLM** — a complete system that:

### **Core Training System**
- Fine-tunes a **Qwen2.5-Coder-7B** model using **QLoRA** on M1 Max (32GB RAM)
- Embeds **procedural knowledge** (error handling patterns, tool usage, commit conventions)
- Learns **custom definitions** (e.g., "42 = harmony between rules and freedom")
- Trains **context window replacement** and **metadata tagging** capabilities
- Supports **daily learning cycles** with overnight training integration

### **MCP Integration Layer**
- **AGENTS MUST COPY AND ADAPT** the working MCP server from `/media/hannesn/storage/Code/MCP/`
  - Complete file system migration with conflict resolution
  - Clean and customize for small coder training project
  - Update all references and configurations
- Implement **dual-layer context preservation**:
  - **Layer 1**: Context Window Replacement (proactive education)
  - **Layer 2**: Metadata Tagging (protective contracts)
- Enable **RAG system** for dynamic knowledge injection
- Provide **agent coordination** through MCP protocol

### **Context-Aware Agent System**
- **Planner**: Creates implementation plans with context preservation tags
- **Implementer**: Writes code with metadata markers and tool calls
- **Tester**: Validates with preservation pattern respect
- **Refactorer**: Maintains architectural boundaries while respecting preservation levels
- **Doc Writer**: Updates documentation with appropriate context tags

### **Daily Learning Pipeline**
- **Insight Capture**: Automatic detection of user corrections and new patterns
- **RAG Storage**: Temporary storage of daily insights
- **Overnight Training**: Automated QLoRA training with conflict resolution
- **Model Updates**: Seamless deployment of improved models
- **Knowledge Lifecycle**: Coordination between RAG and model weights

---

## Success Criteria (Measurable)
*How will agents know when the project is complete?*

### **Training System (Core)**
- [ ] **Model Training**: Successfully fine-tune Qwen2.5-Coder-7B with QLoRA
  - Training completes in 6-24 hours on M1 Max
  - Model size ≤ 8GB quantized (GGUF Q4_K_M)
  - Embedding dimension: 384 (all-MiniLM-L6-v2 compatible)
  - Dataset: 1k-5k examples in instruction-input-output format

- [ ] **Context Training**: Model learns context preservation patterns
  - Generates context windows with system prompts and active rules
  - Embeds metadata tags with preservation levels (strict/moderate/flexible)
  - Includes rule compliance markers (concept:*, pattern:*, definition:*)
  - Provides knowledge updates for Cursor integration

- [ ] **Custom Knowledge**: Model embeds project-specific definitions
  - "42 = harmony between rules and freedom" consistently applied
  - Domain-specific error handling patterns (DomainError vs generic Error)
  - Tool usage format: `<tool:fs.write>...</tool>` syntax
  - Architectural patterns and naming conventions

### **MCP Integration (Critical)**
- [ ] **Server Migration**: Successfully copy and adapt MCP server
  - **AGENTS MUST**: Copy complete `/media/hannesn/storage/Code/MCP/` structure to this project
  - **AGENTS MUST**: Clean and adapt for small coder training project (remove unnecessary features)
  - **AGENTS MUST**: Maintain core functionality: memory management, vector search, policy system
  - **AGENTS MUST**: Update dependencies and configuration for this project
  - **AGENTS MUST**: Resolve any file conflicts between original template and MCP server files

- [ ] **Dual-Layer Context Preservation**: Both layers working together
  - Context Window Replacement: Cursor adopts LLM-provided context
  - Metadata Tagging: Individual response protection with preservation levels
  - Enhanced Cursor Rules: Respect for source validation and rule compliance
  - Integration Testing: End-to-end context preservation validation

- [ ] **Protocol Compliance**: Full MCP standard implementation
  - stdin/stdout communication with Cursor IDE
  - Tool definitions for memory management and context operations
  - Resource handlers for read-only access to system state
  - Error handling and recovery mechanisms

### **Agent System (Enhanced)**
- [ ] **Context-Aware Agents**: All agents respect preservation patterns
  - Planner embeds context preservation tags in implementation plans
  - Implementer includes metadata markers in all code responses
  - Tester validates while respecting preservation levels
  - All agents provide context windows to educate Cursor

- [ ] **Tool Integration**: Seamless tool server communication
  - File system operations (read, write, delete)
  - Git operations (commit, branch, merge)
  - Command execution with proper error handling
  - Search and indexing capabilities

### **Daily Learning System (Advanced)**
- [ ] **Insight Capture**: Automatic learning from user interactions
  - Detect user corrections with ≥85% accuracy
  - Capture explicit teaching commands ("remember this", "always do")
  - Identify new patterns and architectural decisions
  - Store insights with confidence scores and validation status

- [ ] **Overnight Training**: Automated model improvement
  - Insight aggregation and conflict resolution (5 minutes)
  - Training data generation with context enhancement (10 minutes)
  - Incremental QLoRA training (2-6 hours)
  - Validation and deployment with rollback safety (15 minutes)

### **Quality & Performance (Production-Ready)**
- [ ] **Code Quality**: 
  - ≥ 85% line coverage on all modules
  - ≥ 75% branch coverage
  - 0 high-severity issues in pip-audit
  - black, ruff, mypy pass on all code
  - Type hints: mypy strict mode enabled

- [ ] **Performance Benchmarks**:
  - Model inference: <2s response time for typical coding queries
  - Memory usage: ≤16GB RAM during inference
  - Training time: 6-24 hours for incremental updates
  - Context preservation: ≥95% success rate in validation tests

- [ ] **Integration Testing**:
  - End-to-end Cursor IDE integration working
  - MCP protocol communication stable
  - Context preservation validated across all agent types
  - Daily learning cycle completes without manual intervention

### **Documentation & Deployment (Complete)**
- [ ] **Comprehensive Documentation**:
  - README with installation, training, and usage instructions
  - Architecture diagrams showing training and MCP integration flow
  - Training dataset examples with context window and metadata patterns
  - Cursor Rules configuration guide
  - Troubleshooting guide for common issues

- [ ] **Deployment Ready**:
  - Docker containers for Qdrant and training environment
  - Automated setup scripts for M1 Max environment
  - Model serving with Ollama/MLX integration
  - Backup and recovery procedures for trained models

---

## Constraints / Guardrails

### **Hardware & Performance**
- **Target Platform**: Apple M1 Max with 32GB RAM
- **Model Size**: 7B parameters (Qwen2.5-Coder-7B base)
- **Training Method**: QLoRA with rank=16, alpha=32
- **Quantization**: GGUF Q4_K_M for deployment
- **Memory Limit**: ≤16GB RAM during inference

### **Technical Stack**
- **Base Model**: Qwen2.5-Coder-7B-Instruct
- **Training Framework**: axolotl or Apple MLX-LM
- **Serving**: Ollama or MLX for local inference
- **Vector DB**: Qdrant for RAG and memory management
- **Protocol**: MCP (Model Context Protocol) for Cursor integration
- **Embeddings**: sentence-transformers (all-MiniLM-L6-v2)

### **Quality Gates**
- **Type Checking**: mypy strict mode for all Python code
- **Formatting**: black with line-length=100
- **Linting**: ruff with security and best practice rules
- **Testing**: pytest with asyncio support for MCP testing
- **Security**: pip-audit clean, no high-severity vulnerabilities

### **Context Preservation Requirements**
- **Preservation Levels**: strict (no changes), moderate (preserve logic), flexible (preserve intent)
- **Rule Compliance**: Dynamic pattern-based categories (concept:*, pattern:*, definition:*)
- **Source Validation**: Always respect responses marked with `source: "local_trained_model"`
- **Metadata Enforcement**: Cursor rules must enforce preservation policies

### **Learning System Constraints**
- **Training Frequency**: Adaptive based on insight volume (nightly to weekly)
- **Conflict Resolution**: Temporal precedence with user preference override
- **Quality Control**: Multi-layer validation pipeline with rollback safety
- **Knowledge Lifecycle**: Clear separation between RAG (temporary) and model weights (permanent)

---

## Non-Goals (Out of Scope)

### **Explicitly NOT building:**
- ❌ **Large model training** (>7B parameters - hardware constraints)
- ❌ **Cloud dependencies** (fully local system required)
- ❌ **Real-time training** (overnight batch training only)
- ❌ **Multi-user system** (single developer focus)
- ❌ **GUI interface** (CLI and IDE integration only)
- ❌ **Model serving infrastructure** (use existing Ollama/MLX)

### **Out of scope for v1.0 (future versions):**
- Advanced query languages for RAG system
- Multi-model ensemble training
- Distributed training across multiple machines
- Integration with other IDEs beyond Cursor
- Advanced conflict resolution with human-in-the-loop

---

## Implementation Strategy

### **Phase 1: MCP Server Migration (Week 1)**
1. **Copy MCP Server**: **AGENTS EXECUTE** - Complete migration from `/media/hannesn/storage/Code/MCP/`
   - Use `cp -r /media/hannesn/storage/Code/MCP/* /media/hannesn/storage/Code/MCPLocalLLM/`
   - Resolve file conflicts (prioritize MCP server files over template files)
   - Preserve OODATCAA system files in `.oodatcaa/` directory
2. **Clean & Adapt**: **AGENTS EXECUTE** - Remove unnecessary features, update for training focus
   - Remove UI components not needed for training system
   - Update package name from "mcp-memory-server" to "mcp-local-llm"
   - Adapt configuration for small coder training use case
3. **Integration Testing**: **AGENTS EXECUTE** - Verify MCP protocol communication with Cursor
4. **Documentation**: **AGENTS EXECUTE** - Update configuration and setup instructions

### **Phase 2: Training System (Weeks 2-3)**
1. **Dataset Creation**: Build 1k-5k training examples with context patterns
2. **QLoRA Setup**: Configure training environment for M1 Max
3. **Base Model Training**: Initial fine-tuning with procedural knowledge
4. **Validation Pipeline**: Automated testing and quality assurance

### **Phase 3: Context Preservation (Week 4)**
1. **Dual-Layer Implementation**: Context windows + metadata tagging
2. **Cursor Rules Enhancement**: Advanced preservation policies
3. **Agent System**: Context-aware agent implementations
4. **End-to-End Testing**: Full integration validation

### **Phase 4: Daily Learning (Week 5)**
1. **Insight Capture**: Automatic pattern detection system
2. **Overnight Pipeline**: Automated training and deployment
3. **Conflict Resolution**: Systematic handling of contradictory insights
4. **Knowledge Lifecycle**: RAG ↔ Model weight coordination

---

## Notes
- **Objective ID:** OBJ-2025-002
- **Created:** 2025-10-01
- **Target Platform:** Apple M1 Max (32GB RAM)
- **Base Architecture:** Qwen2.5-Coder-7B with QLoRA fine-tuning
- **Integration Method:** MCP protocol with dual-layer context preservation
- **Learning Approach:** Daily insight capture with overnight training integration

---

## Success Metrics
- **Training Success**: Model completes fine-tuning and passes validation tests
- **Context Preservation**: ≥95% success rate in preserving custom patterns and definitions
- **Integration Quality**: Seamless Cursor IDE experience with no manual context management
- **Learning Effectiveness**: Model improves daily based on user interactions and corrections
- **Performance Target**: Sub-2s response times with ≤16GB RAM usage

---

**Agents:** This objective defines a complete system for training and deploying a small, context-aware coding model with advanced MCP integration and daily learning capabilities. You may now plan sprints to achieve this comprehensive objective!
