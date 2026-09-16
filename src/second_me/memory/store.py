import json
import re
import sqlite3
from datetime import datetime
from pathlib import Path
import yaml
from .models import Memory

WIKILINK = re.compile(r"\[\[([^\]]+)\]\]")

class MemoryStore:
    """Markdown is truth; SQLite is a disposable navigation index."""

    def __init__(self, vault: Path, db: Path):
        self.vault, self.db = Path(vault), Path(db)
        self.conn = sqlite3.connect(self.db)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("""CREATE TABLE IF NOT EXISTS memories (
            id TEXT PRIMARY KEY, title TEXT NOT NULL, path TEXT NOT NULL,
            kind TEXT NOT NULL, event_at TEXT, importance REAL NOT NULL,
            content TEXT NOT NULL, concepts TEXT NOT NULL, entities TEXT NOT NULL,
            links TEXT NOT NULL
        )""")
        self.conn.execute("CREATE VIRTUAL TABLE IF NOT EXISTS memory_fts USING fts5(id UNINDEXED, title, content, concepts, entities)")

    def _parse(self, path: Path) -> Memory:
        raw = path.read_text(encoding="utf-8")
        meta, body = {}, raw
        if raw.startswith("---\n"):
            _, header, body = raw.split("---", 2)
            meta = yaml.safe_load(header) or {}
        title = meta.get("title") or next((x[2:].strip() for x in body.splitlines() if x.startswith("# ")), path.stem)
        event_at = datetime.fromisoformat(str(meta["date"])) if meta.get("date") else None
        return Memory(
            id=str(meta.get("id", path.stem)), title=title, content=body.strip(), path=path,
            kind=str(meta.get("type", "episodic")), event_at=event_at,
            importance=float(meta.get("importance", 0.5)),
            concepts=list(meta.get("concepts", [])), entities=list(meta.get("entities", [])),
            links=WIKILINK.findall(body),
        )

    def index(self) -> int:
        self.conn.execute("DELETE FROM memories")
        self.conn.execute("DELETE FROM memory_fts")
        count = 0
        for path in sorted(self.vault.rglob("*.md")):
            memory = self._parse(path)
            values = (memory.id, memory.title, str(path.relative_to(self.vault)), memory.kind,
                      memory.event_at.isoformat() if memory.event_at else None, memory.importance,
                      memory.content, json.dumps(memory.concepts), json.dumps(memory.entities), json.dumps(memory.links))
            self.conn.execute("INSERT INTO memories VALUES (?,?,?,?,?,?,?,?,?,?)", values)
            self.conn.execute("INSERT INTO memory_fts VALUES (?,?,?,?,?)", (memory.id, memory.title, memory.content, " ".join(memory.concepts), " ".join(memory.entities)))
            count += 1
        self.conn.commit()
        return count

    def search(self, query: str, limit: int = 10):
        rows = self.conn.execute("""SELECT m.*, bm25(memory_fts) AS rank FROM memory_fts
            JOIN memories m ON m.id=memory_fts.id WHERE memory_fts MATCH ? ORDER BY rank LIMIT ?""", (query, limit)).fetchall()
        return [dict(row) for row in rows]

    def get(self, memory_id: str):
        row = self.conn.execute("SELECT * FROM memories WHERE id=?", (memory_id,)).fetchone()
        return dict(row) if row else None

    def neighbors(self, memory_id: str):
        current = self.get(memory_id)
        if not current: return []
        concepts, entities, links = map(set, map(json.loads, (current["concepts"], current["entities"], current["links"])))
        scored = []
        for row in self.conn.execute("SELECT * FROM memories WHERE id != ?", (memory_id,)):
            score = len(concepts & set(json.loads(row["concepts"]))) + len(entities & set(json.loads(row["entities"]))) + len(links & set(json.loads(row["links"])))
            if row["title"] in links: score += 2
            if score: scored.append((score, dict(row)))
        return [r for _, r in sorted(scored, key=lambda x: x[0], reverse=True)]
