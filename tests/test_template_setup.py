import json
import sys

from app import setup
from app.config import Settings


def test_new_setup_creates_generic_context_without_overwriting_edits(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "setup",
            "--owner-phone",
            "+15555550100",
            "--owner-name",
            "Alex",
            "--group-name",
            "Team",
            "--project-name",
            "Example robot",
        ],
    )
    setup.main()
    identity = tmp_path / "context/local/identity.json"
    assert json.loads(identity.read_text())["creator"] == "Alex"
    assert json.loads((tmp_path / "data/team.json").read_text())["owner_phone"] == "15555550100"
    assert Settings().bridge_token.get_secret_value()
    identity.write_text('{"name":"Customized assistant"}')
    setup.main()
    assert json.loads(identity.read_text())["name"] == "Customized assistant"
