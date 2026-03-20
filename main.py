"""
TODO CLI アプリ

使い方:
    python main.py add "タスク内容"   # タスクを追加
    python main.py list               # 未完了タスクを表示
    python main.py list --all         # 全タスクを表示
    python main.py done <id>          # タスクを完了にする
    python main.py delete <id>        # タスクを削除する
    python main.py clear              # 完了済みタスクを全削除
"""

import argparse
import sys

import todo_app

# ANSI カラー
GREEN  = "\033[32m"
RED    = "\033[31m"
YELLOW = "\033[33m"
CYAN   = "\033[36m"
GRAY   = "\033[90m"
BOLD   = "\033[1m"
RESET  = "\033[0m"


def print_todos(rows) -> None:
    if not rows:
        print(f"{GRAY}タスクはありません{RESET}")
        return

    print()
    for row in rows:
        status = f"{GREEN}✓{RESET}" if row["done"] else f"{YELLOW}○{RESET}"
        title  = f"{GRAY}{row['title']}{RESET}" if row["done"] else row["title"]
        date   = f"{GRAY}{row['created'][:10]}{RESET}"
        print(f"  {status} {BOLD}[{row['id']:>3}]{RESET}  {title}  {date}")
    print()


def cmd_add(args) -> None:
    title = " ".join(args.title)
    todo_id = todo_app.add_todo(title)
    print(f"{GREEN}追加しました{RESET}  [{todo_id}] {title}")


def cmd_list(args) -> None:
    rows = todo_app.list_todos(show_all=args.all)
    label = "全タスク" if args.all else "未完了タスク"
    print(f"{CYAN}{BOLD}{label} ({len(rows)}件){RESET}", end="")
    print_todos(rows)


def cmd_done(args) -> None:
    if todo_app.mark_done(args.id):
        print(f"{GREEN}完了しました{RESET}  [{args.id}]")
    else:
        print(f"{RED}該当するタスクが見つかりません: {args.id}{RESET}", file=sys.stderr)
        sys.exit(1)


def cmd_delete(args) -> None:
    if todo_app.delete_todo(args.id):
        print(f"{RED}削除しました{RESET}  [{args.id}]")
    else:
        print(f"{RED}該当するタスクが見つかりません: {args.id}{RESET}", file=sys.stderr)
        sys.exit(1)


def cmd_clear(args) -> None:
    count = todo_app.clear_done()
    print(f"{RED}完了済みタスクを {count} 件削除しました{RESET}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="todo",
        description="シンプルなCLI TODOアプリ",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # add
    p_add = sub.add_parser("add", help="タスクを追加する")
    p_add.add_argument("title", nargs="+", help="タスクの内容")
    p_add.set_defaults(func=cmd_add)

    # list
    p_list = sub.add_parser("list", help="タスクを表示する")
    p_list.add_argument("--all", "-a", action="store_true", help="完了済みも含めて表示")
    p_list.set_defaults(func=cmd_list)

    # done
    p_done = sub.add_parser("done", help="タスクを完了にする")
    p_done.add_argument("id", type=int, help="タスクID")
    p_done.set_defaults(func=cmd_done)

    # delete
    p_del = sub.add_parser("delete", help="タスクを削除する")
    p_del.add_argument("id", type=int, help="タスクID")
    p_del.set_defaults(func=cmd_delete)

    # clear
    p_clear = sub.add_parser("clear", help="完了済みタスクを全削除する")
    p_clear.set_defaults(func=cmd_clear)

    return parser


def main() -> None:
    todo_app.init_db()
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
