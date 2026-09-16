import argparse, json
from pathlib import Path
from .memory.store import MemoryStore

def main():
    p = argparse.ArgumentParser(prog="second-me")
    p.add_argument("--vault", default="vault")
    p.add_argument("--db", default="second-me.db")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("index")
    s = sub.add_parser("search"); s.add_argument("query")
    g = sub.add_parser("get"); g.add_argument("id")
    n = sub.add_parser("neighbors"); n.add_argument("id")
    args = p.parse_args(); store = MemoryStore(Path(args.vault), Path(args.db))
    if args.cmd == "index": print(f"Indexed {store.index()} memories")
    elif args.cmd == "search": print(json.dumps(store.search(args.query), indent=2))
    elif args.cmd == "get": print(json.dumps(store.get(args.id), indent=2))
    elif args.cmd == "neighbors": print(json.dumps(store.neighbors(args.id), indent=2))
