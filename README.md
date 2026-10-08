# Smart Project Assistant AI

A customizable AI teammate for your project: conversational WhatsApp group/DM support, a local web chat, Google Drive documents, PDF answers with sources, persistent decisions, timetables and shared calendars.

**WhatsApp and web are implemented. Discord is a future adapter.** This is a local, single-team MVP—not a hosted service or an official WhatsApp product.

## What it does

- Answers naturally using a configurable identity and project background.
- Searches Drive, receives/uploads files, avoids duplicate uploads and indexes PDFs added directly to Drive.
- Saves explicit project memories, tracks revisions and keeps current project status separate from the system prompt.
- Reads and changes shared Google Calendar events; accepts manual timetables from people without Google Calendar.
- Checks conflicts without treating missing schedules as guaranteed availability.
- Supports public, approved-members-only and owner-only access.
- Lets the owner change permissions conversationally, including rules requiring another person’s approval before an action.
- Sends requested messages and recurring group reminders through a durable local queue.
- Provides a centered light/dark web client that opens ready to chat on the owner’s computer.

Say things like “What’s on our calendar this week?”, “Remember this design decision”, “I have class every Monday from 9 to 11”, or “Require my approval before scheduling meetings.” Ordinary authorized actions execute directly. Critical access changes and configured approval rules require confirmation. The model never receives API keys or OAuth credentials.

## Requirements

- Python **3.12+**, Node.js **24+** and Git.
- A Gemini Developer API key. A personal Gemini subscription is not used as an API login.
- A dedicated WhatsApp bot account and a group containing it.
- Optional Google Drive project folder and Google OAuth Desktop client; optional shared Google Calendar.
- A computer that stays awake while the assistant is needed. 24/7 hosting is intentionally outside this template.

## Quick start

Clone this repository, open a terminal inside it, and create your Python environment:

```sh
python -m venv .venv
```

Activate it with `.venv\Scripts\Activate.ps1` in PowerShell, or `source .venv/bin/activate` on macOS/Linux. Then:

```sh
python -m pip install -r requirements.lock
python -m pip install --no-deps -e .
npm --prefix whatsapp ci --omit=optional
```

Copy `.env.example` to `.env`. Set `ASSISTANT_GEMINI_API_KEY`, your preferred `ASSISTANT_DEFAULT_TIMEZONE` (an IANA name such as `Europe/London`), and `ASSISTANT_WEEK_START` (Monday=0, Sunday=6). API quotas and models vary by account; the example uses a free-tier-compatible configuration without enabling billing.

```sh
python -m app.setup --owner-phone "+15555550100" --owner-name "Alex" --group-name "My team" --assistant-name "Our Assistant" --project-name "Our project"
```

**Replace the example number with your own number, not the bot’s.** Add `--drive-folder-id "YOUR_FOLDER_ID"` when using Drive. Setup creates private local context files, registers the permanent owner and generates the internal bridge credential. Re-running setup preserves existing context edits and the owner identity.

Edit `context/local/identity.json`, `project.json` and `team.json`. Describe what is real, what is proposed and what remains unknown. Generic examples are supplied under `context/examples/`; no original team’s private context is included. See [context and permissions](docs/context.md).

For Drive, follow [Google setup](docs/drive-setup.md). For calendars, follow [Calendar setup](docs/calendar.md). The bot can chat before those integrations are connected.

Run the local services:

```sh
python scripts/run-local.py
```

Open [WhatsApp pairing](http://127.0.0.1:8787/), then use the **bot phone → Linked devices → Link a device**. Open [web chat](http://127.0.0.1:8000/). Keep the terminal open; Ctrl+C stops both services while preserving login. Windows users can alternatively use `scripts/start-local.ps1` and `scripts/stop-local.ps1` for hidden background processes. Do not start both launchers simultaneously or run two copies of the same WhatsApp session.

In WhatsApp, message the bot privately or mention/reply to it in the group. Unknown people are ignored by default. As owner, ask it to approve a number and name, or use the recovery command:

```sh
python -m app.admin approve-whatsapp-member --phone "+15555550200" --name "Teammate"
```

## Identity, permissions and memory

The permanent owner cannot be blocked, removed or replaced by another member. Project role descriptions do not grant administrative authority. Approved members can save memories, maintain their own timetables, read the shared calendar and request event changes by default. Other operations start admin-only; the owner can grant scoped capabilities.

Permission rules can allow, deny or require approval, globally or per member. Requests awaiting approval persist and notify designated approvers through WhatsApp. Any listed approver may approve; current permissions are checked again before execution. “Approve the design review” works without a slash command. Opening public access and appointing admins require owner confirmation.

Project files stay in Drive. SQLite stores users, recent conversation context, structured decisions, index metadata, permissions, schedules and reminders. Private DM history is not automatically shared with groups. Forgetting a decision retires it from active retrieval but preserves audit history. Manual timetable labels remain private in team-conflict answers.

## Models, search and limits

The default conversational model is Gemini 3.5 Flash, with Flash-Lite fallback on quota exhaustion; PDF retrieval uses Flash-Lite. Free model quotas can be small, and each tool-assisted turn can use several model requests. Temporary unavailability remains possible. No billing is enabled by the code, and no fixed zero-cost capacity is promised.

Web search defaults to the no-key DDGS/DuckDuckGo adapter. Gemini uses returned snippets and source links; it does not claim to have read full pages. This unofficial search adapter can be rate-limited. An optional Gemini-grounding adapter is available, but verify model availability and [current Google pricing](https://ai.google.dev/gemini-api/docs/pricing) before enabling it. A personal AI subscription does not replace API quotas.

Defaults: 25 MiB uploads; 20 indexed PDFs/200 MiB; background Drive sync every two minutes; 20 recent turns/seven days; bounded model/tool rounds. Other file formats can be uploaded and located, but PDF is the supported content-indexing format. See [PDF behavior](docs/pdf-answers.md).

## Deployment boundaries

The web UI automatically trusts the local owner machine. **Do not expose it through a public proxy or bind it publicly.** Public/multi-user browser deployment requires proper login, TLS and a different session bootstrap. The Dockerfile is a backend packaging starting point, not a complete always-on deployment.

Baileys is an unofficial WhatsApp Web integration. Account restrictions, protocol changes and maintenance are possible. Normal groups are supported, but every participant can see group answers regardless of sender whitelist. Only one backend worker/instance and one bridge should use the local databases/session.

Reminders stop while the PC is offline; old missed occurrences are skipped. Interrupted message delivery can be uncertain and is not blindly resent. Calendar recurring series edits, full task management, non-PDF content parsing, advanced agents, audio overviews and Discord are not implemented.

## Development

```sh
python -m pytest -q
python -m ruff check app tests scripts/run-local.py
python -m ruff format --check app tests scripts/run-local.py
npm --prefix whatsapp test
```

Tests use isolated databases and mocked external services; they do not send real WhatsApp messages or require your API key. See [architecture and adding a channel](docs/architecture.md), [optional shortcuts](docs/chat-commands.md), [contributing](CONTRIBUTING.md) and [security](SECURITY.md).

Licensed under the existing [MIT license](LICENSE).


## Diagnosing an unavailable reply

An unavailable response is not proof that no action happened. Check the current member list, calendar or saved records before repeating a request that changes them. Action receipts prevent duplicate execution within a request, but a new message is a new request.

The backend logs safe diagnostic categories: `provider_api_error` includes the upstream HTTP status (429 commonly indicates quota), `provider_incomplete` records the finish reason, `provider_tool_limit` reports the bounded tool budget, and `generation_failed` identifies timeouts or provider failures. Logs intentionally omit prompts, API keys, tool arguments and raw exception messages. Windows background-service logs are under the ignored `data/` directory; the foreground launcher displays them in the terminal.

The assistant supports several member additions in one message. For unusually large imports, use smaller batches; the current budget is 16 tool calls per model response and 32 per request, across at most five tool rounds. These limits do not bypass permissions.

See [release notes](CHANGELOG.md) for recent fixes.
