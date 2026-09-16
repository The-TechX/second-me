# second-me

A small experiment in persistent, navigable memory for humans and agents.

## V1

- Markdown vault is the source of truth and can be opened with Obsidian.
- SQLite + FTS5 is a disposable local index.
- Memories carry metadata, concepts, entities, and `[[wikilinks]]`.
- Navigation is progressive: `search` → `get` / `neighbors`.
- No LLM, skills, tools, or agent runtime is required.
- Real `*.md` vault content is ignored by Git; only `*.example.md` fixtures are committed.

## Try it

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
cp vault/memories/project-kickoff.example.md vault/memories/project-kickoff.md
cp vault/memories/retrieval-design.example.md vault/memories/retrieval-design.md
cp vault/concepts/memory-architecture.example.md vault/concepts/memory-architecture.md
second-me index
second-me search memory
second-me neighbors mem-project-kickoff
```

Delete `second-me.db` at any time and rebuild it with `second-me index`.

## Next experiments

The storage boundary intentionally leaves room for embeddings/pgvector, working memory, active threads, progressive `peek`/`expand` recall, and consolidation without changing the Markdown source of truth.
