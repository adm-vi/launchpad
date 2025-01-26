# Launchpad Git Instructions

## Making Changes to the Repository

Follow these steps when making local changes:

1. Check what files you've changed:
```bash
git status
```

2. Add your changed files to staging:
```bash
git add .
```
Or add specific files:
```bash
git add filename
```

3. Commit your changes with a descriptive message:
```bash
git commit -m "Your message describing the changes"
```

4. Push your changes to GitHub:
```bash
git push origin main
```

## Common Git Commands

- View commit history: `git log`
- View remote repository URL: `git remote -v`
- Pull latest changes from GitHub: `git pull origin main`
- View differences in files: `git diff`

## Tips
- Write clear commit messages that describe what changed
- Always check `git status` before committing to see what files will be included
- Use `git pull` before starting new work to get the latest changes
