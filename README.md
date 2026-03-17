# Endbricks Static Site

Static multi-page marketing site for Endbricks, designed for deployment on Sevalla free static hosting.

## Structure

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

## Local Preview

From the project root:

```bash
python3 -m http.server 4173
```

Then open:

```txt
http://localhost:4173
```

## Before Launch

1. Replace the Formspree placeholder in `contact/index.html`.
2. Replace the company credibility placeholder copy in `about/index.html` if you want something more specific.
3. Replace the privacy placeholder in `privacy/index.html`.
4. Update `robots.txt` and `sitemap.xml` if the production domain is not `endbricks.com`.
5. Swap in real case studies, testimonials, and outcome metrics as they become available.

## Sevalla Deployment

1. Push this directory to your repo.
2. Create a static site in Sevalla.
3. Set the publish directory to the repo root, or the folder containing these files.
4. Connect the production domain.
5. Test the contact form submission after adding the real endpoint.

## Content Priorities

- Strong homepage headline and proof
- Clear company credibility and implementation proof
- At least 2 credible case studies
- Privacy and form compliance
- Consistent CTA: `Book a Consultation`
