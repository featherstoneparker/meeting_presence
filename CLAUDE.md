# meeting_presence

Reads the current user's presence/status from communication platforms.

## Purpose

Check whether the user is currently in a meeting or otherwise busy, by querying live presence data. Intended for personal automation (e.g. suppress notifications, update a status light, block distractions when in a meeting).

## Platforms

- **Microsoft Teams** — implemented via Microsoft Graph API (`/me/presence`)
- **Slack** — not yet implemented; may be added later via Slack API (`users.getPresence`)

## Auth approach

Uses MSAL `PublicClientApplication` with an interactive browser login as the user (delegated auth). No admin-approved app registration required — uses Microsoft's pre-approved Azure CLI client ID. Tokens are cached locally by MSAL so login is only needed once.

## Structure

```
meeting_presence/
├── CLAUDE.md
├── README.md
├── requirements.txt
├── presence/
│   ├── __init__.py
│   ├── teams.py       # Teams presence via Graph API
│   └── base.py        # Abstract base for future providers (Slack, etc.)
└── main.py            # CLI entry point
```

## Key details

- `client_id`: `04b07795-8ddb-461a-bbee-02f9e1bf7b46` (Azure CLI public client — works on any tenant without registration)
- Scopes: `https://graph.microsoft.com/Presence.Read`
- Token cache: stored in `~/.meeting_presence_token_cache.json`
- Graph endpoint: `GET https://graph.microsoft.com/v1.0/me/presence`

## Presence values

Teams `availability` field returns: `Available`, `Busy`, `DoNotDisturb`, `BeRightBack`, `Away`, `Offline`, `PresenceUnknown`

Teams `activity` field gives more detail: `InACall`, `InAMeeting`, `InAConferenceCall`, `Presenting`, `Focusing`, etc.

## Running

```bash
pip install -r requirements.txt
python main.py
```
