## 1. `git config` - Configure Git Settings

- `git config --global user.name "Your Name"`: Sets your name globally for all Git repositories.
- `git config --global user.email "your.email@example.com"`: Sets your email globally for all Git repositories.
- `git config --list`: Shows all Git configuration settings (global, system, and local).
- `git config user.name`: Shows the currently configured user name.

## 2. `git init` - Initialize a New Repository

- `git init`: Initializes an empty Git repository in the current directory. A `.git` folder is created.
- `git init <directory_name>`: Initializes a new Git repository in the specified directory.

## 3. `git clone` - Download an Existing Repository

- `git clone <repository_url>`: Clones an existing repository from a URL (e.g., GitHub, GitLab) into a new directory with the same name as the repository.
- `git clone <repository_url> <local_directory_name>`: Clones the repository into a specified local directory name.
- `git clone -b <branch_name> <repository_url>`: Clones only a specific branch from the repository.

## 4. `git add` - Stage Changes

- `git add <file_name>`: Adds a specific file to the staging area.
- `git add .`: Adds all changes (new files, modified files, deleted files) in the current directory and its subdirectories to the staging area.
- `git add -A` or `git add --all`: Same as `git add .` but also stages deleted files. (Often `git add .` is sufficient for most cases).
- `git add -p` or `git add --patch`: Interactively stages parts of a modified file, allowing you to select specific "hunks" of changes.

## 5. `git commit` - Record Changes

- `git commit -m "Your descriptive commit message"`: Creates a new commit with the staged changes and the provided message. This is the most common way to commit.
- `git commit`: Opens your default text editor (e.g., Vim, Nano) to write a multi-line commit message.
- `git commit -am "Your descriptive commit message"`: Stages all *modified and deleted- files that are already tracked and then commits them. Caution: This does *not- stage new, untracked files. Use `git add .` first if you have new files.
- `git commit --amend`: Allows you to change the message of the most recent commit, or add/remove files from it. The commit hash will change. Use with caution if the commit has already been pushed.
- `git commit --no-verify`: Skips the pre-commit hooks (if any are configured) when committing.

## 6. `git status` - Check Repository Status

- `git status`: Shows the current state of your working directory and staging area, including untracked files, modified files, and staged changes.
- `git status -s` or `git status --short`: Provides a concise, single-line summary of the status.

## 7. `git log` - View Commit History

- `git log`: Displays the entire commit history for the current branch.
- `git log --oneline`: Shows a concise, single-line summary for each commit (commit hash and message).
- `git log --graph --oneline --decorate`: Shows a graphical representation of the commit history, useful for visualizing merges and branches.
- `git log -p` or `git log --patch`: Shows the difference (diff) introduced by each commit.
- `git log --author="Your Name"`: Filters commits by a specific author.
- `git log --grep="keyword"`: Filters commits by keywords in the commit message.
- `git log -n 5`: Shows the last 5 commits.
- `git log <file_name>`: Shows the commit history for a specific file.

## 8. `git diff` - Show Changes Between Commits/Files

- `git diff`: Shows changes in the working directory that are not yet staged.
- `git diff --staged` or `git diff --cached`: Shows changes that are staged but *not- yet committed.
- `git diff <commit1> <commit2>`: Shows the difference between two specific commits.
- `git diff <branch1> <branch2>`: Shows the difference between the tips of two branches.
- `git diff HEAD~1`: Shows the difference between your current working directory and the previous commit.

## 9. `git branch` - Manage Branches

- `git branch`: Lists all local branches. The current branch is highlighted.
- `git branch -a`: Lists all local and remote branches.
- `git branch <new_branch_name>`: Creates a new branch (but does not switch to it).
- `git branch -d <branch_name>`: Deletes a local branch if it has been fully merged.
- `git branch -D <branch_name>`: Forcibly deletes a local branch, even if it hasn't been merged. Use with caution.
- `git branch -m <old_name> <new_name>`: Renames a branch.

## 10. `git checkout` - Switch Branches or Restore Files

- `git checkout <branch_name>`: Switches to an existing branch.
- `git checkout -b <new_branch_name>`: Creates a new branch and immediately switches to it (shortcut for `git branch <new_branch_name>` followed by `git checkout <new_branch_name>`).
- `git checkout <commit_id>`: Switches to a specific commit, putting you in a "detached HEAD" state. Useful for inspecting past states.
- `git checkout <file_name>`: Discards changes in the working directory for a specific file, reverting it to the last committed version. Caution: This will permanently discard unsaved changes.
- `git checkout -- .`: Discards all uncommitted changes in the current directory (reverts all modified files to their last committed state). Extreme Caution: This permanently discards all unsaved changes.

## 11. `git restore` - Undo Changes (Modern Alternative to `git checkout` for Undoing)

- `git restore <file_name>`: Discards changes in the working directory for a specific file (same as `git checkout <file_name>`).
- `git restore --source=HEAD <file_name>`: Explicitly restores a file from the last commit (HEAD).
- `git restore --staged <file_name>`: Unstages a file, moving it from the staging area back to the working directory. This is the primary use case of `git restore`.
- `git restore --staged .`: Unstages all files from the staging area.

## 12. `git merge` - Combine Branches

- `git merge <branch_to_merge_into_current>`: Merges the specified branch into the current branch.
- `git merge --no-ff <branch_name>`: Performs a merge without a "fast-forward" if possible, creating a merge commit even if a fast-forward merge could be done. This keeps the branch history explicit.
- `git merge --abort`: Aborts a merge in progress if conflicts occur.

## 13. `git rebase` - Reapply Commits on Top of Another Base

- `git rebase <base_branch>`: Reapplies commits from your current branch onto the tip of the specified base branch. This creates a linear history. Caution: Avoid rebasing commits that have already been pushed to a shared remote, as it rewrites history.
- `git rebase -i HEAD~N`: Starts an interactive rebase for the last N commits. Allows you to squash, reorder, edit, or delete commits.
- `git rebase --abort`: Aborts a rebase in progress.
- `git rebase --continue`: Continues a rebase after resolving conflicts.

## 14. `git revert` - Undo Committed Changes (Safely)

- `git revert <commit_id>`: Creates a *new- commit that undoes the changes introduced by the specified commit. This is the safest way to undo changes in a shared history, as it does not rewrite history.
- `git revert HEAD`: Reverts the last commit.
- `git revert <commit_id> -n` or `--no-commit`: Prepares the changes to revert the commit, but doesn't create a new commit immediately, allowing you to make further changes.

## 15. `git reset` - Undo Changes (Potentially Destructive)

- `git reset --soft <commit_id>`: Moves the HEAD to the specified commit, but keeps the changes in the staging area and working directory.
- `git reset --mixed <commit_id>` (default): Moves the HEAD to the specified commit and unstages the changes, but keeps them in the working directory.
- `git reset --hard <commit_id>`: Moves the HEAD to the specified commit and discards all changes in the staging area and working directory since that commit. Use with extreme caution, as it permanently deletes uncommitted changes and rewritten history.
- `git reset HEAD <file_name>`: Unstages a file (same as `git restore --staged <file_name>`).

## 16. `git remote` - Manage Remote Repositories

- `git remote`: Lists the names of your remote repositories (usually `origin`).
- `git remote -v`: Lists remote repositories with their URLs.
- `git remote add <name> <url>`: Adds a new remote repository. (e.g., `git remote add origin https://github.com/user/repo.git`)
- `git remote rm <name>`: Removes a remote.
- `git remote rename <old_name> <new_name>`: Renames a remote.

## 17. `git fetch` - Download Changes from Remote

- `git fetch`: Downloads all new branches and commits from the remote repository but does *not- merge them into your local branches.
- `git fetch <remote_name>`: Fetches from a specific remote.
- `git fetch <remote_name> <branch_name>`: Fetches a specific branch from a remote.

## 18. `git pull` - Fetch and Merge from Remote

- `git pull`: Fetches changes from the remote repository and automatically merges them into your current local branch. (Equivalent to `git fetch` followed by `git merge`).
- `git pull <remote_name> <branch_name>`: Pulls from a specific branch on a specific remote.
- `git pull --rebase`: Fetches changes and then rebases your local commits on top of the fetched commits, creating a cleaner, linear history.

## 19. `git push` - Upload Changes to Remote

- `git push`: Pushes your local commits to the configured upstream remote and branch.
- `git push <remote_name> <branch_name>`: Pushes a specific local branch to a specific remote branch. (e.g., `git push origin main`)
- `git push -u <remote_name> <branch_name>` or `--set-upstream`: Sets the upstream branch for your local branch, so you can just use `git push` and `git pull` in the future without specifying the remote and branch.
- `git push --force` or `-f`: Forcibly pushes your changes, overwriting the remote branch. Use with extreme caution, as it can destroy history for others. Only use if you know exactly what you're doing and have communicated with your team.
- `git push --tags`: Pushes all local tags to the remote.
- `git push <remote_name> --delete <branch_name>`: Deletes a branch on the remote repository.

## 20. `git tag` - Create, List, Delete Tags

- `git tag`: Lists all tags in the repository.
- `git tag -l "v1.*"`: Lists tags matching a pattern.
- `git tag <tag_name>`: Creates a lightweight (non-annotated) tag at the current commit.
- `git tag -a <tag_name> -m "Tag message"`: Creates an annotated tag (recommended) with a message.
- `git tag -d <tag_name>`: Deletes a local tag.
- `git push <remote_name> <tag_name>`: Pushes a specific tag to the remote.
- `git push <remote_name> --tags`: Pushes all local tags to the remote.
- `git push <remote_name> --delete <tag_name>`: Deletes a tag on the remote.

## 21. `git stash` - Temporarily Save Changes

- `git stash`: Temporarily saves all modified and staged changes in your working directory, allowing you to switch branches or do other work without committing.
- `git stash save "message"`: Stashes with a descriptive message.
- `git stash list`: Lists all stashed changes.
- `git stash pop`: Applies the most recent stash and then removes it from the stash list.
- `git stash apply`: Applies the most recent stash but leaves it in the stash list.
- `git stash drop`: Deletes the most recent stash.
- `git stash clear`: Deletes all stashes.
- `git stash show <stash@{index}>`: Shows the content of a specific stash.
