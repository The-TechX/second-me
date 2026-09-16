import tempfile, unittest
from pathlib import Path
from second_me.memory.store import MemoryStore

class StoreTest(unittest.TestCase):
    def test_index_search_and_neighbors(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); vault = root / "vault"; vault.mkdir()
            (vault / "a.md").write_text("---\nid: a\ntitle: Alpha\nconcepts: [memory]\n---\n# Alpha\n[[Beta]] memory", encoding="utf-8")
            (vault / "b.md").write_text("---\nid: b\ntitle: Beta\nconcepts: [memory]\n---\n# Beta\nmemory", encoding="utf-8")
            store = MemoryStore(vault, root / "db.sqlite")
            self.assertEqual(store.index(), 2)
            self.assertEqual({x["id"] for x in store.search("memory")}, {"a", "b"})
            self.assertEqual(store.neighbors("a")[0]["id"], "b")

if __name__ == "__main__": unittest.main()
