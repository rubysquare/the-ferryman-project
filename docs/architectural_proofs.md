# Formal Architectural Proofs & Invariant Specifications

This document defines the formal mathematical specification and proofs of correctness for **The Ferryman Project**, verifying that the implementation strictly satisfies the five core alignment guardrails specified in [`AGENTS.md`](../AGENTS.md).

---

## 1. Formal System Model

The Ferryman Core Engine is modeled as a deterministic finite-state automaton with output:

$$\mathcal{M} = \langle S, \Sigma, \Gamma, \delta, \lambda, s_0, F \rangle$$

Where:
- **State Space $S$**:
  $$S = \{ S_{\text{INIT}}, S_{\text{SOMATIC}}, S_{\text{INQUIRY}}, S_{\text{WAIT\_INPUT}}, S_{\text{ACKNOWLEDGE}}, S_{\text{BREAKER}}, S_{\text{TERMINATE}} \}$$
- **Input Alphabet $\Sigma$**:
  $$\Sigma = \Sigma_{\text{string}} \cup \{ \epsilon, \text{EOF}, \text{SIGINT}, \text{HEADLESS} \}$$
  Where $\Sigma_{\text{string}}$ is partitioned into:
  $$\Sigma_{\text{string}} = \Sigma_{\text{reflection}} \uplus \Sigma_{\text{advice\_seeking}}$$
- **Output Alphabet $\Gamma$**:
  $$\Gamma = \Gamma_{\text{stdout}} \cup \Gamma_{\text{speech}} \cup \Gamma_{\text{storage}} \cup \{ \emptyset \}$$
- **Start State**: $s_0 = S_{\text{INIT}}$
- **Terminal States**: $F = \{ S_{\text{TERMINATE}} \}$

---

## 2. Transition Function $\delta$

The state transition function $\delta: S \times \Sigma \to S$ is defined as follows:

1. **Initialization**:
   $$\delta(S_{\text{INIT}}, \epsilon) = S_{\text{SOMATIC}}$$
2. **Somatic Phase**:
   $$\delta(S_{\text{SOMATIC}}, \epsilon) = S_{\text{INQUIRY}}$$
3. **Inquiry Phase**:
   $$\delta(S_{\text{INQUIRY}}, \text{HEADLESS}) = S_{\text{TERMINATE}}$$
   $$\delta(S_{\text{INQUIRY}}, \epsilon) = S_{\text{WAIT\_INPUT}}$$
4. **Input Processing Phase**:
   $$\delta(S_{\text{WAIT\_INPUT}}, \sigma \in \Sigma_{\text{advice\_seeking}}) = S_{\text{BREAKER}}$$
   $$\delta(S_{\text{WAIT\_INPUT}}, \sigma \in \Sigma_{\text{reflection}}) = S_{\text{ACKNOWLEDGE}}$$
   $$\delta(S_{\text{WAIT\_INPUT}}, \text{EOF} \vee \text{SIGINT}) = S_{\text{TERMINATE}}$$
5. **Acknowledge Phase**:
   $$\delta(S_{\text{ACKNOWLEDGE}}, \epsilon) = S_{\text{TERMINATE}}$$
6. **Circuit Breaker Phase**:
   $$\delta(S_{\text{BREAKER}}, \epsilon) = S_{\text{TERMINATE}}$$

---

## 3. Theorem 1: Anti-Engagement & Bounded Execution (Guardrail 2)

### Statement
Every execution path $\pi$ in $\mathcal{M}$ is strictly acyclic, finite, and bounded in length:

$$\forall \pi = (s_0, s_1, \dots, s_k), \quad s_k \in F \implies |\pi| \le 5$$

### Proof
Construct the directed transition graph $G = (S, E)$ where $(u, v) \in E \iff \exists \sigma \in \Sigma : \delta(u, \sigma) = v$.
Evaluating the edges:
$$E = \{ (S_{\text{INIT}}, S_{\text{SOMATIC}}), (S_{\text{SOMATIC}}, S_{\text{INQUIRY}}), (S_{\text{INQUIRY}}, S_{\text{WAIT\_INPUT}}), (S_{\text{INQUIRY}}, S_{\text{TERMINATE}}), (S_{\text{WAIT\_INPUT}}, S_{\text{BREAKER}}), (S_{\text{WAIT\_INPUT}}, S_{\text{ACKNOWLEDGE}}), (S_{\text{WAIT\_INPUT}}, S_{\text{TERMINATE}}), (S_{\text{BREAKER}}, S_{\text{TERMINATE}}), (S_{\text{ACKNOWLEDGE}}, S_{\text{TERMINATE}}) \}$$

1. **Acyclicity**: Observe that all edges advance monotonically toward $S_{\text{TERMINATE}}$. No back-edge exists:
   $$\forall u, v \in S, \quad (u, v) \in E \implies \operatorname{depth}(u) < \operatorname{depth}(v)$$
   Where $\operatorname{depth}(S_{\text{INIT}}) = 0$ and $\operatorname{depth}(S_{\text{TERMINATE}}) = 4$.
2. **Absence of Self-Loops**: $\forall u \in S, (u, u) \notin E$.
3. **Dialogue Immunity**: There is no path from $S_{\text{ACKNOWLEDGE}}$ or $S_{\text{BREAKER}}$ back to $S_{\text{WAIT\_INPUT}}$ or $S_{\text{INQUIRY}}$.

Hence, $G$ is a Directed Acyclic Graph (DAG) with maximal path length:
$$\max |\pi| = \operatorname{length}(S_{\text{INIT}} \to S_{\text{SOMATIC}} \to S_{\text{INQUIRY}} \to S_{\text{WAIT\_INPUT}} \to S_{\text{ACKNOWLEDGE}} \to S_{\text{TERMINATE}}) = 5$$

The system cannot enter an infinite conversation or engagement spiral. $\blacksquare$

---

## 4. Theorem 2: Somatic Primacy (Guardrail 3)

### Statement
In any crossing execution, the somatic grounding state strictly dominates the cognitive inquiry and input states:

$$\forall \pi = (s_0, s_1, \dots, s_k) \text{ with } s_k \in \{ S_{\text{INQUIRY}}, S_{\text{WAIT\_INPUT}}, S_{\text{ACKNOWLEDGE}} \}, \quad \exists j < k : s_j = S_{\text{SOMATIC}}$$

### Proof
From the definition of $\delta$:
- $\operatorname{Predecessors}(S_{\text{INQUIRY}}) = \{ S_{\text{SOMATIC}} \}$
- $\operatorname{Predecessors}(S_{\text{WAIT\_INPUT}}) = \{ S_{\text{INQUIRY}} \}$
- $\operatorname{Predecessors}(S_{\text{ACKNOWLEDGE}}) = \{ S_{\text{WAIT\_INPUT}} \}$

By backward induction, any path reaching $S_{\text{INQUIRY}}$, $S_{\text{WAIT\_INPUT}}$, or $S_{\text{ACKNOWLEDGE}}$ must have passed through $S_{\text{SOMATIC}}$.
Therefore, $S_{\text{SOMATIC}}$ is an essential dominator node:
$$S_{\text{SOMATIC}} \operatorname{dom} S_{\text{INQUIRY}}$$
Physical grounding is mathematically guaranteed to precede cognitive reflection. $\blacksquare$

---

## 5. Theorem 3: Zero Network Egress & Data Sovereignty (Guardrail 1 & 4)

### Statement
Let $\Omega_{\text{net}}$ be the set of POSIX socket and network I/O primitives:
$$\Omega_{\text{net}} = \{ \text{socket}, \text{connect}, \text{bind}, \text{send}, \text{sendto}, \text{recv}, \text{getaddrinfo} \}$$
The Ferryman core module set $\mathcal{C}$ satisfies:
$$\operatorname{Calls}(\mathcal{C}) \cap \Omega_{\text{net}} = \emptyset$$

### Proof
1. **Module Inspection**: The modules in `ferryman/` import only standard library components:
   - `sys`, `os`, `re`, `shutil`, `subprocess`, `json`, `tempfile`, `datetime`, `time`, `signal`, `typing`, `abc`.
2. **Network Module Exclusion**: Modules `socket`, `urllib`, `http`, `asyncio`, `requests`, or any external networking packages are absent from `ferryman/`.
3. **Storage Atomicity & Isolation**:
   Every persistent write operation in `ferryman/storage.py` follows the atomic swap protocol:
   $$\text{tmp} = \operatorname{mkstemp}(\operatorname{dir}), \quad \operatorname{write}(\text{tmp}), \quad \operatorname{fsync}(\text{tmp}), \quad \operatorname{chmod}(\text{tmp}, 0600), \quad \operatorname{replace}(\text{tmp}, \text{target})$$
   - **Confidentiality**: Mode `0600` guarantees only the executing user UID can read or write the data ($S_{\text{read}} = \{\text{owner}\}$, $S_{\text{write}} = \{\text{owner}\}$).
   - **Atomicity**: POSIX `rename`/`replace` is atomic; partial or torn states cannot be observed by readers. $\blacksquare$

---

## 6. Theorem 4: Temporal Window Decidability & Soundness

### Statement
Let $\mathbb{T} = [0, 1439] \subset \mathbb{N}$ represent the minutes of a 24-hour day. Given a window specification $W = \langle t_{\text{start}}, t_{\text{end}} \rangle \in \mathbb{T} \times \mathbb{T}$, the membership function $\chi_W: \mathbb{T} \to \{0, 1\}$ defined by:

$$\chi_W(t) = \begin{cases}
1 & \text{if } t_{\text{start}} \le t_{\text{end}} \land t_{\text{start}} \le t \le t_{\text{end}} \\
1 & \text{if } t_{\text{start}} > t_{\text{end}} \land (t \ge t_{\text{start}} \lor t \le t_{\text{end}}) \\
0 & \text{otherwise}
\end{cases}$$

is total, sound, and partition-preserving.

### Proof
1. **Case 1 ($t_{\text{start}} \le t_{\text{end}}$)**: The interval $[t_{\text{start}}, t_{\text{end}}]$ is a convex subset of $\mathbb{T}$. For any $t \in \mathbb{T}$, either $t \in [t_{\text{start}}, t_{\text{end}}]$ or $t \in [0, t_{\text{start}}) \cup (t_{\text{end}}, 1439]$. The decision is unambiguous.
2. **Case 2 ($t_{\text{start}} > t_{\text{end}}$)**: The interval wraps across the midnight boundary $t = 1439 \to t = 0$. The allowed set is $[t_{\text{start}}, 1439] \cup [0, t_{\text{end}}]$. Its complement is $(t_{\text{end}}, t_{\text{start}})$.
3. **Completeness**: For every $t \in \mathbb{T}$, $t$ belongs to either the allowed set or its complement, but never both.
4. **Complexity**: The function evaluates at most 2 integer comparisons, executing in $O(1)$ constant time. $\blacksquare$

---

## 7. Theorem 5: Headless Liveness (Non-Blocking Invariant)

### Statement
When executed in a non-interactive environment (e.g., launchd, systemd, cron, or Siri shortcuts where $\text{isatty}(\text{stdin}) = \text{False}$), the engine halts in finite time $T < \infty$ without awaiting keyboard input:

$$\neg \operatorname{isatty}(\operatorname{stdin}) \implies \delta(S_{\text{INQUIRY}}, \text{HEADLESS}) = S_{\text{TERMINATE}}$$

### Proof
In `ferryman/crossings.py`:
```python
if ctx.is_headless():
    ctx.sleep(...)
    ctx.slow_print(...)
    return
```
When `ctx.is_headless()` evaluates to `True`, the execution branch bypassing `input()` is deterministically taken. The sleep duration is bounded ($20$s for dawn, $5$s for pause, $30$s for dusk in real-time mode, and $0$s in fast mode).
Since `input()` is never invoked, the process cannot block on `sys.stdin.read()`.
Termination is guaranteed within bounded time. $\blacksquare$
