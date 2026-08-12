# tracezilla-shopify-python

Framework-neutral Python templates for integrating Shopify with the tracezilla
API. The first example implements the read-only, cross-platform **Compare
Catalogs** workflow.

## Hello World: Compare Catalogs

The command paginates both complete catalogs, maps the two API responses to a
shared model, and compares records by SKU code. Differences are a valid result
and return exit code `0`; configuration or API failures return a non-zero code.
The command never writes to either service.

## Run with Docker

```bash
cp .env.example .env
```

Fill in `.env`, then build and run:

```bash
docker compose build
docker compose run --rm app
```

Optional output controls:

```bash
docker compose run --rm app --limit=25
docker compose run --rm app --json
```

The complete catalogs are always compared. `--limit` controls only the maximum
rows displayed from each result category and defaults to 10. JSON contains the
complete result arrays.

## Tests and type checking

Python does not need to be installed on the host:

```bash
docker compose run --rm --entrypoint pytest app
docker compose run --rm --entrypoint mypy app src tests
```

Tests use in-memory clients and do not contact Shopify or tracezilla.
Runtime and development dependency versions are recorded in
`requirements.lock` for reproducible container and CI builds.

## Design

```text
GraphQL query -> Shopify client -> catalog service -> mapper --+
                                                              +-> CompareCatalogs
tracezilla API -> tracezilla client -> catalog service -> mapper+
```

Queries, HTTP clients, pagination services, response mappers, workflow logic,
and output rendering have separate responsibilities. This is ordinary Python,
without Django, Flask, or another application framework.

Canonical setup and safety guidance lives in the
[Tracezilla Integrations documentation](https://happy-bananas.github.io/tracezilla-integrations-docs/).

## Configuration safety

- Never commit `.env`; Git and Docker ignore it.
- Start with a development Shopify store and test tracezilla team.
- This workflow needs only Shopify `read_products` access.
- Never print API credentials or access tokens.
