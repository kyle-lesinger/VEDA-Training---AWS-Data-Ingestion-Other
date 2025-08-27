# Git and GitHub Comprehensive Training Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Prerequisites & System Setup](#prerequisites--system-setup)
3. [Git Installation](#git-installation)
4. [GitHub Account Setup](#github-account-setup)
5. [GitHub CLI Installation & Authentication](#github-cli-installation--authentication)
6. [Setting Up Your First Repository](#setting-up-your-first-repository)
7. [Essential Git Commands](#essential-git-commands)
8. [GitHub CLI Essentials](#github-cli-essentials)
9. [Common Workflows](#common-workflows)
10. [Best Practices](#best-practices)
11. [Troubleshooting](#troubleshooting)
12. [Quick Reference](#quick-reference)
13. [Resources & Links](#resources--links)

---

## Introduction

Git is a distributed version control system that tracks changes in your code over time. GitHub is a cloud-based hosting service that lets you manage Git repositories with additional collaboration features. This guide will walk you through everything you need to know to get started with Git and GitHub on macOS.

### Why Use Git and GitHub?

- **Version Control**: Track every change made to your code
- **Collaboration**: Work with others without conflicts
- **Backup**: Your code is safely stored in the cloud
- **Documentation**: Built-in wiki and issue tracking
- **Portfolio**: Showcase your work to potential employers

---

## Prerequisites & System Setup

### System Requirements
- macOS 10.15 (Catalina) or later
- Administrator access to install software
- Internet connection
- Terminal application (built into macOS)

### Recommended Tools
- **Text Editor**: VS Code, Sublime Text, or vim
- **Terminal**: iTerm2 or built-in Terminal app
- **Git GUI** (optional): SourceTree, GitHub Desktop, or GitKraken

---

## Git Installation

### Method 1: Install via Homebrew (Recommended)

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Git
brew install git

# Verify installation
git --version
```

### Method 2: Install via Xcode Command Line Tools

```bash
# This will prompt to install Xcode Command Line Tools
git --version

# Follow the prompts to complete installation
```

### Method 3: Download from Git Website

1. Visit [https://git-scm.com/download/mac](https://git-scm.com/download/mac)
2. Download the installer
3. Run the installer package
4. Verify: `git --version`

### Initial Git Configuration

```bash
# Set your name (visible in commits)
git config --global user.name "Your Name"

# Set your email (should match GitHub account)
git config --global user.email "your.email@example.com"

# Set default branch name to 'main'
git config --global init.defaultBranch main

# Set default editor (optional)
git config --global core.editor "code --wait"  # For VS Code
# git config --global core.editor "vim"        # For vim
# git config --global core.editor "nano"       # For nano

# Enable color output
git config --global color.ui auto

# View all settings
git config --list
```

---

## GitHub Account Setup

### Step 1: Create a GitHub Account

1. Visit [https://github.com](https://github.com)
2. Click "Sign up" in the top right
3. Enter your details:
   - **Username**: Choose wisely - this is permanent and public
   - **Email**: Use a professional email address
   - **Password**: Use a strong, unique password
4. Verify your email address
5. Complete the profile setup

### Step 2: Configure Account Security

1. **Enable Two-Factor Authentication (2FA)**:
   - Go to Settings → Security
   - Click "Enable two-factor authentication"
   - Use an authenticator app (Google Authenticator, Authy)
   - Save backup codes securely

2. **Add SSH Key** (recommended for secure authentication):

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your.email@example.com"

# Press Enter for default location
# Set a passphrase (recommended)

# Start SSH agent
eval "$(ssh-agent -s)"

# Add SSH key to agent
ssh-add ~/.ssh/id_ed25519

# Copy public key to clipboard
pbcopy < ~/.ssh/id_ed25519.pub
```

3. **Add SSH Key to GitHub**:
   - Go to Settings → SSH and GPG keys
   - Click "New SSH key"
   - Paste your key and give it a descriptive title
   - Click "Add SSH key"

4. **Test SSH connection**:
```bash
ssh -T git@github.com
# You should see: "Hi username! You've successfully authenticated..."
```

### Step 3: Set Up Personal Access Token (Alternative to SSH)

1. Go to Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token"
3. Set expiration and select scopes (at minimum: repo, workflow)
4. Copy the token immediately (you won't see it again)
5. Use this token as your password when prompted by Git

---

## GitHub CLI Installation & Authentication

### Installing GitHub CLI (gh)

```bash
# Install via Homebrew
brew install gh

# Verify installation
gh --version
```

### Authenticating with GitHub CLI

```bash
# Start authentication process
gh auth login

# Follow the prompts:
# 1. Choose GitHub.com
# 2. Choose HTTPS or SSH (SSH recommended if you've set it up)
# 3. Authenticate via web browser or paste authentication token
# 4. Choose default git protocol (ssh recommended)

# Verify authentication
gh auth status
```

### Configure GitHub CLI

```bash
# Set default editor
gh config set editor "code --wait"  # For VS Code

# Set default browser
gh config set browser safari

# View current configuration
gh config list
```

---

## Setting Up Your First Repository

### Method 1: Clone an Existing Repository

```bash
# Using HTTPS
git clone https://github.com/username/repository.git

# Using SSH (recommended if configured)
git clone git@github.com:username/repository.git

# Using GitHub CLI
gh repo clone username/repository

# Clone into specific directory
git clone git@github.com:username/repository.git my-project
```

### Method 2: Create a New Repository

#### Via GitHub Website:
1. Click the "+" icon → "New repository"
2. Enter repository name
3. Add description (optional)
4. Choose public or private
5. Initialize with README (recommended)
6. Add .gitignore (select template)
7. Choose a license
8. Click "Create repository"

#### Via GitHub CLI:

```bash
# Create a new repository on GitHub
gh repo create my-project --public --clone

# With more options
gh repo create my-project \
  --public \
  --description "My awesome project" \
  --clone \
  --add-readme \
  --license mit \
  --gitignore Python
```

### Method 3: Push Existing Local Project

```bash
# Navigate to your project
cd my-existing-project

# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit"

# Create repository on GitHub
gh repo create my-project --source=. --public --push

# Or manually add remote and push
git remote add origin git@github.com:username/my-project.git
git branch -M main
git push -u origin main
```

---

## Essential Git Commands

### Basic Commands

```bash
# Check Git version
git --version

# Get help
git help <command>
git <command> --help

# Initialize repository
git init

# Clone repository
git clone <url>

# Check status
git status

# View commit history
git log
git log --oneline
git log --graph --oneline --all
```

### Working with Changes

```bash
# Add files to staging area
git add <file>
git add .                    # Add all files
git add *.js                 # Add all JavaScript files
git add -p                   # Interactive staging

# Remove files from staging
git reset HEAD <file>
git restore --staged <file>  # Git 2.23+

# Commit changes
git commit -m "Commit message"
git commit -am "Message"     # Add and commit (tracked files only)
git commit --amend           # Amend last commit

# View differences
git diff                     # Unstaged changes
git diff --staged           # Staged changes
git diff HEAD~1             # Changes since last commit
```

### Branching and Merging

```bash
# List branches
git branch                   # Local branches
git branch -r               # Remote branches
git branch -a               # All branches

# Create branch
git branch <branch-name>
git checkout -b <branch-name>  # Create and switch
git switch -c <branch-name>    # Git 2.23+ (create and switch)

# Switch branches
git checkout <branch-name>
git switch <branch-name>       # Git 2.23+

# Merge branch
git merge <branch-name>

# Delete branch
git branch -d <branch-name>    # Safe delete
git branch -D <branch-name>    # Force delete

# Rename branch
git branch -m <old-name> <new-name>
```

### Working with Remotes

```bash
# View remotes
git remote -v

# Add remote
git remote add <name> <url>
git remote add origin git@github.com:username/repo.git

# Remove remote
git remote remove <name>

# Rename remote
git remote rename <old> <new>

# Fetch changes
git fetch
git fetch origin

# Pull changes
git pull
git pull origin main

# Push changes
git push
git push origin main
git push -u origin main      # Set upstream
git push --force             # Force push (use with caution!)
```

### Stashing Changes

```bash
# Save changes temporarily
git stash
git stash save "Work in progress"

# List stashes
git stash list

# Apply stash
git stash apply              # Apply most recent
git stash apply stash@{0}   # Apply specific stash

# Apply and remove stash
git stash pop

# Remove stash
git stash drop stash@{0}

# Clear all stashes
git stash clear
```

### Undoing Changes

```bash
# Discard changes in working directory
git checkout -- <file>
git restore <file>           # Git 2.23+

# Unstage files
git reset HEAD <file>
git restore --staged <file>  # Git 2.23+

# Reset to previous commit (keeping changes)
git reset --soft HEAD~1

# Reset to previous commit (discard changes)
git reset --hard HEAD~1

# Revert a commit (creates new commit)
git revert <commit-hash>
```

### Tagging

```bash
# List tags
git tag

# Create tag
git tag v1.0.0
git tag -a v1.0.0 -m "Version 1.0.0"  # Annotated tag

# Push tags
git push origin v1.0.0
git push origin --tags       # Push all tags

# Delete tag
git tag -d v1.0.0           # Local
git push origin :v1.0.0     # Remote
```

---

## GitHub CLI Essentials

### Repository Management

```bash
# Set default repository
gh repo set-default
# Select from list or specify:
gh repo set-default owner/repo

# View repository
gh repo view
gh repo view owner/repo

# Fork repository
gh repo fork owner/repo

# Create repository
gh repo create my-repo --public --clone

# Delete repository (use with caution!)
gh repo delete owner/repo

# Clone repository
gh repo clone owner/repo

# List repositories
gh repo list
gh repo list owner
```

### Pull Request Commands

```bash
# Create pull request
gh pr create
gh pr create --title "Feature X" --body "Description"
gh pr create --fill  # Use commit messages for title/body
gh pr create --draft # Create as draft
gh pr create --assignee @me --label bug,enhancement

# List pull requests
gh pr list
gh pr list --state all
gh pr list --author @me

# View pull request
gh pr view
gh pr view 123

# Checkout pull request
gh pr checkout 123

# Merge pull request
gh pr merge 123
gh pr merge 123 --merge    # Create merge commit
gh pr merge 123 --rebase   # Rebase and merge
gh pr merge 123 --squash   # Squash and merge

# Close pull request
gh pr close 123

# Review pull request
gh pr review 123 --approve
gh pr review 123 --request-changes
gh pr review 123 --comment

# Check pull request status
gh pr status
gh pr checks 123
```

### Issue Management

```bash
# Create issue
gh issue create
gh issue create --title "Bug report" --body "Description"

# List issues
gh issue list
gh issue list --assignee @me
gh issue list --label bug

# View issue
gh issue view 123

# Close issue
gh issue close 123

# Reopen issue
gh issue reopen 123

# Comment on issue
gh issue comment 123 --body "This is fixed"
```

### Workflow Commands

```bash
# List workflows
gh workflow list

# View workflow runs
gh run list
gh run view

# Watch workflow run
gh run watch

# Download artifacts
gh run download

# Trigger workflow
gh workflow run <workflow-name>
```

### Gist Management

```bash
# Create gist
gh gist create file.txt
gh gist create --public file.txt

# List gists
gh gist list

# View gist
gh gist view <id>

# Edit gist
gh gist edit <id>
```

---

## Common Workflows

### Daily Development Workflow

```bash
# 1. Start your day - sync with remote
git pull origin main

# 2. Create feature branch
git checkout -b feature/new-feature

# 3. Make changes and commit
git add .
git commit -m "Add new feature"

# 4. Push to remote
git push -u origin feature/new-feature

# 5. Create pull request
gh pr create --fill

# 6. After PR is merged, clean up
git checkout main
git pull origin main
git branch -d feature/new-feature
```

### Fixing Merge Conflicts

```bash
# 1. Pull latest changes
git pull origin main

# 2. If conflicts occur, Git will notify you
# 3. Open conflicted files and resolve manually
# Look for conflict markers:
# <<<<<<< HEAD
# Your changes
# =======
# Their changes
# >>>>>>> branch-name

# 4. After resolving, add the files
git add <resolved-files>

# 5. Complete the merge
git commit -m "Resolve merge conflicts"

# 6. Push changes
git push origin <branch>
```

### Updating Fork

```bash
# 1. Add upstream remote (one time)
git remote add upstream https://github.com/original-owner/repo.git

# 2. Fetch upstream changes
git fetch upstream

# 3. Checkout main branch
git checkout main

# 4. Merge upstream changes
git merge upstream/main

# 5. Push to your fork
git push origin main

# Using GitHub CLI
gh repo sync owner/repo -b main
```

### Squashing Commits

```bash
# Interactive rebase for last 3 commits
git rebase -i HEAD~3

# In the editor:
# Change 'pick' to 'squash' for commits to combine
# Save and close

# Force push (if already pushed)
git push --force-with-lease origin <branch>
```

### Cherry-picking Commits

```bash
# Apply specific commit to current branch
git cherry-pick <commit-hash>

# Cherry-pick multiple commits
git cherry-pick <hash1> <hash2> <hash3>

# Cherry-pick range
git cherry-pick <oldest-hash>^..<newest-hash>
```

---

## Best Practices

### Commit Messages

**The Seven Rules of Great Commit Messages:**

1. Separate subject from body with blank line
2. Limit subject line to 50 characters
3. Capitalize the subject line
4. Don't end subject line with period
5. Use imperative mood ("Add feature" not "Added feature")
6. Wrap body at 72 characters
7. Explain what and why, not how

**Example:**
```
Add user authentication feature

Implement OAuth 2.0 authentication using GitHub as provider.
This allows users to sign in with their GitHub credentials
instead of creating separate accounts.

Resolves: #123
See also: #456, #789
```

### Branch Naming Conventions

```bash
feature/add-login-page
bugfix/fix-navigation-menu
hotfix/security-patch
release/v2.0.0
docs/update-readme
test/add-unit-tests
refactor/optimize-database
```

### .gitignore Best Practices

Create a `.gitignore` file in your repository root:

```bash
# macOS
.DS_Store
.AppleDouble
.LSOverride

# IDE
.vscode/
.idea/
*.swp
*.swo

# Dependencies
node_modules/
vendor/
.env

# Build outputs
dist/
build/
*.log

# Sensitive data
*.pem
*.key
.env.local
config/secrets.yml
```

### Security Best Practices

1. **Never commit sensitive data**:
   - Passwords, API keys, tokens
   - Private keys or certificates
   - Database credentials
   - .env files with secrets

2. **If you accidentally commit secrets**:
   ```bash
   # Remove from history (requires force push)
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch path/to/file" \
     --prune-empty --tag-name-filter cat -- --all
   
   # Or use BFG Repo-Cleaner (easier)
   brew install bfg
   bfg --delete-files file-with-secrets.txt
   ```

3. **Use GitHub's security features**:
   - Enable Dependabot alerts
   - Enable secret scanning
   - Use protected branches
   - Require PR reviews

### Collaboration Best Practices

1. **Always work in branches** - Never commit directly to main
2. **Keep PRs small** - Easier to review and less likely to have conflicts
3. **Write descriptive PR descriptions** - Include what, why, and how
4. **Review others' code** - Learn and help maintain quality
5. **Update documentation** - Keep README and docs current
6. **Test before pushing** - Run tests locally first
7. **Communicate** - Use issues and PR comments effectively

---

## Troubleshooting

### Common Issues and Solutions

#### 1. Permission Denied (SSH)

```bash
# Check SSH key is added
ssh-add -l

# Add SSH key
ssh-add ~/.ssh/id_ed25519

# Test connection
ssh -T git@github.com
```

#### 2. Failed to Push (Non-fast-forward)

```bash
# Pull first, then push
git pull origin main --rebase
git push origin main

# Or force push (careful!)
git push --force-with-lease
```

#### 3. Accidentally Committed to Wrong Branch

```bash
# Create new branch with current commits
git branch new-branch

# Reset original branch
git reset --hard HEAD~3  # Go back 3 commits

# Switch to new branch
git checkout new-branch
```

#### 4. Need to Undo Last Commit

```bash
# Keep changes, undo commit
git reset --soft HEAD~1

# Discard changes completely
git reset --hard HEAD~1
```

#### 5. Large Files Blocking Push

```bash
# Install Git LFS
brew install git-lfs
git lfs install

# Track large files
git lfs track "*.psd"
git add .gitattributes
git add large-file.psd
git commit -m "Add large file with LFS"
```

#### 6. Merge Conflicts in Pull Request

```bash
# Update your branch
git checkout main
git pull origin main
git checkout your-branch
git rebase main

# Resolve conflicts, then
git add .
git rebase --continue
git push --force-with-lease
```

---

## Quick Reference

### Git Aliases (Add to ~/.gitconfig)

```ini
[alias]
    st = status
    co = checkout
    ci = commit
    br = branch
    df = diff
    lg = log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit
    last = log -1 HEAD
    unstage = reset HEAD --
    amend = commit --amend
    branches = branch -a
    remotes = remote -v
    contributors = shortlog --summary --numbered
```

### Essential Keyboard Shortcuts (VS Code Git Integration)

- `Cmd + Shift + P` → Git commands
- `Ctrl + Shift + G` → Source control panel
- `Cmd + Enter` → Commit staged changes
- `Option + Cmd + Enter` → Commit all changes

### Terminal Aliases (Add to ~/.zshrc)

```bash
# Git shortcuts
alias g='git'
alias gs='git status'
alias ga='git add'
alias gc='git commit -m'
alias gp='git push'
alias gpl='git pull'
alias gco='git checkout'
alias gb='git branch'
alias glog='git log --oneline --graph --all'

# GitHub CLI shortcuts
alias ghr='gh repo'
alias ghpr='gh pr'
alias ghi='gh issue'
```

---

## Resources & Links

### Official Documentation

- **Git Documentation**: [https://git-scm.com/doc](https://git-scm.com/doc)
- **GitHub Docs**: [https://docs.github.com](https://docs.github.com)
- **GitHub CLI Manual**: [https://cli.github.com/manual](https://cli.github.com/manual)
- **GitHub Learning Lab**: [https://lab.github.com](https://lab.github.com)

### Interactive Learning

- **Learn Git Branching**: [https://learngitbranching.js.org](https://learngitbranching.js.org)
- **GitHub Skills**: [https://skills.github.com](https://skills.github.com)
- **Atlassian Git Tutorial**: [https://www.atlassian.com/git/tutorials](https://www.atlassian.com/git/tutorials)
- **Oh My Git! (Game)**: [https://ohmygit.org](https://ohmygit.org)

### Cheat Sheets

- **GitHub Git Cheat Sheet**: [https://education.github.com/git-cheat-sheet-education.pdf](https://education.github.com/git-cheat-sheet-education.pdf)
- **Interactive Git Cheat Sheet**: [https://ndpsoftware.com/git-cheatsheet.html](https://ndpsoftware.com/git-cheatsheet.html)
- **GitHub CLI Cheat Sheet**: [https://github.com/cli/cli#commands](https://github.com/cli/cli#commands)

### Advanced Topics

- **Pro Git Book (Free)**: [https://git-scm.com/book](https://git-scm.com/book)
- **Git Flow**: [https://nvie.com/posts/a-successful-git-branching-model](https://nvie.com/posts/a-successful-git-branching-model)
- **Conventional Commits**: [https://www.conventionalcommits.org](https://www.conventionalcommits.org)
- **Semantic Versioning**: [https://semver.org](https://semver.org)

### GUI Tools

- **GitHub Desktop**: [https://desktop.github.com](https://desktop.github.com)
- **SourceTree**: [https://www.sourcetreeapp.com](https://www.sourcetreeapp.com)
- **GitKraken**: [https://www.gitkraken.com](https://www.gitkraken.com)
- **Tower**: [https://www.git-tower.com](https://www.git-tower.com)

### VS Code Extensions

- **GitLens**: Enhanced Git capabilities
- **Git Graph**: Visualize branch structure
- **GitHub Pull Requests**: Manage PRs from VS Code
- **Git History**: View and search git log

### Troubleshooting Resources

- **GitHub Status**: [https://www.githubstatus.com](https://www.githubstatus.com)
- **Stack Overflow Git Tag**: [https://stackoverflow.com/questions/tagged/git](https://stackoverflow.com/questions/tagged/git)
- **GitHub Community Forum**: [https://github.community](https://github.community)

### YouTube Channels

- **GitHub YouTube**: [https://youtube.com/github](https://youtube.com/github)
- **The Net Ninja Git Tutorial**: Comprehensive video series
- **Traversy Media Git Crash Course**: Quick overview

### Markdown Resources

- **GitHub Flavored Markdown**: [https://github.github.com/gfm](https://github.github.com/gfm)
- **Markdown Guide**: [https://www.markdownguide.org](https://www.markdownguide.org)
- **Shields.io (Badges)**: [https://shields.io](https://shields.io)

---

## Appendix: Quick Setup Script

Save this as `setup-git-github.sh` and run to quickly set up your environment:

```bash
#!/bin/bash

echo "🚀 Git and GitHub Setup Script for macOS"
echo "======================================="

# Install Homebrew if not present
if ! command -v brew &> /dev/null; then
    echo "📦 Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Install Git
echo "📦 Installing Git..."
brew install git

# Install GitHub CLI
echo "📦 Installing GitHub CLI..."
brew install gh

# Git configuration
echo "⚙️ Configuring Git..."
read -p "Enter your name: " name
read -p "Enter your email: " email

git config --global user.name "$name"
git config --global user.email "$email"
git config --global init.defaultBranch main
git config --global color.ui auto

# Generate SSH key
echo "🔑 Generating SSH key..."
ssh-keygen -t ed25519 -C "$email" -f ~/.ssh/id_ed25519 -N ""

# Start SSH agent and add key
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Copy SSH key to clipboard
pbcopy < ~/.ssh/id_ed25519.pub
echo "📋 SSH public key copied to clipboard!"

# GitHub CLI authentication
echo "🔐 Authenticating with GitHub..."
gh auth login

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Go to GitHub Settings → SSH Keys"
echo "2. Add a new SSH key (already in clipboard)"
echo "3. Test with: ssh -T git@github.com"
```

Make executable and run:
```bash
chmod +x setup-git-github.sh
./setup-git-github.sh
```

---

*Last Updated: 2024*
*Version: 1.0*

*This guide is a living document. Contribute improvements at: [your-repo-url]*