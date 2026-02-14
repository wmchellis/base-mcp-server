# MCP Server — Architecture Decisions

This document records the key decisions made when designing this MCP server,
along with the alternatives considered and the trade-offs involved. It should
be updated whenever a significant decision is revisited or reversed.

---

## Decision 1: Operating System — Ubuntu 25.10 → 26.04 LTS

**Decision:** Start on Ubuntu 25.10 (interim release), then upgrade to 26.04 LTS when available (April 2026).

### Alternatives Considered

| Option | Pros | Cons |
|---|---|---|
| **Ubuntu 25.10** (chosen starting point) | Latest kernel and packages; good hardware support; familiar tooling | Interim release — EOL ~July 2026; interim-to-LTS upgrades can be messy |
| **Ubuntu 24.04 LTS** | Stable right now; 5-year LTS support; proven upgrade path to 26.04 LTS | Older kernel; may miss newer driver/hardware support |
| **Ubuntu 26.04 LTS** (target) | 5-year LTS; cutting-edge; clean install from day one | Not released yet (April 2026); first month post-release often has bugs |
| **Debian Stable** | Extremely stable; minimal bloat; conservative packages | Older packages; smaller community tutorials for MCP/AI tooling |
| **Rocky Linux / AlmaLinux** | Enterprise-grade stability; RHEL compatibility | Smaller ecosystem for Python/AI tooling; fewer tutorials |

### Rationale
25.10 provides the most current packages while 26.04 LTS is being finalized. The upgrade path is tight (~6 months) but acceptable. A fresh install of 26.04 LTS is preferred over in-place upgrade from 25.10 if downtime is tolerable.

---

## Decision 2: Programming Language — Python

**Decision:** Python 3.11+ as the primary language for the MCP server and all integrations.

### Alternatives Considered

| Option | Pros | Cons |
|---|---|---|
| **Python** (chosen) | Best-in-class PDF/data libraries; native fit with Kali tooling; mature Google and Proxmox clients; excellent async support | Slightly slower startup; type safety requires discipline |
| **TypeScript/Node.js** | Strong MCP SDK support; fast I/O; good for concurrent web-facing servers | PDF libraries far weaker than Python's; Proxmox/Kali ecosystem thinner; less natural for data analysis |
| **Go** | Excellent performance; single binary deployment; strong concurrency | Minimal MCP tooling; significantly more verbose for rapid integration work |

### Rationale
The integration targets (PDF processing, Google Drive, Proxmox API, Kali tools) all have significantly stronger Python ecosystems. Python's async capabilities (`asyncio`) are sufficient for this server's I/O profile.

---

## Decision 3: PDF Processing Libraries

**Decision:** Use `pymupdf` (fitz) as primary, `pdfplumber` for table extraction, and `pypdf` for form filling.

### Alternatives Considered

| Option | Use Case | Pros | Cons |
|---|---|---|---|
| **pymupdf / fitz** (chosen) | Text extraction, rendering, annotation | Very fast; C-based; excellent quality | GPL/AGPL license (check if commercial use needed) |
| **pdfplumber** (chosen) | Table extraction | Layout-aware; handles complex tables well | Slower than pymupdf for pure text |
| **pypdf** (chosen) | AcroForm filling | Pure Python; lightweight; good form support | Less powerful for extraction |
| **pdfminer.six** | Text extraction | Good layout analysis | Slow; complex API |
| **reportlab** | PDF generation | Full PDF creation from scratch | Write-only; not for reading/editing existing PDFs |
| **camelot** | Table extraction | Very accurate tables | Heavy dependencies (ghostscript required) |

### Rationale
No single PDF library excels at everything. The three-library approach covers reading, table extraction, and form filling with minimal overlap.

---

## Decision 4: Google Drive Authentication — Service Account

**Decision:** Use a Google Service Account (JSON key file) rather than OAuth 2.0 with user consent flow.

### Alternatives Considered

| Option | Pros | Cons |
|---|---|---|
| **Service Account** (chosen) | No browser/user interaction; perfect for server automation; persistent credentials | Requires sharing Drive folders explicitly with the SA email; cannot access user's personal Drive directly |
| **OAuth 2.0 (user consent flow)** | Access to user's own Drive natively | Requires browser redirect; tokens expire; refresh token management complexity on a headless server |
| **API Key** | Simple | Drive API does not support API key auth for user data access |

### Rationale
A Service Account eliminates the need for any interactive auth flow, which is essential for a background server. The trade-off of explicitly sharing folders with the SA email is acceptable and actually improves auditability.

---

## Decision 5: Proxmox Authentication — API Tokens

**Decision:** Use Proxmox API Tokens (user + token name + token secret) rather than username/password.

### Alternatives Considered

| Option | Pros | Cons |
|---|---|---|
| **API Token** (chosen) | Revocable without changing user password; granular per-token permissions; no session management needed | Slightly more setup in Proxmox UI |
| **Username/Password** | Simple | Must store raw password; no fine-grained revocation; sessions expire requiring re-auth logic |
| **Ticket-based auth** | Standard Proxmox flow | Short-lived tickets (2h); requires re-auth loop in long-running server |

### Rationale
API tokens are the secure, idiomatic way to authenticate automated systems against Proxmox VE. They can be scoped to minimum permissions (PVEAuditor for read-only, PVEVMAdmin for power operations) and revoked independently.

---

## Decision 6: Kali Linux Deployment — VM/LXC on Proxmox

**Decision:** Run Kali as a VM or LXC container on Proxmox, accessed by the MCP server via SSH.

### Alternatives Considered

| Option | Pros | Cons |
|---|---|---|
| **VM/LXC on Proxmox via SSH** (chosen) | Isolated from MCP server; snapshotable; network-segmentable; standard SSH is well-understood | Adds SSH hop; slightly more latency per command |
| **Kali installed natively on MCP server host** | Lowest latency; no SSH needed | Kali tools run with MCP server's privileges; hard to isolate; Kali repos can conflict with Ubuntu packages |
| **Docker container (kalilinux/kali-rolling)** | Lightweight; reproducible; easy to rebuild | Kali tools often require raw socket access / capabilities that complicate Docker security; no persistent state easily |
| **Separate bare-metal Kali machine** | Maximum isolation | Cost; requires additional hardware; harder to automate |

### Rationale
Running Kali as a Proxmox VM/LXC leverages infrastructure already in scope, provides strong isolation, and can be snapshotted before/after operations. SSH access with key-based auth and a restricted non-root user gives the right security posture.

---

## Decision 7: MCP Transport — stdio

**Decision:** Use the stdio transport (stdin/stdout) for the MCP server, not HTTP/SSE.

### Alternatives Considered

| Option | Pros | Cons |
|---|---|---|
| **stdio** (chosen) | Simplest; no port/firewall management; natural for local Claude Desktop integration; MCP SDK default | Single client at a time; not suitable for multi-client or web-facing deployments |
| **HTTP + SSE** | Supports multiple concurrent clients; web-accessible; can be load-balanced | More infrastructure (nginx, TLS, auth); more complex to set up |

### Rationale
The primary use case is a local or LAN-accessible MCP server serving a single Claude client. stdio is simpler, safer (no exposed port), and the path of least resistance for integration with Claude Desktop. Can be revisited if multi-client support becomes a requirement.

---

## Decision 8: Process Management — systemd

**Decision:** Use systemd to manage the MCP server process lifecycle.

### Alternatives Considered

| Option | Pros | Cons |
|---|---|---|
| **systemd** (chosen) | Native to Ubuntu; automatic start on boot; journald integration; hardening options (NoNewPrivileges, ProtectSystem, etc.) | Config is declarative/verbose; slightly more friction to edit than a script |
| **pm2** | Easy to use; good for Node.js; web dashboard available | Extra dependency; primarily Node.js-oriented; redundant with systemd on Linux |
| **Docker** | Full isolation; reproducible; restart policies built-in | Overkill for a single-service Python app; adds complexity; stdio transport awkward through Docker |
| **supervisor** | Simple; works well for Python | Older project; systemd supersedes it on modern Ubuntu |

### Rationale
systemd is the correct native choice for a long-running daemon on Ubuntu. The `ProtectSystem`, `NoNewPrivileges`, and `PrivateTmp` options provide meaningful security hardening with zero extra dependencies.

---

## Decision 9: Build Order

**Decision:** Scaffold → PDF → Google Drive → Proxmox → Kali

### Rationale

| Step | Reason |
|---|---|
| Scaffold first | Validates the full MCP loop before any integration complexity |
| PDF second | Self-contained; no external auth; fast feedback loop |
| Google Drive third | Service Account setup has human latency (approval/sharing); start early |
| Proxmox fourth | Requires network access to Proxmox; more integration surface area |
| Kali last | Most security-sensitive; patterns (auth, logging, allowlisting) should be proven before opening tool execution |

---

*Last updated: Initial architecture session*
