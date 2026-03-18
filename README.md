# Endbricks Website

Static multi-page marketing site for Endbricks.

Production deployment is handled through Sevalla from the GitHub repo:

- Repo: [https://github.com/hwsbula/endbricks](https://github.com/hwsbula/endbricks)
- Hosting: Sevalla static site

## Site Structure

- `index.html`
- `services/index.html`
- `how-it-works/index.html`
- `case-studies/index.html`
- `about/index.html`
- `contact/index.html`
- `faq/index.html`
- `privacy/index.html`
- `assets/css/styles.css`
- `assets/js/site.js`

## Current Production Notes

- The site is built as plain static HTML, CSS, and JavaScript.
- Contact form submissions are handled by Formspree.
- Cloudflare Turnstile is embedded on the contact form for spam protection.
- The site is designed to be deployed from the repository root without a build step.

## Contact Form

The contact form lives in `contact/index.html`.

Current integration:

- Form endpoint: `https://formspree.io/f/xbdzpbqd`
- Turnstile site key is embedded in the form markup

Important:

- Formspree must have Turnstile enabled in its dashboard
- The Turnstile secret key must be configured in Formspree

## Local Preview

From the project root:

```bash
python3 -m http.server 4180
```

Then open:

```txt
http://localhost:4180
```

## Deployment

Sevalla should be configured as:

- Branch: `main`
- Build command: none
- Publish directory: `.`

Any push to `main` should be deployable directly by Sevalla.

## Content and Maintenance

When making updates, check these first:

- `robots.txt`
- `sitemap.xml`
- `contact/index.html`
- `privacy/index.html`

Review after any meaningful content or design change:

- homepage hero spacing and header overlay
- contact form submission and Turnstile widget
- footer layout across all core pages
- mobile layout on `index.html`, `about/index.html`, and `how-it-works/index.html`

## Design System Notes

- Headers use `Manrope`
- Body copy uses `"Text Node", "Manrope", sans-serif`
- The site relies on shared layout rules in `assets/css/styles.css`
- Interactions and small UI behaviors live in `assets/js/site.js`

## Recommended Update Workflow

1. Make edits locally.
2. Preview with `python3 -m http.server 4180`.
3. Check desktop and mobile layouts.
4. Commit changes.
5. Push to `main`.
6. Verify the Sevalla deployment and test the contact form.
