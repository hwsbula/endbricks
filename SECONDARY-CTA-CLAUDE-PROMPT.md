You are working inside the Endbricks website repository — a plain static HTML/CSS/JS site with no build step. Before writing any code, read the following files in full so you understand the existing structure, conventions, and design system:

- `README.md`
- `index.html`
- `contact/index.html`
- `case-studies/index.html`
- `assets/css/styles.css`
- `assets/js/site.js`
- `sitemap.xml`

Do not write a single line of code until you have read all of these.

---

## Your task

Implement a secondary lead generation CTA across this site. The feature allows visitors to download a PDF checklist (the AI Implementation Readiness Checklist) in exchange for their name and email address. This is a secondary conversion path alongside the existing "Book a Consultation" primary CTA.

You will create two new pages and modify three existing ones. All work must strictly follow the conventions you observed in the files above. No new frameworks, npm packages, build tools, or dependencies. No new CSS or JS files — extend `styles.css` and `site.js` only if needed, and only at the bottom of those files.

---

## Constraints

- Match the `<head>` block structure of existing pages exactly: favicon, GA tag, canonical, OG/Twitter meta, JSON-LD, font import, `styles.css` link.
- Match the `site-shell`, `site-header`, `site-footer`, and `<script src="/assets/js/site.js">` structure of existing pages exactly.
- Use only existing CSS classes. Do not invent new ones unless absolutely necessary, and if you do, name them consistently with the existing pattern.
- The Turnstile site key for all forms is: `0x4AAAAAACsaPQ59_pMzmZb4`. Load the Turnstile script in `<head>` the same way `contact/index.html` does.
- The PDF asset will be placed at `/assets/checklist-ai-readiness.pdf`. Treat this path as final — do not change it.
- The Formspree endpoint for the checklist form is a placeholder: `CHECKLIST_FORMSPREE_ENDPOINT`. Use this string as the `action` value. The owner will replace it with the real endpoint after creating a new Formspree form.

---

## Step 1 — Create `/checklist/index.html`

This page captures the visitor's name and email in exchange for the PDF. It has one job.

**Page title and meta:**
```
<title>AI Implementation Readiness Checklist | Endbricks</title>
<meta name="description" content="Download the Endbricks AI Implementation Readiness Checklist — a practical assessment tool for operations and leadership teams evaluating AI implementation.">
<link rel="canonical" href="https://endbricks.com/checklist/">
```
Update OG and Twitter tags to match. Use the same JSON-LD `WebPage` structure as other pages, adapted for this URL.

**Page layout:**
Mirror the `page-hero` + `section` + `split-feature` layout from `contact/index.html`. The form goes on the left inside a `card`. Supporting copy goes on the right in the sidebar style.

**Page hero:**
- Eyebrow: `Free download`
- H1: `The AI Implementation Readiness Checklist`
- Lead: `A self-assessment for operations and leadership teams evaluating AI implementation — before building anything.`

**Left side — the form:**
- H2: `Get the Checklist`
- Description: `A practical tool for assessing whether your workflows, data, and team are ready for AI implementation. Takes less than 10 minutes to complete.`
- Fields: Name (text, required), Work email (email, required)
- Honeypot: `<input type="text" name="_gotcha" class="hidden-field" tabindex="-1" autocomplete="off">` — match `contact/index.html` exactly
- Redirect fallback: `<input type="hidden" name="_next" value="https://endbricks.com/checklist/thank-you/">`
- Turnstile widget: `<div class="cf-turnstile" data-sitekey="0x4AAAAAACsaPQ59_pMzmZb4"></div>`
- Submit button: `Download the Checklist` using `button button-primary`
- Form note below the button: `Your email is used only to deliver the checklist. You will not be added to a mailing list.` — use the `form-note` class from `contact/index.html`
- Form `action`: `CHECKLIST_FORMSPREE_ENDPOINT`, `method="POST"`

**Right side — supporting copy:**
- Eyebrow: `What you will get`
- H2: `A structured assessment across five areas.`
- A `check-list` with these five items:
  - `Process readiness — whether your workflows are stable and documented enough to automate`
  - `Use case clarity — whether the problem is specific enough to scope and measure`
  - `Data and systems — whether the right inputs exist in an accessible form`
  - `Stakeholder and change readiness — whether there is internal alignment on ownership and adoption`
  - `Success criteria — whether you can define what a working implementation looks like`
- Note at the bottom: `No preparation required. Bring your knowledge of your own workflows.`

---

## Step 2 — Create `/checklist/thank-you/index.html`

This is the page visitors land on after submitting the form. It delivers the download and prompts the next step.

**Page title and meta:**
```
<title>Your Checklist is Ready | Endbricks</title>
<meta name="robots" content="noindex">
```
Do not include this page in any sitemaps. Do not add OG tags — it is a transactional page, not a shareable one.

**Page layout:**
Keep this simple. A single centered `section` with a `container`. Use the `cta-band` pattern from `index.html` (the "Start with a focused conversation" section near the bottom) as a structural reference — adapt it, do not copy it verbatim.

**Content — download block:**
- Eyebrow: `Your download is ready`
- H1: `The AI Implementation Readiness Checklist`
- One sentence: `Use this to assess where your workflows, data, and team stand before starting an AI implementation.`
- Download button: `<a class="button button-primary" href="/assets/checklist-ai-readiness.pdf" download>Download the Checklist (PDF)</a>`

**Content — next step block (below the download):**
- H2: `Ready to take the next step?`
- One sentence: `If the checklist surfaces gaps you want to work through, a consultation is the right next conversation.`
- Button: `Book a Consultation` using `button button-secondary` linking to `/contact/`

---

## Step 3 — Modify `index.html` (homepage)

Find this block in the hero section:

```html
<div class="hero-actions hero-actions-centered">
  <a class="button button-primary" href="/contact/">Book a Consultation</a>
  <a class="button button-secondary button-dark" href="/how-it-works/">See How It Works</a>
</div>
```

Replace it with:

```html
<div class="hero-actions hero-actions-centered">
  <a class="button button-primary" href="/contact/">Book a Consultation</a>
  <a class="button button-secondary button-dark" href="/checklist/">Get the Readiness Checklist</a>
</div>
<p style="text-align:center;margin-top:0.75rem;"><a class="text-link" href="/how-it-works/">See how it works</a></p>
```

This preserves the "How It Works" path as a lower-priority text link while elevating the checklist to the secondary button position.

---

## Step 4 — Modify `case-studies/index.html`

Read the full file. Find the closing `</section>` tag of the main case study listing section (the section that contains the individual case study cards or entries). Immediately before that closing tag, insert a `cta-band` block.

Match the structure and class pattern of the `cta-band` in `index.html` (the "Start with a focused conversation" section). Adapt the content:

- Eyebrow: `Not sure if your workflow is ready?`
- H2: `Download the checklist before your next step.`
- Body: `A self-assessment covering process maturity, use case clarity, data readiness, and stakeholder alignment.`
- Button: `Get the Checklist` using `button button-primary` linking to `/checklist/`

---

## Step 5 — Modify `contact/index.html`

Find the `contact-sidebar` div. It currently ends with the "On capacity" `contact-direct` block. After that block and before the closing `</div>` of the sidebar, add:

```html
<div class="contact-direct">
  <strong>Not ready to book yet?</strong>
  <p>Download the AI Implementation Readiness Checklist — a self-assessment covering workflows, data readiness, and team alignment before starting an engagement.</p>
  <a class="button button-secondary" href="/checklist/">Get the Checklist</a>
</div>
```

---

## Step 6 — Update `sitemap.xml`

Add one entry for the checklist page. Do not add the thank-you page.

```xml
<url>
  <loc>https://endbricks.com/checklist/</loc>
  <changefreq>monthly</changefreq>
  <priority>0.6</priority>
</url>
```

---

## When you are done

Confirm the following before finishing:

- Both new pages use the exact same header, footer, and script structure as existing pages
- The checklist form has the honeypot field, Turnstile widget, `_next` hidden field, and `CHECKLIST_FORMSPREE_ENDPOINT` placeholder as the action
- The thank-you page has `<meta name="robots" content="noindex">` and no canonical tag
- The homepage hero still has two buttons — the primary CTA unchanged, the secondary now pointing to `/checklist/`
- The case studies and contact pages have their new CTA blocks in the correct positions
- `sitemap.xml` has the checklist URL and does not have the thank-you URL
- No existing page structure, styles, or behavior has been altered beyond the specified additions

Do not push to the repository. Leave that for the owner to review and deploy.
