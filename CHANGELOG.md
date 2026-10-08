# Release notes

## 2026-10-09 — Reply context and reliability review

- Port quoted WhatsApp replies, group-name discovery and optional multiple chat credentials.
- Prevent duplicate plain-message retries after uncertain quoted sends; store minimal quote context.
- Preserve disabled groups during discovery and require explicit registration for new groups in whitelist mode. Validate group IDs and bound sync batches.
- Bound key rotation, honor per-model cooldowns, redact credential settings, and preserve configured daily request caps.
- Pin PDF indexing/retrieval to one credential rather than rotating across project-owned stores.
- Add regression tests covering these behaviors and document configuration and limitations.

## 2026-10-08 — Public template fixes

- Allow multi-person requests with up to 16 tool calls per model response, within a 32-call request budget. Every action still passes the same backend permissions and approval rules.
- Add WhatsApp-specific presentation guidance and formatting for headings, bold, bullets and source links; preserve code blocks and technical citations.
- Clarify exclusive Calendar end dates to avoid displaying an extra day for all-day events and weekly ranges.
- Record safe failure diagnostics (error category, HTTP status, tool counts) without logging prompts, credentials, tool arguments or raw exception bodies.
- Wait for recorded Windows service processes to exit before returning from the stop script.

This is a local single-team MVP. Provider quotas, upstream outages and unofficial WhatsApp session changes can still interrupt service. Review the README and SECURITY.md before deployment. Discord and 24/7 hosting remain future work.
