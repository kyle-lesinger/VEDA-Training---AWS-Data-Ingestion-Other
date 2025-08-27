# Setting Up Disaster Repository - Step-by-Step Guide

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [GitHub Account Setup](#github-account-setup)
3. [Configure Git Identity](#configure-git-identity)
4. [GitHub Authentication Setup](#github-authentication-setup)
5. [Clone the Repository](#clone-the-repository)
6. [Working with Branches](#working-with-branches)
7. [Making Changes and Pushing](#making-changes-and-pushing)
8. [Troubleshooting Common Issues](#troubleshooting-common-issues)

---

## Prerequisites

Before starting, ensure you have:
- Git installed in your JupyterHub environment
- Access to terminal in JupyterHub
- Internet connection
- GitHub account (we'll create one if needed)

Check if Git is installed:
```bash
git --version
```

If not installed, contact your JupyterHub administrator.

---

## GitHub Account Setup

### Step 1: Create GitHub Account (if you don't have one)

1. Visit [https://github.com](https://github.com)
2. Click **Sign up**
3. Enter your details:
   - **Username**: Choose carefully (this is permanent and public)
   - **Email**: Use your professional/institutional email
   - **Password**: Create a strong password
4. Verify your email address
5. Complete profile setup

### Step 2: Enable Two-Factor Authentication (Recommended)

1. Go to **Settings** → **Password and authentication**
2. Click **Enable two-factor authentication**
3. Use an authenticator app (Google Authenticator, Authy, or Microsoft Authenticator)
4. Save backup codes securely

---

## Configure Git Identity

Configure Git with your GitHub account information:

```bash
# Set your name (visible in commits)
git config --global user.name "Your Full Name"

# Set your email (MUST match your GitHub account email)
git config --global user.email "your.email@example.com"

# Set default branch name to main
git config --global init.defaultBranch main

# Enable colored output for better readability
git config --global color.ui auto

# Verify your configuration
git config --list
```

**Example:**
```bash
git config --global user.name "Kyle Lesinger"
git config --global user.email "kyle.lesinger@example.com"
```

---

## GitHub Authentication Setup

Since GitHub no longer supports password authentication, you need to use either:
1. **Personal Access Token** (Easier for JupyterHub)
2. **SSH Keys** (More secure, one-time setup)
3. **GitHub CLI** (Recommended - handles auth automatically)

### Option 1: GitHub CLI Authentication (Recommended)

```bash
# Authenticate with GitHub CLI
gh auth login

# Follow the prompts:
# 1. Choose: GitHub.com
# 2. Choose: HTTPS (recommended for JupyterHub)
# 3. Choose: Login with a web browser
# 4. Copy the one-time code shown
# 5. Press Enter to open browser (or manually visit https://github.com/login/device)
# 6. Enter the code and authorize

# Verify authentication
gh auth status
```

### Option 2: Personal Access Token

1. Go to GitHub.com → **Settings** → **Developer settings**
2. Click **Personal access tokens** → **Tokens (classic)**
3. Click **Generate new token** → **Generate new token (classic)**
4. Name it: "JupyterHub Access"
5. Set expiration (90 days recommended)
6. Select scopes:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `workflow` (Update GitHub Action workflows)
7. Click **Generate token**
8. **COPY THE TOKEN IMMEDIATELY** (you won't see it again!)

Store the token securely for use when pushing:
```bash
# Store credentials (will be saved after first use)
git config --global credential.helper store
```

### Option 3: SSH Key Setup

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your.email@example.com"
# Press Enter for default location
# Optionally set a passphrase

# Display your public key
cat ~/.ssh/id_ed25519.pub

# Copy the entire output, then:
# 1. Go to GitHub.com → Settings → SSH and GPG keys
# 2. Click "New SSH key"
# 3. Paste your key and save

# Test SSH connection
ssh -T git@github.com
```

---

## Clone the Repository

### Step 1: Clone the Repository

```bash
# Navigate to your workspace
cd ~/

# Clone the repository (creates a new folder called 'conversion_scripts')
git clone https://github.com/kyle-lesinger/conversion_scripts.git

# Navigate into the repository
cd conversion_scripts

# Verify the clone
ls -la
git status
```

### Step 2: Verify Remote Configuration

```bash
# Check current remotes
git remote -v

# You should see:
# origin  https://github.com/kyle-lesinger/conversion_scripts.git (fetch)
# origin  https://github.com/kyle-lesinger/conversion_scripts.git (push)
```

### Step 3: (Optional) Switch to SSH Remote

If you set up SSH keys and prefer using SSH:

```bash
# Remove HTTPS remote
git remote remove origin

# Add SSH remote
git remote add origin git@github.com:kyle-lesinger/conversion_scripts.git

# Verify the change
git remote -v
```

---

## Working with Branches

### Create a New Branch

Always create a new branch for your work instead of committing directly to main:

```bash
# Make sure you're on the main branch
git checkout main

# Pull latest changes
git pull origin main

# Create and switch to a new branch
git checkout -b feature/your-feature-name

# Example branch names:
# git checkout -b feature/add-preprocessing
# git checkout -b bugfix/fix-data-pipeline
# git checkout -b docs/update-readme
```

### Verify Your Branch

```bash
# Check which branch you're on
git branch

# List all branches (local and remote)
git branch -a
```

---

## Making Changes and Pushing

### Step 1: Make Your Changes

```bash
# Create or edit files
echo "# Conversion Scripts" > README.md
echo "This repository contains data conversion scripts." >> README.md

# Check what files have changed
git status
```

### Step 2: Stage and Commit Changes

```bash
# Add specific files
git add README.md

# Or add all changes
git add .

# Commit with descriptive message
git commit -m "Add README with project description"

# View commit history
git log --oneline
```

### Step 3: Push to GitHub

#### First Time Push (new branch):
```bash
# Push and set upstream branch
git push -u origin feature/your-feature-name

# If using Personal Access Token, enter:
# Username: your-github-username
# Password: your-personal-access-token (NOT your GitHub password!)
```

#### Subsequent Pushes:
```bash
# After upstream is set, simply:
git push
```

### Step 4: Create Pull Request

```bash
# Using GitHub CLI (if authenticated)
gh pr create --title "Add README documentation" --body "Added project description"

# Or manually:
# 1. Visit https://github.com/kyle-lesinger/conversion_scripts
# 2. Click "Compare & pull request" button
# 3. Add title and description
# 4. Click "Create pull request"
```

---

## Complete Workflow Example

Here's a complete example workflow from start to finish:

```bash
# 1. Configure Git (one-time setup)
git config --global user.name "Kyle Lesinger"
git config --global user.email "kyle.lesinger@example.com"

# 2. Authenticate with GitHub CLI
gh auth login
# Follow the interactive prompts

# 3. Clone the repository
cd ~/
git clone https://github.com/kyle-lesinger/conversion_scripts.git
cd conversion_scripts

# 4. Create a new branch
git checkout -b feature/add-conversion-script

# 5. Create a new file
cat > convert_data.py << 'EOF'
#!/usr/bin/env python3
"""
Data conversion utility script
"""

def convert_format(input_file, output_file):
    """Convert data from one format to another"""
    print(f"Converting {input_file} to {output_file}")
    # Add conversion logic here

if __name__ == "__main__":
    convert_format("input.txt", "output.json")
EOF

# 6. Stage and commit
git add convert_data.py
git commit -m "Add data conversion utility script"

# 7. Push to GitHub
git push -u origin feature/add-conversion-script

# 8. Create pull request
gh pr create --title "Add data conversion script" --body "Initial conversion utility"
```

---

## Troubleshooting Common Issues

### Issue 1: Authentication Failed

**Error:** `remote: Invalid username or password`

**Solution:**
```bash
# Use Personal Access Token instead of password
# When prompted for password, paste your token

# Or use GitHub CLI
gh auth login
```

### Issue 2: Permission Denied (publickey)

**Error:** `git@github.com: Permission denied (publickey)`

**Solution:**
```bash
# Check if SSH key exists
ls -la ~/.ssh/

# Generate new key if needed
ssh-keygen -t ed25519 -C "your.email@example.com"

# Add to SSH agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Add public key to GitHub account
cat ~/.ssh/id_ed25519.pub
# Copy output and add to GitHub.com → Settings → SSH Keys
```

### Issue 3: Remote Already Exists

**Error:** `error: remote origin already exists`

**Solution:**
```bash
# Remove existing remote
git remote remove origin

# Add new remote
git remote add origin https://github.com/kyle-lesinger/conversion_scripts.git
```

### Issue 4: Rejected Push (Non-fast-forward)

**Error:** `! [rejected] main -> main (non-fast-forward)`

**Solution:**
```bash
# Pull latest changes first
git pull origin main --rebase

# Then push
git push origin main
```

### Issue 5: Wrong Branch

**Error:** Working on main branch instead of feature branch

**Solution:**
```bash
# Create new branch with current changes
git checkout -b feature/my-changes

# Push to new branch
git push -u origin feature/my-changes
```

---

## Best Practices

1. **Always work in branches** - Never commit directly to main
2. **Pull before pushing** - Always sync with remote before pushing
3. **Use descriptive commit messages** - Explain what and why
4. **Commit frequently** - Small, logical commits are better
5. **Keep tokens secure** - Never commit tokens or passwords
6. **Test locally** - Run your code before committing

---

## Quick Command Reference

```bash
# Clone repository
git clone https://github.com/kyle-lesinger/conversion_scripts.git

# Create branch
git checkout -b feature/new-feature

# Check status
git status

# Add files
git add .

# Commit
git commit -m "Description of changes"

# Push new branch
git push -u origin feature/new-feature

# Push existing branch
git push

# Pull latest changes
git pull origin main

# Switch branches
git checkout branch-name

# List branches
git branch -a

# Delete local branch
git branch -d branch-name

# View commit history
git log --oneline --graph
```

---

## Additional Resources

- [GitHub Docs](https://docs.github.com)
- [Git Documentation](https://git-scm.com/doc)
- [GitHub CLI Manual](https://cli.github.com/manual)
- [Pro Git Book (Free)](https://git-scm.com/book)

---

## Getting Help

If you encounter issues not covered here:

1. Check the repository issues: https://github.com/kyle-lesinger/conversion_scripts/issues
2. Ask in the JupyterHub support channel
3. Consult the comprehensive [Git/GitHub guide](../Github/git-github-comprehensive-guide.md)

---

*Last Updated: 2024*
*Version: 1.0*