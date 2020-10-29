# Contributing Guidelines

Want to contribute to this repo? Great! We  :heart:  contributions. Just make sure to follow these guidelines.
Read both the [general guidelines](#general-guidelines) and the [coding style guidelines](#coding-style-guidelines).
By making a contribution, in any form (including, but not limited to, Issues and Pull Requests), you agree to abide by the [Code of Conduct](CODE_OF_CONDUCT.md).

## General Guidelines

### New Feature or a Bug Fix?
1. Fork the repo (you can ignore this step if you are a part of the maintainer team)
2. Create a new branch with a descriptive name of the feature or the bug you are fixing.
3. If you are a part of the maintainer team, push the branch to the remote so that others know that you are working on this branch. Otherwise, create a new issue mentioning that you would like to add a new feature or fix a bug you noticed. This lets us know that someone is already helping us fix the issue!
4. Make changes and commit them. Your commit messages should be descriptive and imperative. Read [this](http://who-t.blogspot.com/2009/12/on-commit-messages.html) for guidelines.
5. Create a pull request with a descriptive title. Clearly document any changes you made. You should be able to explain why you made those changes.

### Working on the Next Release?

Create a pull request with a descriptive title. Clearly document any changes you made. You should be able to explain why you made those changes.

## Coding Style Guidelines

We allow up to 120 characters/line as this is the width of GitHub code review; anything longer requires horizontal scrolling which makes review more difficult. This check is included when you run flake8. Documentation, comments, and docstrings should be wrapped at 79 characters, even though PEP 8 suggests 72.

## Commit Message Guidelines

Commit Guidelines inspired by [Gnome Commit Guidelines](https://wiki.gnome.org/Git/CommitMessages).

Those are only general-purpose recommended guidelines, depending on the context of each PR the following rules can vary.

Remember: the commit message is mainly for the other people, so they should be able to understand the changes made at any point in time.

### Example

```
short explanation of the commit

Longer (optional) explanation explaining exactly what's changed and why instead of how,
whether any external or private interfaces changed, what bugs were fixed (with bug
tracker reference if applicable) and so forth. Be concise but not too brief. Avoid writing long lines, use newlines when necessary.

[Reference to the issue solved, if any]
```

### Details

- First line (the brief description) must only be one sentence in imperative mood. The message should be concise, less than 50 characters if possible. Do not end it with a period.
- The long explanation is optional, although it is encouraged to be written if it helps clarify the issue tackled. Explain the "why", not the "how" there and try to wrap every line at 72 characters. Also, keep a blank like between the first line and the long explanation.
- Remember to commit your code with a [username](https://help.github.com/articles/setting-your-username-in-git/) and [email](https://help.github.com/articles/setting-your-email-in-git/).
- If there is an issue created for this commit, link it at the end of the commit message, in a new line. The issue should follow the [GitHub guidelines](https://help.github.com/articles/closing-issues-via-commit-messages/#closing-an-issue-in-the-same-repository).
