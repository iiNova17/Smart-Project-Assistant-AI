# Security boundaries

This template is for a trusted local computer and a small approved team. The local browser bootstrap grants the configured owner a session without password entry and must not be exposed through an internet-facing proxy. The internal bridge credential remains backend-only. Public deployment requires new browser authentication, TLS, request limits and operational review.

WhatsApp sender identity comes from provider mappings, not a message claiming a role. Permanent-owner and capability checks run in the backend. Approval requests are scoped to a specific action and rechecked against current permissions. Context files and model outputs cannot grant privileges.

Google OAuth refresh tokens, Gemini keys and WhatsApp credentials remain under ignored local paths. Drive OAuth requests broad Google scope because the app must discover pre-existing project files; the app then enforces the configured project-root boundary. Protect local files and backups. Do not connect calendars/files you do not intend the authorized team to use.

The unofficial WhatsApp and search adapters have maintenance and availability risks. Do not treat a no-conflict result as proof of complete availability, or a citation as proof that an engineering interpretation is correct.

Report suspected vulnerabilities privately to the repository owner through GitHub’s private reporting feature if available. Do not include live credentials or team data in public issues. If a credential is exposed, revoke it at its provider and replace the local session/key; deleting a Git commit alone does not revoke it.
