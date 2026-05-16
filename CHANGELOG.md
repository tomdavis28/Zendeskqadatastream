# Changelog

## Unreleased

- Initial scaffold: Zendesk QA reviews extractor with paged HTTP client,
  exponential backoff, and upsert-by-id CSV sink.
- 12-month default backfill window; date range overridable on the CLI.
- Configuration via `.env` (`ZQA_API_TOKEN`, `ZQA_BASE_URL`,
  `ZQA_ACCOUNT_ID`, `ZQA_WORKSPACE_ID`).
