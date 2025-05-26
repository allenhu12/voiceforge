# VoiceForge Git Workflow Guide

**Version:** 1.0.0  
**Last Updated:** January 26, 2025  
**Target Audience:** Developers and Contributors

---

## 📚 Table of Contents

1. [Git Repository Setup](#git-repository-setup)
2. [Branch Strategy](#branch-strategy)
3. [Commit Guidelines](#commit-guidelines)
4. [Development Workflow](#development-workflow)
5. [Release Management](#release-management)
6. [Collaboration Guidelines](#collaboration-guidelines)

---

## 🚀 Git Repository Setup

### Repository Structure
```
VoiceForge/
├── .git/                    # Git repository data
├── .gitignore              # Files to ignore in version control
├── src/voiceforge/         # Main application source code
├── docs/                   # Documentation
├── tests/                  # Test suite
├── README.md               # Project overview
├── requirements.txt        # Python dependencies
├── setup.py               # Package configuration
└── demo.py                # Demo script
```

### Initial Setup Complete ✅
- [x] Git repository initialized
- [x] Comprehensive `.gitignore` configured
- [x] Initial commit with Phase 1 codebase
- [x] 26 files committed (~4,900 lines of code)

---

## 🌿 Branch Strategy

### Main Branches

#### `master` (or `main`)
- **Purpose**: Production-ready code
- **Protection**: Protected branch, requires PR reviews
- **Deployment**: Automatically deployed to production
- **Commits**: Only merge commits from `develop` or hotfix branches

#### `develop`
- **Purpose**: Integration branch for features
- **Source**: Feature branches merge here
- **Target**: Merges to `master` for releases
- **Testing**: Continuous integration runs on all commits

### Supporting Branches

#### Feature Branches
```bash
# Naming convention: feature/description-of-feature
feature/batch-processing
feature/openai-tts-integration
feature/gui-implementation
feature/voice-preview
```

#### Release Branches
```bash
# Naming convention: release/version-number
release/1.1.0
release/1.2.0
release/2.0.0
```

#### Hotfix Branches
```bash
# Naming convention: hotfix/issue-description
hotfix/api-key-encryption-bug
hotfix/cli-crash-fix
hotfix/security-vulnerability
```

---

## 📝 Commit Guidelines

### Commit Message Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, etc.)
- **refactor**: Code refactoring
- **test**: Adding or updating tests
- **chore**: Maintenance tasks

### Examples
```bash
# Feature commit
feat(cli): add batch processing support for multiple files

# Bug fix commit
fix(config): resolve API key encryption issue on Windows

# Documentation commit
docs(readme): update installation instructions for Phase 2

# Refactoring commit
refactor(services): extract common TTS client functionality
```

### Commit Best Practices
- **Keep commits atomic**: One logical change per commit
- **Write clear messages**: Explain what and why, not how
- **Use present tense**: "Add feature" not "Added feature"
- **Reference issues**: Include issue numbers when applicable
- **Limit subject line**: 50 characters or less
- **Separate subject and body**: Use blank line between them

---

## 🔄 Development Workflow

### 1. Starting New Work

```bash
# Update your local repository
git checkout develop
git pull origin develop

# Create a new feature branch
git checkout -b feature/your-feature-name

# Start development...
```

### 2. During Development

```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "feat(core): implement voice preview functionality"

# Push to remote branch
git push origin feature/your-feature-name
```

### 3. Code Review Process

```bash
# Create Pull Request (GitHub/GitLab)
# - Target: develop branch
# - Include: Description, testing notes, screenshots
# - Request: Code review from team members

# Address review feedback
git add .
git commit -m "fix(review): address code review comments"
git push origin feature/your-feature-name
```

### 4. Merging

```bash
# After approval, merge via PR interface
# Or locally:
git checkout develop
git merge --no-ff feature/your-feature-name
git push origin develop

# Clean up
git branch -d feature/your-feature-name
git push origin --delete feature/your-feature-name
```

---

## 🚀 Release Management

### Phase-Based Releases

#### Phase 1: Foundation ✅ (v1.0.0)
- **Status**: Completed and committed
- **Features**: Core CLI, Fish Audio integration, configuration
- **Commit**: `d366771`

#### Phase 2: Enhancements (v1.1.0)
```bash
# Create release branch
git checkout develop
git checkout -b release/1.1.0

# Update version numbers
# Update CHANGELOG.md
# Final testing

# Merge to master
git checkout master
git merge --no-ff release/1.1.0
git tag -a v1.1.0 -m "Release v1.1.0: CLI enhancements and additional providers"
git push origin master --tags

# Merge back to develop
git checkout develop
git merge --no-ff release/1.1.0
git push origin develop
```

### Version Numbering
- **Major**: Breaking changes (2.0.0)
- **Minor**: New features, backward compatible (1.1.0)
- **Patch**: Bug fixes, backward compatible (1.0.1)

### Release Checklist
- [ ] All tests passing
- [ ] Documentation updated
- [ ] Version numbers updated
- [ ] CHANGELOG.md updated
- [ ] Release notes prepared
- [ ] Security review completed

---

## 👥 Collaboration Guidelines

### Before Starting Work
1. **Check existing issues**: Avoid duplicate work
2. **Create/assign issue**: Document what you're working on
3. **Discuss approach**: Get feedback on implementation plan
4. **Update project board**: Move issue to "In Progress"

### Code Quality Standards
```bash
# Format code before committing
black src/
isort src/

# Type checking
mypy src/

# Linting
flake8 src/

# Run tests
pytest tests/
```

### Pull Request Guidelines
- **Clear title**: Summarize the change
- **Detailed description**: Explain what, why, and how
- **Link issues**: Reference related issues
- **Include tests**: Add/update tests for new features
- **Update docs**: Keep documentation current
- **Small PRs**: Easier to review and merge

### Code Review Checklist
- [ ] Code follows project style guidelines
- [ ] Tests are included and passing
- [ ] Documentation is updated
- [ ] No security vulnerabilities
- [ ] Performance impact considered
- [ ] Error handling is appropriate

---

## 🛠️ Useful Git Commands

### Daily Workflow
```bash
# Check status
git status

# View changes
git diff
git diff --staged

# Interactive staging
git add -p

# Amend last commit
git commit --amend

# View history
git log --oneline --graph
git log --author="Your Name"
```

### Branch Management
```bash
# List branches
git branch -a

# Switch branches
git checkout branch-name
git switch branch-name  # Git 2.23+

# Create and switch
git checkout -b new-branch
git switch -c new-branch  # Git 2.23+

# Delete branch
git branch -d branch-name
git push origin --delete branch-name
```

### Undoing Changes
```bash
# Unstage files
git reset HEAD file-name

# Discard working directory changes
git checkout -- file-name
git restore file-name  # Git 2.23+

# Reset to previous commit
git reset --hard HEAD~1

# Revert a commit
git revert commit-hash
```

### Remote Management
```bash
# Add remote
git remote add origin https://github.com/username/voiceforge.git

# View remotes
git remote -v

# Fetch updates
git fetch origin

# Pull with rebase
git pull --rebase origin develop
```

---

## 📊 Git Statistics

### Current Repository Stats
- **Initial Commit**: `d366771`
- **Files Tracked**: 26 files
- **Lines of Code**: ~4,900 lines
- **Branches**: `master` (main)
- **Tags**: None yet (v1.0.0 planned)

### Ignored Files
- Python cache files (`__pycache__/`, `*.pyc`)
- Virtual environments (`venv/`, `.env`)
- IDE files (`.vscode/`, `.idea/`)
- Output files (`*.mp3`, `voiceforge_output/`)
- Configuration files with secrets (`*.key`, `api_keys.json`)
- Log files (`*.log`, `logs/`)
- Temporary files (`test_*.txt`, `temp_*`)

---

## 🎯 Next Steps

### Immediate (This Week)
1. **Set up remote repository**: GitHub/GitLab
2. **Configure branch protection**: Require PR reviews
3. **Set up CI/CD**: Automated testing and deployment
4. **Create issue templates**: Bug reports and feature requests

### Short Term (Next Month)
1. **Implement Git hooks**: Pre-commit formatting and linting
2. **Set up semantic versioning**: Automated version bumps
3. **Create release automation**: Automated changelog generation
4. **Set up code coverage**: Track test coverage metrics

### Long Term (Next Quarter)
1. **Implement GitOps**: Infrastructure as code
2. **Set up monitoring**: Track repository health
3. **Create contributor guidelines**: Onboarding documentation
4. **Implement security scanning**: Automated vulnerability detection

---

## 📞 Getting Help

### Git Resources
- **Official Documentation**: https://git-scm.com/doc
- **Interactive Tutorial**: https://learngitbranching.js.org/
- **Cheat Sheet**: https://education.github.com/git-cheat-sheet-education.pdf

### Project-Specific Help
- **Issues**: Create GitHub/GitLab issues for bugs and features
- **Discussions**: Use repository discussions for questions
- **Code Review**: Request reviews from team members
- **Documentation**: Check `docs/` directory for guides

---

**🎉 Git repository successfully set up!** VoiceForge is now under version control with a solid foundation for collaborative development. Follow this workflow guide to maintain code quality and project organization as we move into Phase 2 and beyond. 