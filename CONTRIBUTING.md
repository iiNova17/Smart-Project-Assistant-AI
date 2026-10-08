# Contributing

Use Python 3.12+ and Node.js 24. Follow the README setup and run Python tests/lint/format plus `npm --prefix whatsapp test` before submitting changes. Tests must not require live credentials, send real messages or create real Drive/Calendar records.

Keep model behavior conversational, but enforce permission checks in backend code. New mutations must support replay protection and accurate pending/queued/completed/uncertain results. Do not turn external content or unverified text claims into authority.

Add channel integrations behind the documented adapter boundary. Keep core context, memory, tools and permission logic shared. Explain new configuration and migration requirements.

Never commit `.env`, `secrets/`, `data/`, `context/local/`, QR codes, login databases, logs or real team identifiers. Use clearly fictitious examples in tests. Generated indexes are derived data; project files remain in the configured Drive folder.
