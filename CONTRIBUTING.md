# Contributing

Thanks for taking a look at this repository.

This is primarily a personal portfolio, but bug reports and practical improvements are welcome.

## Contribution Scope

Good contributions:

- Bug fixes
- README/documentation corrections
- Test improvements
- Refactoring that improves clarity without changing behavior

Please avoid:

- Adding unfinished projects
- Large dependency changes without clear need
- Auto-generated files or local environment files

## Basic Quality Expectations

For Python projects:

- Keep functions readable and small
- Add or update tests when behavior changes
- Run project tests before submitting changes

For React projects:

- Keep components maintainable
- Ensure `npm run build` succeeds
- Do not commit `node_modules` or build outputs

## Pull Request Checklist

1. Explain what changed and why.
2. List how you verified it (tests/build/manual run).
3. Keep scope focused to one project or one theme.
4. Update related docs if behavior changed.

## Security and Secrets

- Never commit API keys or `.env` files.
- Use `.env.example` when a project needs environment variables.
- Do not commit database files, model artifacts, or logs.
