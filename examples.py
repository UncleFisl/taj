#!/usr/bin/env python3
"""
Examples of using the Git Branch Fixer
أمثلة على استخدام أداة إصلاح فروع Git
"""

from git_branch_fixer import GitBranchFixer, NamingConvention


def example_validate_branches():
    """Example 1: Validate branch names"""
    print("=" * 60)
    print("Example 1: Validating Branch Names")
    print("مثال 1: التحقق من أسماء الفروع")
    print("=" * 60)

    fixer = GitBranchFixer(NamingConvention.GITFLOW)

    test_branches = [
        "feature/add-login",
        "bugfix/fix-navbar",
        "My Feature Branch",
        "bug_fix",
        "hotfix/critical-security-patch",
        "main",
        "develop",
    ]

    for branch in test_branches:
        is_valid, error = fixer.validate_branch_name(branch)
        if is_valid:
            print(f"✓ '{branch}' is valid")
        else:
            print(f"✗ '{branch}' is invalid - {error}")

    print()


def example_suggest_fixes():
    """Example 2: Suggest fixes for invalid branch names"""
    print("=" * 60)
    print("Example 2: Suggesting Fixes")
    print("مثال 2: اقتراح الإصلاحات")
    print("=" * 60)

    fixer = GitBranchFixer(NamingConvention.GITFLOW)

    invalid_branches = [
        "My Feature Branch",
        "Fix User Login Bug",
        "ADD_NEW_FEATURE",
        "bug_fix_navbar",
        "hotfix//critical//fix",
    ]

    for branch in invalid_branches:
        suggested = fixer.suggest_fix(branch)
        print(f"Original:  {branch}")
        print(f"Suggested: {suggested}")
        print()


def example_different_conventions():
    """Example 3: Using different naming conventions"""
    print("=" * 60)
    print("Example 3: Different Naming Conventions")
    print("مثال 3: معايير تسمية مختلفة")
    print("=" * 60)

    test_branch = "my-feature-branch"

    conventions = [
        NamingConvention.GITFLOW,
        NamingConvention.FEATURE_SLASH,
        NamingConvention.KEBAB_CASE,
        NamingConvention.SNAKE_CASE,
    ]

    for convention in conventions:
        fixer = GitBranchFixer(convention)
        is_valid, error = fixer.validate_branch_name(test_branch)

        print(f"\nConvention: {convention.value}")
        if is_valid:
            print(f"  ✓ '{test_branch}' is valid")
        else:
            print(f"  ✗ '{test_branch}' is invalid - {error}")
            suggested = fixer.suggest_fix(test_branch)
            print(f"  Suggested: {suggested}")


def example_kebab_case():
    """Example 4: Kebab case convention"""
    print("\n" + "=" * 60)
    print("Example 4: Kebab Case Convention")
    print("مثال 4: معيار Kebab Case")
    print("=" * 60)

    fixer = GitBranchFixer(NamingConvention.KEBAB_CASE)

    test_branches = [
        "my-feature-branch",
        "fix-login-bug",
        "My_Feature_Branch",
        "addNewFeature",
        "feature/add-login",
    ]

    for branch in test_branches:
        is_valid, error = fixer.validate_branch_name(branch)
        if is_valid:
            print(f"✓ '{branch}'")
        else:
            suggested = fixer.suggest_fix(branch)
            print(f"✗ '{branch}' → '{suggested}'")


def example_snake_case():
    """Example 5: Snake case convention"""
    print("\n" + "=" * 60)
    print("Example 5: Snake Case Convention")
    print("مثال 5: معيار Snake Case")
    print("=" * 60)

    fixer = GitBranchFixer(NamingConvention.SNAKE_CASE)

    test_branches = [
        "my_feature_branch",
        "fix_login_bug",
        "My-Feature-Branch",
        "addNewFeature",
        "feature/add_login",
    ]

    for branch in test_branches:
        is_valid, error = fixer.validate_branch_name(branch)
        if is_valid:
            print(f"✓ '{branch}'")
        else:
            suggested = fixer.suggest_fix(branch)
            print(f"✗ '{branch}' → '{suggested}'")


def example_common_mistakes():
    """Example 6: Common mistakes and their fixes"""
    print("\n" + "=" * 60)
    print("Example 6: Common Mistakes")
    print("مثال 6: الأخطاء الشائعة")
    print("=" * 60)

    fixer = GitBranchFixer(NamingConvention.GITFLOW)

    mistakes = {
        "feature with spaces": "Spaces in branch name",
        "feature//double-slash": "Double slashes",
        "/starts-with-slash": "Starts with slash",
        "ends-with-slash/": "Ends with slash",
        "has~special*chars": "Special characters",
        "UPPERCASE_BRANCH": "Uppercase letters",
    }

    for branch, description in mistakes.items():
        is_valid, error = fixer.validate_branch_name(branch)
        suggested = fixer.suggest_fix(branch)

        print(f"\n{description}:")
        print(f"  Original:  '{branch}'")
        if not is_valid:
            print(f"  Error:     {error}")
        print(f"  Suggested: '{suggested}'")


def main():
    """Run all examples"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║  Git Branch Name Fixer - Examples                       ║")
    print("║  أمثلة على أداة إصلاح أسماء فروع Git                   ║")
    print("╚" + "=" * 58 + "╝")
    print()

    example_validate_branches()
    example_suggest_fixes()
    example_different_conventions()
    example_kebab_case()
    example_snake_case()
    example_common_mistakes()

    print("\n" + "=" * 60)
    print("Examples completed! | اكتملت الأمثلة!")
    print("=" * 60)
    print()


if __name__ == '__main__':
    main()
