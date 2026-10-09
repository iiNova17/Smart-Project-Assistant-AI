# Release notes

## 2026-10-09 — WhatsApp image understanding

- Stop dropping image messages; preserve photo captions and mentions.
- Pass validated direct/quoted images to Gemini as multimodal content.
- Bound file size and pixel count, correct orientation, strip metadata, and clean temporary media.
- Explain image failures; preserve quiet-group rules and authenticated sender identity.
- Add image transport, decoding, provider mapping and channel-trigger regression tests.


## 2026-10-09 — Actual sticker delivery

- Add `sticker_send` for saved stickers in the current WhatsApp conversation.
- Deliver binary WebP media through the authenticated backend and durable WhatsApp queue, with current permissions, private-asset checks, integrity validation and bounded fetch retries.
- Deduplicate repeated tool calls within a request; suppress replay after uncertain sends.
- Add backend/media-route and WhatsApp media-send regression tests.


## 2026-10-09 — Scheduled tasks, reply context, stickers, and voice notes

- **Authoritative speaker identification**: Trace participant identity directly from the WhatsApp envelope through phone/LID mapping, authorization, conversation history, and tool execution. Quoting another user's message never inherits their identity or permissions.
- **Incoming reply context**: Structured `ReplyContext` (message ID, author, content type, text/caption, attachment) injected as untrusted reference material, isolated from executable instructions.
- **Durable scheduled tasks**: SQLite-backed `TaskScheduler` (`scheduled_tasks`, `task_proposals`, `task_executions`) supporting reminders, messages, and structured summaries with atomic occurrence claims and uncertain-send handling. Scheduled reports/calendar writes remain unimplemented.
- **Preview-and-confirm workflow**: Natural-language scheduling requests present an exact preview requiring explicit confirmation before activation; stale proposals expire automatically.
- **Lifecycle permission checks**: Authoritative permissions rechecked at proposal, confirmation, tick, and execution. Blocked or revoked users cannot execute scheduled actions. Missed runs overdue by >15 minutes after offline downtime are suppressed.
- **Reusable stickers**: Local disk storage and SQLite registry with SHA-256 deduplication, usage guidance, and role-based deletion protection.
- **Voice-note understanding**: Multimodal Gemini audio transcription with automatic cleanup of temporary audio files. Language accuracy still needs live validation.

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


### Follow-up audit corrections

Fixed voice-note spool filenames and attachment-path validation; isolated sticker uploads by request; prevented private-sticker metadata takeover; added task capability checks, approval requests, separate confirmation, atomic proposal consumption, privacy-filtered history, reconfirmation after edits and interrupted-execution recovery. Audio processing is bounded and logs error categories without raw provider errors. Incomplete scheduled handlers now fail explicitly instead of claiming success. Legacy reminders and sticker access now honor current grants; recurring tasks survive long offline gaps.
