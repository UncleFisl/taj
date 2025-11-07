# Git Branch Name Fixer | أداة إصلاح أسماء فروع Git

<div dir="rtl">

## نظرة عامة

أداة Python قوية لفحص وإصلاح أسماء فروع Git تلقائياً. تدعم معايير تسمية متعددة وتساعد في الحفاظ على تنظيم المشروع.

</div>

A powerful Python tool to automatically check and fix Git branch names. Supports multiple naming conventions and helps maintain project organization.

---

## ✨ Features | الميزات

<div dir="rtl">

- ✅ **فحص التحقق**: التحقق من صحة أسماء الفروع وفقاً لمعايير محددة
- 🔧 **الإصلاح التلقائي**: اقتراح وتطبيق أسماء فروع صحيحة
- 📋 **معايير متعددة**: دعم GitFlow، Feature Slash، Kebab Case، Snake Case
- 🌍 **دعم عربي**: واجهة وتوثيق باللغتين العربية والإنجليزية
- 📊 **تقارير مفصلة**: عرض ملخصات شاملة للفروع المفحوصة
- 🔄 **إعادة التسمية الآمنة**: إعادة تسمية الفروع بشكل آمن مع تأكيد المستخدم

</div>

- ✅ **Validation Check**: Verify branch names against specific conventions
- 🔧 **Auto-Fix**: Suggest and apply correct branch names
- 📋 **Multiple Conventions**: Support for GitFlow, Feature Slash, Kebab Case, Snake Case
- 🌍 **Arabic Support**: Interface and documentation in both Arabic and English
- 📊 **Detailed Reports**: Display comprehensive summaries of checked branches
- 🔄 **Safe Renaming**: Safely rename branches with user confirmation

---

## 🚀 Installation | التثبيت

```bash
# Clone the repository | استنساخ المستودع
git clone <repository-url>
cd taj

# Make the script executable | جعل السكريبت قابلاً للتنفيذ
chmod +x git_branch_fixer.py
```

---

## 📖 Usage | الاستخدام

### Basic Commands | الأوامر الأساسية

```bash
# Check all branches | فحص جميع الفروع
python3 git_branch_fixer.py check

# Check and fix branches interactively | فحص وإصلاح الفروع بشكل تفاعلي
python3 git_branch_fixer.py check --fix

# Include remote branches | تضمين الفروع البعيدة
python3 git_branch_fixer.py check --include-remote

# Validate a specific branch name | التحقق من اسم فرع محدد
python3 git_branch_fixer.py validate "feature/my-feature"

# Suggest a fix for a branch name | اقتراح إصلاح لاسم فرع
python3 git_branch_fixer.py suggest "My Feature Branch"

# Rename a branch | إعادة تسمية فرع
python3 git_branch_fixer.py rename "old-name" --new-name "feature/new-name"
```

### Naming Conventions | معايير التسمية

#### 1. GitFlow (Default | الافتراضي)

```bash
python3 git_branch_fixer.py check --convention gitflow
```

<div dir="rtl">

**الأنماط الصحيحة:**
- `main`, `master`, `develop`
- `feature/feature-name`
- `bugfix/bug-description`
- `hotfix/urgent-fix`
- `release/version-number`
- `support/support-task`

</div>

**Valid Patterns:**
- `main`, `master`, `develop`
- `feature/feature-name`
- `bugfix/bug-description`
- `hotfix/urgent-fix`
- `release/version-number`
- `support/support-task`

#### 2. Feature Slash

```bash
python3 git_branch_fixer.py check --convention feature_slash
```

**Valid:** `type/description` (e.g., `feature/add-login`, `fix/navbar-bug`)

#### 3. Kebab Case

```bash
python3 git_branch_fixer.py check --convention kebab_case
```

**Valid:** Lowercase with hyphens (e.g., `my-feature-branch`, `fix-login-bug`)

#### 4. Snake Case

```bash
python3 git_branch_fixer.py check --convention snake_case
```

**Valid:** Lowercase with underscores (e.g., `my_feature_branch`, `fix_login_bug`)

---

## 📝 Examples | أمثلة

### Example 1: Check Current Repository | فحص المستودع الحالي

```bash
$ python3 git_branch_fixer.py check

============================================================
Checking branches using gitflow convention
============================================================

✓ main
✗ My Feature Branch
  Error: Branch name cannot contain spaces
  Suggested: feature/my-feature-branch

✓ feature/add-login
✗ bug_fix_navbar
  Error: Branch must start with one of: feature/, bugfix/, hotfix/, release/, support/, main, master, develop
  Suggested: bugfix/bug-fix-navbar

============================================================
Summary: 4 branches checked
Invalid: 2
============================================================
```

### Example 2: Fix Branches Interactively | إصلاح الفروع بشكل تفاعلي

```bash
$ python3 git_branch_fixer.py check --fix

✗ My Feature Branch
  Error: Branch name cannot contain spaces
  Suggested: feature/my-feature-branch
  Rename to 'feature/my-feature-branch'? (y/n): y
✓ Renamed: My Feature Branch → feature/my-feature-branch
```

### Example 3: Validate a Branch Name | التحقق من اسم فرع

```bash
$ python3 git_branch_fixer.py validate "feature/add-authentication"
✓ 'feature/add-authentication' is valid

$ python3 git_branch_fixer.py validate "My Branch"
✗ 'My Branch' is invalid
Error: Branch name cannot contain spaces
```

### Example 4: Suggest Fix | اقتراح إصلاح

```bash
$ python3 git_branch_fixer.py suggest "Fix User Login Bug"
Original:  Fix User Login Bug
Suggested: bugfix/fix-user-login-bug
```

---

## 🎯 Validation Rules | قواعد التحقق

<div dir="rtl">

### القواعد العامة (تنطبق على جميع المعايير)

- ❌ لا يمكن أن يكون الاسم فارغاً
- ❌ لا يمكن أن يبدأ أو ينتهي بـ `/`
- ❌ لا يمكن احتواء `//` متتالية
- ❌ لا يمكن احتواء مسافات
- ❌ لا يمكن احتواء الأحرف الخاصة: `~ ^ : ? * [ \ ..`

### قواعد GitFlow الإضافية

- يجب أن يبدأ بأحد البادئات الصحيحة: `feature/`, `bugfix/`, `hotfix/`, `release/`, `support/`
- أو يكون أحد الفروع الرئيسية: `main`, `master`, `develop`
- الجزء بعد البادئة يجب أن يكون بأحرف صغيرة مع واصلات

</div>

### Common Rules (Apply to All Conventions)

- ❌ Cannot be empty
- ❌ Cannot start or end with `/`
- ❌ Cannot contain consecutive `//`
- ❌ Cannot contain spaces
- ❌ Cannot contain special characters: `~ ^ : ? * [ \ ..`

### GitFlow Additional Rules

- Must start with valid prefix: `feature/`, `bugfix/`, `hotfix/`, `release/`, `support/`
- Or be a main branch: `main`, `master`, `develop`
- Suffix after prefix must be lowercase with hyphens

---

## 🔧 Advanced Usage | الاستخدام المتقدم

### Batch Renaming | إعادة التسمية الجماعية

```bash
# Create a script to rename multiple branches
for branch in $(git branch | grep -v "main\|develop"); do
    python3 git_branch_fixer.py suggest "$branch" >> renames.txt
done
```

### CI/CD Integration | التكامل مع CI/CD

```yaml
# .github/workflows/check-branches.yml
name: Check Branch Names
on: [push, pull_request]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Check branch naming
        run: |
          python3 git_branch_fixer.py validate "${{ github.ref_name }}"
```

### Pre-commit Hook | خطاف ما قبل الالتزام

```bash
# .git/hooks/pre-commit
#!/bin/bash
BRANCH=$(git rev-parse --abbrev-ref HEAD)
python3 git_branch_fixer.py validate "$BRANCH"
if [ $? -ne 0 ]; then
    echo "❌ Branch name is invalid!"
    exit 1
fi
```

---

## 🤝 Contributing | المساهمة

<div dir="rtl">

المساهمات مرحب بها! يرجى:

1. عمل Fork للمستودع
2. إنشاء فرع للميزة (`git checkout -b feature/amazing-feature`)
3. الالتزام بالتغييرات (`git commit -m 'Add amazing feature'`)
4. دفع للفرع (`git push origin feature/amazing-feature`)
5. فتح Pull Request

</div>

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License | الترخيص

This project is open source and available under the MIT License.

<div dir="rtl">

هذا المشروع مفتوح المصدر ومتاح بموجب ترخيص MIT.

</div>

---

## 🙏 Acknowledgments | شكر وتقدير

<div dir="rtl">

- مستوحى من أفضل ممارسات Git وGitFlow
- بني باستخدام Python 3
- دعم اللغة العربية للمطورين العرب

</div>

- Inspired by Git and GitFlow best practices
- Built with Python 3
- Arabic language support for Arab developers

---

## 📞 Support | الدعم

<div dir="rtl">

إذا واجهت أي مشاكل أو لديك اقتراحات، يرجى فتح issue في المستودع.

</div>

If you encounter any issues or have suggestions, please open an issue in the repository.

---

Made with ❤️ by developers, for developers | صُنع بـ ❤️ من المطورين، للمطورين
