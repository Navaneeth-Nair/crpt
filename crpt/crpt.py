import argparse
import os
import sys

# Add the parent directory to Python path to ensure crpt can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import modules with proper package qualification
from crpt.core import repo, index, commit, push, pull, branch, checkout

def main():
    parser = argparse.ArgumentParser(prog='crpt', description="Custom version control tool")
    subparsers = parser.add_subparsers(dest='command')

    # crpt init
    subparsers.add_parser('init')

    # crpt add <file>
    add_parser = subparsers.add_parser('add')
    add_parser.add_argument('file', help="File to stage")

    # crpt commit -m "message"
    commit_parser = subparsers.add_parser('commit')
    commit_parser.add_argument('-m', '--message', required=True, help="Commit message")

    subparsers.add_parser('push')
    subparsers.add_parser("pull")

    branch_parser = subparsers.add_parser('branch')
    branch_parser.add_argument('name', nargs='?', help='Branch name to create')

    checkout_parser = subparsers.add_parser('checkout')
    checkout_parser.add_argument('name', help='Branch name to switch to')

    args = parser.parse_args()

    if args.command == 'init':
        repo.init_repo()
    elif args.command == 'add':
        index.stage_file(args.file)
    elif args.command == 'commit':
        commit.create_commit(args.message)
    elif args.command == 'push':
        push.push_to_remote()
    elif args.command == 'pull':
        pull.pull_from_remote()
    elif args.command == 'branch':
        if args.name:
            branch.create_branch(args.name)
        else:
            branch.list_branches()
    elif args.command == 'checkout':
        checkout.checkout_branch(args.name)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
