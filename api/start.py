# usr/plugins/qmd/api/start.py
"""POST /api/plugins/qmd/start — explicitly start the bridge subprocess."""
from __future__ import annotations

from helpers.api import ApiHandler, Input, Output, Request
from helpers import plugins


class Start(ApiHandler):

    @classmethod
    def get_methods(cls) -> list[str]:
        return ["POST"]

    async def process(self, input: Input, request: Request) -> Output:
        from usr.plugins.qmd.helpers.client_access import get_or_create_global_client

        # Read db_path from plugin config (no agent context needed)
        config = plugins.get_plugin_config("qmd") or {}
        db_path = config.get("db_path") or None

        try:
            client = await get_or_create_global_client(db_path=db_path)
            running = client.is_running()
            pid = client._proc.pid if running and client._proc else None
            return {"ok": True, "running": running, "pid": pid}
        except Exception as exc:
            return {"ok": False, "error": str(exc)}
