from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

@dataclass
class Memory:
    id: str
    title: str
    content: str
    path: Path
    kind: str = "episodic"
    event_at: datetime | None = None
    importance: float = 0.5
    concepts: list[str] = field(default_factory=list)
    entities: list[str] = field(default_factory=list)
    links: list[str] = field(default_factory=list)
