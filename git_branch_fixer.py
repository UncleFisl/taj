#!/usr/bin/env python3
"""
Git Branch Name Fixer
أداة لإصلاح وتنظيم أسماء فروع Git

Features:
- Validate branch names against naming conventions
- Suggest corrected branch names
- Automatically rename branches
- Support multiple naming conventions
"""

import re
import subprocess
import sys
from typing import List, Tuple, Optional
from enum import Enum


class NamingConvention(Enum):
    """Git branch naming conventions"""
    GITFLOW = "gitflow"
    FEATURE_SLASH = "feature_slash"
    KEBAB_CASE = "kebab_case"
    SNAKE_CASE = "snake_case"


class GitBranchFixer:
    """Main class for fixing Git branch names"""

    def __init__(self, convention: NamingConvention = NamingConvention.GITFLOW):
        self.convention = convention

    def get_all_branches(self, include_remote: bool = False) -> List[str]:
        """Get all Git branches"""
        try:
            cmd = ["git", "branch"]
            if include_remote:
                cmd.append("-a")

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )

            branches = []
            for line in result.stdout.split('\n'):
                line = line.strip()
                if line:
                    # Remove the '*' indicator for current branch
                    branch = line.lstrip('* ').strip()
                    # Skip remote HEAD references
                    if 'HEAD ->' not in branch:
                        branches.append(branch)

            return branches
        except subprocess.CalledProcessError as e:
            print(f"Error getting branches: {e}")
            return []

    def validate_branch_name(self, branch_name: str) -> Tuple[bool, Optional[str]]:
        """
        Validate branch name against the selected convention
        Returns: (is_valid, error_message)
        """
        # Common rules for all conventions
        if not branch_name:
            return False, "Branch name cannot be empty"

        # Cannot start or end with /
        if branch_name.startswith('/') or branch_name.endswith('/'):
            return False, "Branch name cannot start or end with '/'"

        # Cannot contain consecutive slashes
        if '//' in branch_name:
            return False, "Branch name cannot contain consecutive slashes '//'"

        # Cannot contain spaces
        if ' ' in branch_name:
            return False, "Branch name cannot contain spaces"

        # Cannot contain special characters
        invalid_chars = ['~', '^', ':', '?', '*', '[', '\\', '..']
        for char in invalid_chars:
            if char in branch_name:
                return False, f"Branch name cannot contain '{char}'"

        # Convention-specific validation
        if self.convention == NamingConvention.GITFLOW:
            return self._validate_gitflow(branch_name)
        elif self.convention == NamingConvention.FEATURE_SLASH:
            return self._validate_feature_slash(branch_name)
        elif self.convention == NamingConvention.KEBAB_CASE:
            return self._validate_kebab_case(branch_name)
        elif self.convention == NamingConvention.SNAKE_CASE:
            return self._validate_snake_case(branch_name)

        return True, None

    def _validate_gitflow(self, branch_name: str) -> Tuple[bool, Optional[str]]:
        """Validate GitFlow naming convention"""
        valid_prefixes = ['feature/', 'bugfix/', 'hotfix/', 'release/', 'support/', 'main', 'master', 'develop']

        # Check if it's a main branch
        if branch_name in ['main', 'master', 'develop']:
            return True, None

        # Check if it has a valid prefix
        has_valid_prefix = any(branch_name.startswith(prefix) for prefix in valid_prefixes)
        if not has_valid_prefix:
            return False, f"Branch must start with one of: {', '.join(valid_prefixes)}"

        # Check the part after the prefix
        for prefix in valid_prefixes:
            if branch_name.startswith(prefix) and '/' in prefix:
                suffix = branch_name[len(prefix):]
                if not suffix:
                    return False, f"Branch name cannot be just '{prefix}'"
                # Suffix should be lowercase with hyphens or slashes
                if not re.match(r'^[a-z0-9\-/]+$', suffix):
                    return False, "Branch suffix should be lowercase with hyphens or slashes only"

        return True, None

    def _validate_feature_slash(self, branch_name: str) -> Tuple[bool, Optional[str]]:
        """Validate feature/name convention"""
        if '/' not in branch_name:
            return False, "Branch name should contain '/' (e.g., feature/my-feature)"

        parts = branch_name.split('/')
        if len(parts) < 2:
            return False, "Branch name should have format: type/description"

        return True, None

    def _validate_kebab_case(self, branch_name: str) -> Tuple[bool, Optional[str]]:
        """Validate kebab-case convention"""
        if not re.match(r'^[a-z0-9\-/]+$', branch_name):
            return False, "Branch name should be lowercase with hyphens (kebab-case)"

        return True, None

    def _validate_snake_case(self, branch_name: str) -> Tuple[bool, Optional[str]]:
        """Validate snake_case convention"""
        if not re.match(r'^[a-z0-9_/]+$', branch_name):
            return False, "Branch name should be lowercase with underscores (snake_case)"

        return True, None

    def suggest_fix(self, branch_name: str) -> str:
        """Suggest a fixed branch name"""
        fixed = branch_name

        # Remove leading/trailing slashes
        fixed = fixed.strip('/')

        # Replace spaces with hyphens
        fixed = fixed.replace(' ', '-')

        # Remove consecutive slashes
        while '//' in fixed:
            fixed = fixed.replace('//', '/')

        # Remove invalid characters
        fixed = re.sub(r'[~^:?\*\[\]\\]', '', fixed)
        fixed = fixed.replace('..', '')

        # Convert to lowercase
        fixed = fixed.lower()

        # Apply convention-specific fixes
        if self.convention == NamingConvention.GITFLOW:
            fixed = self._fix_gitflow(fixed)
        elif self.convention == NamingConvention.KEBAB_CASE:
            # Convert underscores to hyphens (except in prefixes)
            parts = fixed.split('/')
            parts = [part.replace('_', '-') for part in parts]
            fixed = '/'.join(parts)
        elif self.convention == NamingConvention.SNAKE_CASE:
            # Convert hyphens to underscores (except in prefixes)
            parts = fixed.split('/')
            parts = [part.replace('-', '_') for part in parts]
            fixed = '/'.join(parts)

        return fixed

    def _fix_gitflow(self, branch_name: str) -> str:
        """Fix branch name according to GitFlow"""
        # If it's a main branch, keep it as is
        if branch_name in ['main', 'master', 'develop']:
            return branch_name

        # Check if it already has a valid prefix
        valid_prefixes = ['feature/', 'bugfix/', 'hotfix/', 'release/', 'support/']
        has_prefix = any(branch_name.startswith(prefix) for prefix in valid_prefixes)

        if not has_prefix:
            # Try to guess the prefix based on common keywords
            if any(keyword in branch_name for keyword in ['feat', 'feature', 'add', 'implement']):
                branch_name = 'feature/' + branch_name
            elif any(keyword in branch_name for keyword in ['bug', 'fix', 'issue']):
                branch_name = 'bugfix/' + branch_name
            elif 'hotfix' in branch_name:
                branch_name = 'hotfix/' + branch_name
            elif 'release' in branch_name:
                branch_name = 'release/' + branch_name
            else:
                # Default to feature
                branch_name = 'feature/' + branch_name

        # Clean up the suffix
        for prefix in valid_prefixes:
            if branch_name.startswith(prefix):
                suffix = branch_name[len(prefix):]
                # Convert underscores to hyphens in suffix
                suffix = suffix.replace('_', '-')
                branch_name = prefix + suffix
                break

        return branch_name

    def rename_branch(self, old_name: str, new_name: str, force: bool = False) -> bool:
        """Rename a Git branch"""
        try:
            # Check if this is the current branch
            current_branch = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                capture_output=True,
                text=True,
                check=True
            ).stdout.strip()

            if old_name == current_branch or old_name.endswith('/' + current_branch):
                # Rename current branch
                cmd = ["git", "branch", "-m", new_name]
            else:
                # Rename another branch
                cmd = ["git", "branch", "-m", old_name, new_name]

            if force:
                cmd[2] = "-M"

            subprocess.run(cmd, check=True)
            print(f"✓ Renamed: {old_name} → {new_name}")
            return True

        except subprocess.CalledProcessError as e:
            print(f"✗ Error renaming {old_name}: {e}")
            return False

    def check_all_branches(self, fix: bool = False, include_remote: bool = False) -> None:
        """Check all branches and optionally fix them"""
        branches = self.get_all_branches(include_remote)

        if not branches:
            print("No branches found.")
            return

        print(f"\n{'='*60}")
        print(f"Checking branches using {self.convention.value} convention")
        print(f"{'='*60}\n")

        invalid_count = 0
        fixed_count = 0

        for branch in branches:
            # Skip remote branches if not included
            if branch.startswith('remotes/') and not include_remote:
                continue

            # Skip remote branches for fixing
            if branch.startswith('remotes/'):
                display_name = branch
            else:
                display_name = branch

            is_valid, error = self.validate_branch_name(branch.replace('remotes/origin/', ''))

            if is_valid:
                print(f"✓ {display_name}")
            else:
                invalid_count += 1
                print(f"✗ {display_name}")
                print(f"  Error: {error}")

                if not branch.startswith('remotes/'):
                    suggested = self.suggest_fix(branch)
                    print(f"  Suggested: {suggested}")

                    if fix:
                        confirm = input(f"  Rename to '{suggested}'? (y/n): ")
                        if confirm.lower() == 'y':
                            if self.rename_branch(branch, suggested):
                                fixed_count += 1
                print()

        print(f"{'='*60}")
        print(f"Summary: {len(branches)} branches checked")
        print(f"Invalid: {invalid_count}")
        if fix:
            print(f"Fixed: {fixed_count}")
        print(f"{'='*60}\n")


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Git Branch Name Fixer - أداة لإصلاح أسماء فروع Git',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Check all branches
  python git_branch_fixer.py check

  # Check and fix branches interactively
  python git_branch_fixer.py check --fix

  # Use kebab-case convention
  python git_branch_fixer.py check --convention kebab_case

  # Check a specific branch name
  python git_branch_fixer.py validate "my-branch-name"

  # Suggest a fix for a branch name
  python git_branch_fixer.py suggest "My Feature Branch"
        """
    )

    parser.add_argument(
        'command',
        choices=['check', 'validate', 'suggest', 'rename'],
        help='Command to execute'
    )

    parser.add_argument(
        'branch_name',
        nargs='?',
        help='Branch name (for validate, suggest, rename commands)'
    )

    parser.add_argument(
        '--new-name',
        help='New branch name (for rename command)'
    )

    parser.add_argument(
        '--convention',
        choices=['gitflow', 'feature_slash', 'kebab_case', 'snake_case'],
        default='gitflow',
        help='Naming convention to use (default: gitflow)'
    )

    parser.add_argument(
        '--fix',
        action='store_true',
        help='Automatically fix invalid branch names (interactive)'
    )

    parser.add_argument(
        '--include-remote',
        action='store_true',
        help='Include remote branches in check'
    )

    parser.add_argument(
        '--force',
        action='store_true',
        help='Force rename even if target exists'
    )

    args = parser.parse_args()

    # Create fixer instance
    convention = NamingConvention(args.convention)
    fixer = GitBranchFixer(convention)

    # Execute command
    if args.command == 'check':
        fixer.check_all_branches(fix=args.fix, include_remote=args.include_remote)

    elif args.command == 'validate':
        if not args.branch_name:
            print("Error: branch_name is required for validate command")
            sys.exit(1)

        is_valid, error = fixer.validate_branch_name(args.branch_name)
        if is_valid:
            print(f"✓ '{args.branch_name}' is valid")
        else:
            print(f"✗ '{args.branch_name}' is invalid")
            print(f"Error: {error}")
            sys.exit(1)

    elif args.command == 'suggest':
        if not args.branch_name:
            print("Error: branch_name is required for suggest command")
            sys.exit(1)

        suggested = fixer.suggest_fix(args.branch_name)
        print(f"Original:  {args.branch_name}")
        print(f"Suggested: {suggested}")

    elif args.command == 'rename':
        if not args.branch_name or not args.new_name:
            print("Error: both branch_name and --new-name are required for rename command")
            sys.exit(1)

        fixer.rename_branch(args.branch_name, args.new_name, force=args.force)


if __name__ == '__main__':
    main()
