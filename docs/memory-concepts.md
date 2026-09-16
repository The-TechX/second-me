# Memory Concepts — V1 Baseline

This document freezes the conceptual baseline for the first Second-Me memory experiments. It is intentionally small: V1 stores long-term memories; it does not yet implement consolidation, learning, state, intentions, or working-memory construction.

## Long-term memory

For V1, a memory is persistent information that can be retrieved later because it is relevant to a new situation. We distinguish three kinds by the question they naturally answer.

### Episodic memory — What happened?

Episodic memory records a concrete experience or event situated in context and time.

Examples:
- "Yesterday the deployment failed after changing X."
- "On September 15 we decided to wait for a safe smoke task before testing state transitions."

An episode is not defined by being recent or short-lived. An event from years ago can remain episodic because it refers to a particular occurrence.

V1 principle: store the experience faithfully. Do not automatically turn repeated episodes into facts yet.

### Semantic memory — What do I know?

Semantic memory stores knowledge that is not primarily about one particular occurrence.

Examples:
- "ServiceNow records have a sys_id."
- "Wet smooth surfaces provide less grip."

A semantic memory may eventually be learned from multiple episodes, documentation, explicit instruction, or other evidence. V1 does not implement that consolidation process; semantic knowledge is stored explicitly when it is provided or known.

### Procedural memory — How is something done?

Procedural memory stores knowledge about how to perform a task or process.

Examples:
- "Before changing a WOT state, inspect the current record, resolve the target transition, execute it, and verify the result."
- "To deploy this service, perform A, then B, then C."

Procedural memory is knowledge about how to act. It is not the capability itself. A procedure may say how deployment should be performed; `deploy()` is a tool/capability and belongs outside memory.

## Boundaries we are keeping outside Memory V1

These concepts are related to cognition but are not long-term-memory types.

**State — What is true now?** State represents the current condition of the system or world. It is mutable. If a task changes from waiting to ready, state changes. The historical fact that it was previously waiting may instead be captured as an episode.

**Working memory — What needs to be mentally active now?** Working memory is not another persistent store. It is a temporary workspace assembled for the current reasoning step from relevant state, input, intentions, and recalled long-term memories. Episodic, semantic, and procedural memories can all be recalled into working memory.

**Intentions — What do I want or need to do?** Goals, pending actions, blockers, and plans describe intended future action. They should not be forced into long-term memory merely to keep them alive.

**Observation — What am I perceiving?** An observation is evidence arriving from the environment. It may update state and may later be encoded as an episode, but observation itself is not long-term memory.

## Current conceptual flow

```text
                 LONG-TERM MEMORY
                      │
          ┌───────────┼───────────┐
          │           │           │
       Episodic    Semantic    Procedural
      what happened  what I know  how to do it
          │           │           │
          └───────────┼───────────┘
                      │ recall
                      ▼
STATE ─────────► WORKING MEMORY ◄──────── INTENTIONS
                      ▲
                      │
                CURRENT INPUT
                      │
                      ▼
                   REASON
```

A useful provisional contract is:

```text
WorkingMemory(t) = Input(t) + Goal(t) + Observe(State(t)) + Recall(Memory)
```

This is an architectural model, not a mathematical claim about human cognition.

## V1 scope

For now Second-Me Memory should remain deliberately boring:

```text
remember(memory)
      ↓
 persistent storage
      ↓
search / retrieve / navigate
```

V1 does **not** automatically consolidate episodes into semantic knowledge, modify model weights, infer beliefs, maintain system state, manage intentions, or persist working memory.

The first design question for the next iteration is therefore not "how do we make it intelligent?" but: **what is the smallest correct representation of episodic, semantic, and procedural long-term memory, and what relationships between them are worth preserving?**
