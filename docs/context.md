# Customize your assistant

Setup creates three ignored files in `context/local/`: `identity.json` for the assistant name/creator/style, `project.json` for background and authority rules, and `team.json` for team descriptions. They reload for each model turn. Edit them locally or ask an authorized admin to update them through chat. Generic examples are provided; no prior deployment’s project facts are embedded in the template.

Keep mutable status out of permanent background text. Work-package state and history live in SQLite; ask the assistant to record which packages are active, planned, awaiting planning, blocked or completed. Component candidates are not finalized merely by mentioning them.

The context files do not grant permissions. Authenticated sender identity and backend records determine authority. Live modes are public, whitelist (default) and owner; blocks override public access. Group triggers are mention/reply/recognized optional shortcut or document, unless changed to all.

Capabilities are memory, personal_schedule, calendar_write, members, settings, groups, reminders, drive_write, project_status, context, send_message, stickers and schedule_manage_others. Rules use a global `*` subject or a member’s canonical phone; member rules override global ones. Only the permanent owner changes grants/rules. A scoped capability does not appoint an admin or give access to another person’s private timetable. Supported scheduled reminders, messages and structured summaries enforce their required capabilities at confirmation, execution and delivery. Scheduled calendar writes and reports are not implemented. Sticker grants can be allowed or denied; a designated-approver sticker workflow is not implemented and such requests are blocked.

Approval rules hold exact actions for 24 hours and message designated people. Any listed approver can approve; an all-approvers-must-agree rule is not implemented. Current permissions and account access are rechecked before execution. Critical public-mode/admin-promotion changes require owner confirmation.

Recent context, durable decisions and current status are distinct stores. An explicit memory request persists a shared fact; normal conversation does not automatically become a decision. Replacement preserves revision history. Forgetting retires the active decision; it is not a permanent erasure of the audit record. Manual schedules are stored separately, with private labels omitted from team availability responses.

Calendar subscriptions and timetable imports live in structured schedule-source records. They are not project decisions. Members manage their own records under personal_schedule; changes for others additionally require schedule_manage_others. Imports and edits need a separate confirmation, followed by any configured permission approval. See [availability](availability.md).
