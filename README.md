# Cross-Site Scripting Analysis

This repository preserves a 2023 Safe Programming coursework exercise about cross-site scripting (XSS), browser/server parser differences, Flask session cookies, CSRF state, and HTTPS configuration. It includes the supplied deliberately vulnerable Flask application, my analysis and helper script, and my report.

> [!CAUTION]
> The application is intentionally vulnerable and prints its temporary session secret. Run it only on a trusted local machine. The maintained launcher binds to `127.0.0.1` by default.

## Tech stack

- Python 3.10 or newer, Flask, Jinja2, Beautiful Soup, and Cryptography
- HTML, JavaScript, XSS, CSRF, HMAC-signed session cookies, and parser differentials
- OpenSSL and local TLS certificates

## Included materials

- `assignment/`: supplied Safe Programming exercise brief.
- `framework/XSSApp-1.1.0/`: supplied deliberately vulnerable Flask application, with my HTTPS changes.
- `solution/`: my session-cookie helper.
- `results/report.pdf`: my report.
- `tests/` and `scripts/`: local validation and setup helpers.

The supplied application is the subject of the analysis. Historical certificates, private keys, certificate requests, and configuration containing personal details were deliberately excluded.

## Implementation notes

The pristine framework was reconstructed from the recovered 2023 package by reverting only the HTTPS-specific `app.run` and package-manifest changes described in the report. Other differences from the earlier 2022 framework are course version changes and remain in the first commit.

## Analysis scope

The report documents:

- acceptance of an email-like value without `@`;
- browser/server disagreement over malformed HTML parsing;
- reflected XSS and one-time execution logic;
- Flask session decoding and re-signing when the local secret is known;
- the effect of `HttpOnly`; and
- defensive recommendations including parser choice, CSP, allowlists, and output encoding.

Personal identifiers and live-looking historical cookie, CSRF, email, and phone values were redacted from the report. The technical explanation and screenshots remain intact.

## Run locally

Install the maintained environment and generate a disposable 30-day localhost certificate:

```bash
uv sync
./scripts/generate-local-certificates.sh
uv run start-xss-app
```

Open `https://127.0.0.1:5000`. A browser warning is expected because the generated certificate is self-signed. The key and certificate are ignored by Git and can be deleted or regenerated at any time.

The launcher uses `127.0.0.1` unless `XSSAPP_HOST` is explicitly set. Do not expose this exercise to another device or an untrusted network.

## Session helper

The recovered helper was updated to use Flask's supported serializer instead of an internal `itsdangerous` API. It accepts a cookie from this local app and the base64 secret printed by the same local process:

```bash
uv run python -m solution.flask_cookie_generator SESSION_COOKIE LOGGED_SECRET
```

Use it only with this repository's local exercise instance. The helper uses Flask's own serializer and does not require a separate cookie-analysis tool.

## Verify

```bash
uv run pytest
uv run ruff check solution tests
uv run ruff format --check solution tests
```

The tests exercise the local Flask test client, CSRF flow, intentionally accepted iframe input, rejected event attributes, and session-cookie re-signing. No CI workflow is included because this is a small historical coursework repository with a narrow local validation path.

## License

No blanket license is asserted over the supplied course framework or report.
