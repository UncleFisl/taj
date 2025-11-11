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

