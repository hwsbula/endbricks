# Developer Brief — Secondary CTA Implementation

**Project:** Endbricks
**Task:** Implement a secondary lead generation CTA (downloadable PDF checklist) into the existing static site
**Repo:** https://github.com/hwsbula/endbricks
**Live site:** https://endbricks.com

---

## Overview

The site currently has one conversion path: "Book a Consultation." This brief covers implementing a secondary CTA that captures a visitor's email address in exchange for a downloadable PDF checklist. The feature consists of:

1. A new email capture page at `/checklist/`
2. A new thank-you / download page at `/checklist/thank-you/`
3. CTA additions on three existing pages: homepage, case studies, and contact
4. A new Formspree form endpoint configured for this flow
5. Placement of the PDF asset in `/assets/`

No new frameworks, build tools, or dependencies are to be introduced. All work must follow the existing development standards described below.

---

## Development Standards

Read `README.md` before touching any file. Key constraints:

- **Plain HTML, CSS, and JavaScript only.** No npm, no bundlers, no frameworks.
- **No new CSS files.** Add any new rules at the bottom of `/assets/css/styles.css`.
- **No new JS files.** Add any new behavior at the bottom of `/assets/js/site.js`.
- **Typography:** Manrope via Google Fonts. Already loaded globally — do not add a second import.
- **Deployment:** Push to `main` on GitHub. Sevalla deploys automatically. No build command.
- **Local preview:** `python3 -m http.server 4180` from the project root.

---

## Design System Reference

Use only existing CSS classes wherever possible. New classes should follow the same naming conventions and be minimal.

| Element | Class(es) to use |
|---|---|
| Primary button | `button button-primary` |
| Secondary button | `button button-secondary` |
| Dark secondary button | `button button-secondary button-dark` |
| Section wrapper | `section` |
| Content width wrapper | `container` |
| Card / boxed content | `card` |
| Muted card | `card card-muted` |
| Small label above heading | `eyebrow` |
| Two-column layout | `split-feature` |
| Button group | `hero-actions` or `cta-band-actions` |
| CTA banner section | `cta-band` |
| Checklist items | `check-list` |

Study `index.html` and `contact/index.html` for structural patterns before writing any markup. All new pages must use the same `<head>` structure, `site-shell`, `site-header`, `site-footer`, and `site.js` reference as existing pages.

---

## Part 1 — PDF Asset

The PDF checklist will be provided separately. When you receive it:

- Place it at: `/assets/checklist-ai-readiness.pdf`
- Do not rename it after placing — the thank-you page will link directly to this path.

---

## Part 2 — New Page: `/checklist/index.html`

Create a new page at `checklist/index.html`. This page has one job: collect an email address in exchange for the PDF.

### Page structure

Follow the same full-page structure as `contact/index.html`. Use:
- The shared `<head>` block (favicon, GA tag, canonical, OG tags, fonts, `styles.css`)
- The same `site-header` and `site-footer` markup
- `<script src="/assets/js/site.js"></script>` at the bottom

### Head metadata

```
<title>AI Implementation Readiness Checklist | Endbricks</title>
<meta name="description" content="Download the Endbricks AI Implementation Readiness Checklist — a practical assessment tool for operations and leadership teams evaluating AI implementation.">
<link rel="canonical" href="https://endbricks.com/checklist/">
```

Update OG and Twitter tags to match.

### Page content

The page layout should mirror the `page-hero` + single `section` structure used on `contact/index.html`. Use a `split-feature` layout: the form on the left in a `card`, supporting copy on the right in the sidebar style.

**Left side — email capture form:**

- Heading: `Get the Checklist`
- Brief description (1–2 sentences): explain what the checklist is and who it is for. See `CHECKLIST-ASSET-BRIEF.md` for context.
- Form fields: Name (text, required), Work email (email, required)
- Submit button: `Download the Checklist` using `button button-primary`
- Form note below button (match the style in `contact/index.html`): `"Your email is used only to deliver the checklist. You will not be added to a mailing list."`
- Add Cloudflare Turnstile widget. Use the same site key as the contact form (`0x4AAAAAACsaPQ59_pMzmZb4`). Load the Turnstile script in `<head>` the same way `contact/index.html` does.
- Add a `_gotcha` honeypot field identical to the contact form.

**Right side — supporting copy:**

- Eyebrow: `What you will get`
- Heading: `A practical self-assessment before you build, automate, or scale.`
- A `check-list` with 4–5 bullets describing what the checklist covers. Pull from the section descriptions in `CHECKLIST-ASSET-BRIEF.md` (process readiness, use case clarity, data and systems, stakeholder readiness, success criteria).
- A brief note at the bottom: `"Takes less than 10 minutes to complete. No preparation required."`

### Form configuration (Formspree)

Create a **new, separate Formspree form** for this flow. Do not reuse the contact form endpoint.

1. Log in to Formspree and create a new form named `Endbricks Checklist Download`.
2. In the form settings, set the redirect URL to: `https://endbricks.com/checklist/thank-you/`
3. Optionally configure a confirmation email to the submitter containing the download link: `https://endbricks.com/assets/checklist-ai-readiness.pdf`
4. Enable Cloudflare Turnstile in the Formspree dashboard for this form and add the Turnstile secret key (same key used for the contact form — retrieve from the existing Formspree dashboard).
5. Replace the `action` attribute on the form with the new endpoint URL.

The form should use `method="POST"` and include the `_next` hidden field pointing to the thank-you URL as a fallback:
```html
<input type="hidden" name="_next" value="https://endbricks.com/checklist/thank-you/">
```

---

## Part 3 — New Page: `/checklist/thank-you/index.html`

Create a thank-you page at `checklist/thank-you/index.html`. This is the page the visitor lands on after submitting their email.

### Purpose

Deliver the PDF download and reinforce the next step (booking a consultation).

### Page structure

Use the same `<head>`, header, footer, and JS reference as all other pages.

### Head metadata

```
<title>Your Checklist is Ready | Endbricks</title>
<meta name="robots" content="noindex">
```

The `noindex` meta tag prevents this page from being indexed by search engines and gamed for a free download without submitting an email.

### Page content

Keep this page simple. A single `section` with a `container` and a `cta-band`-style card is appropriate.

Structure:
- Eyebrow: `Your download is ready`
- Heading: `The AI Implementation Readiness Checklist`
- One sentence: `Use this to assess where your workflows, data, and team stand before starting an AI implementation.`
- A prominent download button: `Download the Checklist (PDF)` linking to `/assets/checklist-ai-readiness.pdf` with `download` attribute set.

Use `button button-primary` for the download button.

Below the download section, add a secondary prompt:

- Heading: `Ready to take the next step?`
- One sentence: `If the checklist surfaces areas you want to work through, a consultation is the right next conversation.`
- `button button-secondary` linking to `/contact/` with text: `Book a Consultation`

---

## Part 4 — Modify Existing Pages

Three existing pages need secondary CTA additions. In each case, add the secondary CTA without removing or repositioning the existing primary CTA.

---

### 4a — Homepage (`index.html`)

**Location:** The `hero-actions` div at line 97–100.

Current markup:
```html
<div class="hero-actions hero-actions-centered">
  <a class="button button-primary" href="/contact/">Book a Consultation</a>
  <a class="button button-secondary button-dark" href="/how-it-works/">See How It Works</a>
</div>
```

Replace the "See How It Works" secondary button with the checklist CTA:
```html
<a class="button button-secondary button-dark" href="/checklist/">Get the Readiness Checklist</a>
```

"See How It Works" is a lower-value CTA for this position. The checklist is a better secondary conversion. If there is a preference to keep both, move "See How It Works" to a text link below the button group using the `text-link` class.

---

### 4b — Case Studies page (`case-studies/index.html`)

**Location:** After the final case study entry, before the closing `</section>` of the main case study section.

Add a `cta-band` style block (match the pattern from `index.html` lines 486–498) with:
- Eyebrow: `Not sure if your workflow is ready?`
- Heading: `Download the readiness checklist before your next step.`
- One sentence: `A practical self-assessment covering process maturity, use case clarity, data readiness, and stakeholder alignment.`
- Primary button: `Get the Checklist` linking to `/checklist/`

---

### 4c — Contact page (`contact/index.html`)

**Location:** The `contact-sidebar` div (lines 116–136). Below the "On capacity" block and before the closing `</div>`.

Add a new `contact-direct` block (match the existing pattern in the sidebar):

```html
<div class="contact-direct">
  <strong>Not ready to book yet?</strong>
  <p>Download the AI Implementation Readiness Checklist — a self-assessment that helps you evaluate your workflows, data, and team before starting an engagement.</p>
  <a class="button button-secondary" href="/checklist/">Get the Checklist</a>
</div>
```

---

## Part 5 — Update `sitemap.xml`

Add the new checklist page to `sitemap.xml`. The thank-you page should not be included (it is `noindex`).

Add:
```xml
<url>
  <loc>https://endbricks.com/checklist/</loc>
  <changefreq>monthly</changefreq>
  <priority>0.6</priority>
</url>
```

---

## Part 6 — Testing Checklist

Before pushing to `main`, verify the following locally using `python3 -m http.server 4180`:

- [ ] `/checklist/` loads with no broken styles or missing assets
- [ ] `/checklist/thank-you/` loads correctly and the PDF download button works
- [ ] The email capture form on `/checklist/` submits and redirects to `/checklist/thank-you/`
- [ ] Turnstile widget renders on the checklist form
- [ ] Honeypot field is present and hidden
- [ ] Homepage hero CTA group renders correctly on desktop and mobile
- [ ] Case studies page checklist CTA renders correctly
- [ ] Contact page sidebar secondary CTA renders correctly
- [ ] `sitemap.xml` updated
- [ ] No console errors on any modified or new page
- [ ] All new pages render correctly at 375px width (mobile)
- [ ] Header nav and footer render identically to existing pages on all new pages

After deploying to production:
- [ ] Submit the checklist form with a real email address and confirm the redirect works
- [ ] Confirm the PDF downloads from the thank-you page
- [ ] Confirm the Formspree dashboard receives the submission
- [ ] Confirm Cloudflare Turnstile is blocking spam submissions (check Formspree spam folder)

---

## Files to Create

```
checklist/index.html
checklist/thank-you/index.html
assets/checklist-ai-readiness.pdf        ← provided separately
```

## Files to Modify

```
index.html                               ← hero CTA
case-studies/index.html                  ← post-case-study CTA block
contact/index.html                       ← sidebar secondary CTA
sitemap.xml                              ← add /checklist/
assets/css/styles.css                    ← any new rules (minimal, bottom of file)
assets/js/site.js                        ← any new behavior (minimal, bottom of file)
```

## Files to Leave Unchanged

All other pages. Do not modify shared styles in a way that affects existing pages.
