# Cross-Site Scripting Analysis

This repository preserves a 2023 Safe Programming coursework exercise about cross-site scripting (XSS), browser/server parser differences, Flask session cookies, CSRF state, and HTTPS configuration. It includes the supplied deliberately vulnerable Flask application, my analysis and helper script, my report, and the third-party Flask-Unsign source found with the project.

> [!CAUTION]
> The application is intentionally vulnerable and prints its temporary session secret. Run it only on a trusted local machine. The maintained launcher binds to `127.0.0.1` by default.

## Tech stack

- Python 3.10 or newer, Flask, Jinja2, Beautiful Soup, and Cryptography
- HTML, JavaScript, XSS, CSRF, HMAC-signed session cookies, and parser differentials
- OpenSSL and local TLS certificates

## Authorship and provenance

| Path | Classification | Author or source |
| --- | --- | --- |
| `assignment/` | Course-supplied | Safe Programming exercise brief |
| `framework/XSSApp-1.1.0/` | Course-supplied framework | Deliberately vulnerable 2023 Flask application |
| Framework HTTPS changes in the second commit | Authored solution work | Me |
| `solution/` | Authored solution work | Me |
| `results/report.pdf` | Authored submission | Me |
| `third_party/Flask-Unsign/` | Third-party reference tool | Luke Paris (Paradoxis), Flask-Unsign 1.2.0, MIT License |
| Tests, scripts, and repository documentation | Tests and tooling | Me |

The course framework remains included because it is the subject of the analysis. The repository does not claim that framework or Flask-Unsign as my work. Historical certificates, private keys, certificate requests, and configuration containing personal details were deliberately excluded.

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

Use it only with this repository's local exercise instance. Flask-Unsign is retained under `third_party/` for historical context; it is not required by the maintained helper or application.

## Verify

```bash
uv run pytest
uv run ruff check solution tests
uv run ruff format --check solution tests
```

The tests exercise the local Flask test client, CSRF flow, intentionally accepted iframe input, rejected event attributes, and session-cookie re-signing. No CI workflow is included because this is a small historical coursework repository with a narrow local validation path.

## License

No blanket license is asserted over the course framework or report. Flask-Unsign retains its MIT license in `third_party/Flask-Unsign/LICENSE.md`; the root provenance table distinguishes it from the authored work.
