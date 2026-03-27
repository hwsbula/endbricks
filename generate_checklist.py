#!/usr/bin/env python3
"""
Endbricks — AI Implementation Readiness Checklist PDF Generator
Creates a branded, print-ready PDF with fillable checkboxes and auto-scoring.
"""

import os

# ─── Paths ──────────────────────────────────────────────────────────
BASE_DIR = "/Users/hws-bula/Downloads/endbricks"
FONT_DIR = os.path.join(BASE_DIR, ".fonts")
FONT_PATH = os.path.join(FONT_DIR, "Manrope-Variable.ttf")
LOGO_PATH = os.path.join(BASE_DIR, "assets/endbricks-logo-black.svg")
OUTPUT_PATH = os.path.join(BASE_DIR, "endbricks-ai-readiness-checklist.pdf")

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame,
    Paragraph, Spacer, Table, TableStyle,
    PageBreak, Flowable, KeepTogether
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from svglib.svglib import svg2rlg

# ─── Font Registration ─────────────────────────────────────────────
pdfmetrics.registerFont(TTFont("Manrope", FONT_PATH))
pdfmetrics.registerFont(TTFont("Manrope-Bold", FONT_PATH))
pdfmetrics.registerFont(TTFont("Manrope-SemiBold", FONT_PATH))
registerFontFamily("Manrope",
    normal="Manrope", bold="Manrope-Bold",
    italic="Manrope", boldItalic="Manrope-Bold"
)

# ─── Colors ─────────────────────────────────────────────────────────
DEEP_PURPLE  = HexColor("#0D004C")
TEXT_PRIMARY  = HexColor("#1A1D2E")
TEXT_SECONDARY = HexColor("#3D4055")
TEXT_MUTED    = HexColor("#6B6E7F")
ACCENT_MINT   = HexColor("#77E0B5")
ACCENT_MINT_LIGHT = HexColor("#E8FAF2")
ACCENT_AMBER  = HexColor("#F4AF64")
ACCENT_RED    = HexColor("#E8734A")
BG_CALLOUT    = HexColor("#F4F5F7")
BG_SCORE      = HexColor("#F0F1F5")
BORDER_LIGHT  = HexColor("#D8DAE0")
WHITE         = HexColor("#FFFFFF")

# ─── Page Setup ─────────────────────────────────────────────────────
PAGE_W, PAGE_H = letter
MARGIN_L = 0.75 * inch
MARGIN_R = 0.75 * inch
MARGIN_T = 0.65 * inch
MARGIN_B = 0.6 * inch
CONTENT_W = PAGE_W - MARGIN_L - MARGIN_R

# ─── Styles ─────────────────────────────────────────────────────────
s = {}
s["cover_title"] = ParagraphStyle(
    "cover_title", fontName="Manrope-Bold", fontSize=28, leading=34,
    textColor=DEEP_PURPLE, spaceAfter=6)
s["cover_subtitle"] = ParagraphStyle(
    "cover_subtitle", fontName="Manrope", fontSize=13, leading=18,
    textColor=TEXT_SECONDARY, spaceAfter=24)
s["cover_framing"] = ParagraphStyle(
    "cover_framing", fontName="Manrope", fontSize=10.5, leading=16.5,
    textColor=TEXT_SECONDARY, spaceAfter=10)
s["cover_brand"] = ParagraphStyle(
    "cover_brand", fontName="Manrope-Bold", fontSize=9, leading=13,
    textColor=TEXT_MUTED)
s["intro_body"] = ParagraphStyle(
    "intro_body", fontName="Manrope", fontSize=9.5, leading=15,
    textColor=TEXT_SECONDARY, spaceAfter=8)
s["section_number"] = ParagraphStyle(
    "section_number", fontName="Manrope-Bold", fontSize=8, leading=10,
    textColor=ACCENT_MINT, spaceAfter=2)
s["section_title"] = ParagraphStyle(
    "section_title", fontName="Manrope-Bold", fontSize=14, leading=18,
    textColor=DEEP_PURPLE, spaceAfter=2)
s["section_desc"] = ParagraphStyle(
    "section_desc", fontName="Manrope", fontSize=9, leading=13,
    textColor=TEXT_MUTED, spaceAfter=10)
s["item_text"] = ParagraphStyle(
    "item_text", fontName="Manrope", fontSize=9.2, leading=13.5,
    textColor=TEXT_PRIMARY)
s["callout_label"] = ParagraphStyle(
    "callout_label", fontName="Manrope-SemiBold", fontSize=8, leading=11,
    textColor=TEXT_SECONDARY, spaceAfter=3)
s["callout_text"] = ParagraphStyle(
    "callout_text", fontName="Manrope", fontSize=8.5, leading=13,
    textColor=TEXT_MUTED)
s["cta_heading"] = ParagraphStyle(
    "cta_heading", fontName="Manrope-Bold", fontSize=13, leading=17,
    textColor=DEEP_PURPLE, spaceAfter=5)
s["cta_body"] = ParagraphStyle(
    "cta_body", fontName="Manrope", fontSize=9, leading=14,
    textColor=TEXT_SECONDARY, spaceAfter=6)
s["cta_link"] = ParagraphStyle(
    "cta_link", fontName="Manrope-Bold", fontSize=9.5, leading=13,
    textColor=DEEP_PURPLE)
s["footer_brand"] = ParagraphStyle(
    "footer_brand", fontName="Manrope", fontSize=8, leading=11,
    textColor=TEXT_MUTED)


# ─── Custom Flowables ──────────────────────────────────────────────

class AccentBar(Flowable):
    def __init__(self, width, height=2, color=ACCENT_MINT):
        Flowable.__init__(self)
        self.width = width
        self.height = height
        self._color = color
    def draw(self):
        self.canv.setFillColor(self._color)
        self.canv.roundRect(0, 0, self.width, self.height, 1, fill=1, stroke=0)
    def wrap(self, aW, aH):
        return (self.width, self.height)


class SectionDivider(Flowable):
    def __init__(self, width, color=BORDER_LIGHT):
        Flowable.__init__(self)
        self.width = width
        self._color = color
    def draw(self):
        self.canv.setStrokeColor(self._color)
        self.canv.setLineWidth(0.5)
        self.canv.line(0, 0, self.width, 0)
    def wrap(self, aW, aH):
        return (self.width, 1)


class CheckboxItem(Flowable):
    """Fillable checkbox with label text. Named cb_S_I (section_item)."""
    def __init__(self, text, style, content_width, section_idx, item_idx):
        Flowable.__init__(self)
        self._name = f"cb_{section_idx}_{item_idx}"
        self._style = style
        self._content_width = content_width
        self._cb_size = 10
        self._gap = 8
        self._para = Paragraph(text, style)

    def wrap(self, aW, aH):
        tw = self._content_width - self._cb_size - self._gap - 4
        _, ph = self._para.wrap(tw, aH)
        self.height = max(ph, self._cb_size) + 5
        self.width = self._content_width
        return (self.width, self.height)

    def draw(self):
        cb_y = self.height - self._cb_size - 2
        self.canv.acroForm.checkbox(
            name=self._name, x=0, y=cb_y,
            size=self._cb_size, borderWidth=1,
            borderColor=HexColor("#B0B3BE"),
            fillColor=WHITE, buttonStyle="check",
            checked=False, relative=True,
        )
        tw = self._content_width - self._cb_size - self._gap - 4
        self._para.wrap(tw, 1000)
        self._para.drawOn(self.canv, self._cb_size + self._gap,
                          self.height - self._para.height - 1)


class CalloutBox(Flowable):
    def __init__(self, label, body, width, l_style, b_style,
                 bg=BG_CALLOUT, accent=ACCENT_AMBER):
        Flowable.__init__(self)
        self._w = width
        self._bg = bg
        self._accent = accent
        self._pad = 10
        self._label = Paragraph(label, l_style)
        self._body = Paragraph(body, b_style)

    def wrap(self, aW, aH):
        iw = self._w - 2 * self._pad - 4
        _, lh = self._label.wrap(iw, aH)
        _, bh = self._body.wrap(iw, aH)
        self.height = lh + bh + 2 * self._pad + 2
        self.width = self._w
        return (self.width, self.height)

    def draw(self):
        self.canv.setFillColor(self._bg)
        self.canv.roundRect(0, 0, self._w, self.height, 4, fill=1, stroke=0)
        self.canv.setFillColor(self._accent)
        self.canv.roundRect(0, 2, 3, self.height - 4, 1.5, fill=1, stroke=0)
        iw = self._w - 2 * self._pad - 4
        self._label.wrap(iw, 1000)
        self._body.wrap(iw, 1000)
        y = self.height - self._pad - self._label.height
        self._label.drawOn(self.canv, self._pad + 4, y)
        y -= self._body.height + 2
        self._body.drawOn(self.canv, self._pad + 4, y)


class ScoreCard(Flowable):
    """Auto-scoring card with form text fields for each section and total."""

    LABELS = [
        "Process Readiness",
        "Use Case Clarity",
        "Data and Systems",
        "Stakeholder & Change Readiness",
        "Success Criteria",
    ]

    def __init__(self, width):
        Flowable.__init__(self)
        self.width = width
        self._pad = 16
        # Title(16) + gap(10) + 5 rows(5*22=110) + divider(16) + total(24) +
        # gap(10) + interp(20) + gap(10) + ranges(4*15=60) + padding(32) = 308
        self.height = 298

    def wrap(self, aW, aH):
        return (self.width, self.height)

    def draw(self):
        c = self.canv
        w = self.width
        h = self.height
        p = self._pad

        # Background
        c.setFillColor(BG_SCORE)
        c.roundRect(0, 0, w, h, 6, fill=1, stroke=0)

        # Left accent bar
        c.setFillColor(DEEP_PURPLE)
        c.roundRect(0, 4, 4, h - 8, 2, fill=1, stroke=0)

        # Title
        y = h - p - 13
        c.setFont("Manrope-Bold", 13)
        c.setFillColor(DEEP_PURPLE)
        c.drawString(p + 4, y, "Your Readiness Score")

        # Section score rows
        y -= 26
        field_x = w - p - 54

        for i, label in enumerate(self.LABELS):
            c.setFont("Manrope", 9)
            c.setFillColor(TEXT_PRIMARY)
            c.drawString(p + 4, y + 3, label)

            # Dotted connector
            lbl_end = p + 4 + c.stringWidth(label, "Manrope", 9) + 6
            c.setStrokeColor(BORDER_LIGHT)
            c.setDash(1, 3)
            c.line(lbl_end, y + 6, field_x - 6, y + 6)
            c.setDash()

            # Score text field
            c.acroForm.textfield(
                name=f"score_{i+1}",
                x=field_x, y=y - 2, width=50, height=17,
                value="0 / 6", fontSize=9,
                fontName="Helvetica-Bold",
                borderWidth=0.5, borderColor=BORDER_LIGHT,
                fillColor=WHITE, textColor=DEEP_PURPLE,
                fieldFlags="readOnly",
                relative=True,
            )
            y -= 22

        # Divider
        y -= 4
        c.setStrokeColor(BORDER_LIGHT)
        c.setLineWidth(0.5)
        c.line(p + 4, y, w - p, y)
        y -= 20

        # Total row
        c.setFont("Manrope-Bold", 11)
        c.setFillColor(DEEP_PURPLE)
        c.drawString(p + 4, y + 3, "TOTAL")

        c.acroForm.textfield(
            name="score_total",
            x=field_x, y=y - 2, width=50, height=19,
            value="0 / 30", fontSize=10,
            fontName="Helvetica-Bold",
            borderWidth=1, borderColor=ACCENT_MINT,
            fillColor=ACCENT_MINT_LIGHT, textColor=DEEP_PURPLE,
            fieldFlags="readOnly",
            relative=True,
        )
        y -= 26

        # Interpretation field
        c.acroForm.textfield(
            name="interpretation",
            x=p + 4, y=y - 2,
            width=w - 2 * p - 8, height=16,
            value="Check items above to calculate your readiness score.",
            fontSize=8.5, fontName="Helvetica-Oblique",
            borderWidth=0, fillColor=BG_SCORE,
            textColor=TEXT_SECONDARY,
            fieldFlags="readOnly",
            relative=True,
        )
        y -= 24

        # Score range legend
        ranges = [
            ("26 \u2013 30", "Strong readiness", ACCENT_MINT),
            ("19 \u2013 25", "Moderate \u2014 address gaps before engaging", ACCENT_AMBER),
            ("11 \u2013 18", "Significant gaps \u2014 prioritize fundamentals", ACCENT_RED),
            ("0 \u2013 10",  "Foundation work needed first", TEXT_MUTED),
        ]
        for rng, desc, color in ranges:
            c.setFillColor(color)
            c.circle(p + 8, y + 3, 3, fill=1, stroke=0)
            c.setFont("Manrope-Bold", 7.5)
            c.setFillColor(TEXT_PRIMARY)
            c.drawString(p + 16, y, rng)
            c.setFont("Manrope", 7.5)
            c.setFillColor(TEXT_SECONDARY)
            c.drawString(p + 58, y, desc)
            y -= 14


class CTABlock(Flowable):
    def __init__(self, heading, body, link, width):
        Flowable.__init__(self)
        self._w = width
        self._pad = 16
        self._h = Paragraph(heading, s["cta_heading"])
        self._b = Paragraph(body, s["cta_body"])
        self._l = Paragraph(link, s["cta_link"])

    def wrap(self, aW, aH):
        inner = self._w - 2 * self._pad
        _, hh = self._h.wrap(inner, aH)
        _, bh = self._b.wrap(inner, aH)
        _, lh = self._l.wrap(inner, aH)
        self.height = hh + bh + lh + 2 * self._pad + 8
        self.width = self._w
        return (self.width, self.height)

    def draw(self):
        c = self.canv
        c.setFillColor(ACCENT_MINT_LIGHT)
        c.roundRect(0, 0, self._w, self.height, 6, fill=1, stroke=0)
        c.setFillColor(ACCENT_MINT)
        c.roundRect(self._pad, self.height - 3,
                     self._w - 2 * self._pad, 3, 1.5, fill=1, stroke=0)

        inner = self._w - 2 * self._pad
        self._h.wrap(inner, 1000)
        self._b.wrap(inner, 1000)
        self._l.wrap(inner, 1000)

        y = self.height - self._pad - 6 - self._h.height
        self._h.drawOn(c, self._pad, y)
        y -= self._b.height + 2
        self._b.drawOn(c, self._pad, y)
        y -= self._l.height + 4
        self._l.drawOn(c, self._pad, y)


# ─── Content Data (statements, not questions) ──────────────────────

SECTIONS = [
    {
        "number": "SECTION 1",
        "title": "Process Readiness",
        "desc": "Check each statement that is true for the workflow you plan to automate.",
        "items": [
            "The target workflow can be described step-by-step without consulting documentation.",
            "Everyone who handles this process executes it the same way.",
            "The specific step where time is lost or errors occur most frequently has been identified.",
            "The current process is documented in writing, and that documentation is current and accurate.",
            "This workflow has been stable for at least 90 days \u2014 without significant changes to steps, tools, or team.",
            "The exceptions and edge cases in this workflow are understood and accounted for, not just the happy path.",
        ],
        "callout_label": "Why this matters:",
        "callout": "Automating a broken or inconsistent process compounds the problem. Unchecked items here represent instability that should be resolved before implementation, not after.",
    },
    {
        "number": "SECTION 2",
        "title": "Use Case Clarity",
        "desc": "Check each statement that is true for the problem you intend to solve.",
        "items": [
            "The problem can be described in a single sentence \u2014 without using the word \u201cAI.\u201d",
            "The cost of this problem has been estimated in real terms \u2014 hours per week, error rate, or headcount involved.",
            "This is one scoped problem, not a cluster of related problems that have not yet been separated.",
            "A simpler, non-AI solution has been considered and ruled out.",
            "This workflow happens frequently enough \u2014 in volume or regularity \u2014 to justify the implementation effort.",
            "The expected output of an AI system has been defined, including who would consume it.",
        ],
        "callout_label": "Why this matters:",
        "callout": "Vague problem statements produce vague solutions. Unchecked items here mean the implementation cannot be properly scoped or measured \u2014 and the pilot will almost certainly stall.",
    },
    {
        "number": "SECTION 3",
        "title": "Data and Systems",
        "desc": "Check each statement that is true about the data and systems involved.",
        "items": [
            "The exact location of the data required for this use case is known.",
            "The data is in a machine-readable format \u2014 not primarily in documents, email threads, or verbal handoffs.",
            "The access rights and permissions needed to connect to the relevant data systems are available.",
            "The data is consistently structured and does not vary significantly between records, sources, or time periods.",
            "The destination for the AI output has been identified \u2014 the specific system or tool the team would actually use.",
            "A clear integration path exists between current systems, or the need for custom development is understood.",
        ],
        "callout_label": "Why this matters:",
        "callout": "Data gaps and access barriers are the most common cause of delayed AI pilots. Unchecked items here will surface during build \u2014 identifying them now saves significant time and cost.",
    },
    {
        "number": "SECTION 4",
        "title": "Stakeholder and Change Readiness",
        "desc": "Check each statement that is true about internal alignment and adoption planning.",
        "items": [
            "A named individual is accountable for making this implementation succeed \u2014 not just sponsoring it.",
            "The team that will use the output has input into how it is designed.",
            "Likely sources of resistance have been identified, and a plan exists to address them.",
            "Leadership is aligned on the fact that AI implementation includes a training and adoption phase \u2014 not just a build phase.",
            "Capacity or budget has been allocated for change management, separate from the build budget.",
            "The purpose of this initiative has been communicated clearly to the team that will be most affected.",
        ],
        "callout_label": "Why this matters:",
        "callout": "Most AI implementation failures are organizational, not technical. Unchecked items here consistently lead teams to underestimate the cost of adoption \u2014 and overestimate how much the technology alone will drive change.",
    },
    {
        "number": "SECTION 5",
        "title": "Success Criteria",
        "desc": "Check each statement that is true about how you will measure outcomes.",
        "items": [
            "A specific metric that should improve if this implementation works has been identified.",
            "A current baseline measurement for that metric exists.",
            "A target and timeframe have been set \u2014 for example, \u201creduce processing time by 30% within 90 days.\u201d",
            "There is a way to isolate whether the AI implementation caused the improvement, separate from other changes.",
            "What a failed or underperforming implementation looks like has been defined \u2014 not just what success looks like.",
            "A formal checkpoint exists in the plan \u2014 before full rollout \u2014 to evaluate results and decide whether to continue, adjust, or stop.",
        ],
        "callout_label": "Why this matters:",
        "callout": "Without defined success criteria, there is no way to evaluate whether the implementation worked. Unchecked items here also make it nearly impossible to secure continued internal investment.",
    },
]


# ─── JavaScript for auto-scoring ───────────────────────────────────

SCORE_JS = """
function calculateScores() {
    var total = 0;
    for (var sec = 1; sec <= 5; sec++) {
        var sectionScore = 0;
        for (var item = 1; item <= 6; item++) {
            var f = this.getField("cb_" + sec + "_" + item);
            if (f && f.value !== "Off") sectionScore++;
        }
        var sf = this.getField("score_" + sec);
        if (sf) sf.value = sectionScore + " / 6";
        total += sectionScore;
    }
    var tf = this.getField("score_total");
    if (tf) tf.value = total + " / 30";

    var interp = this.getField("interpretation");
    if (interp) {
        if (total >= 26)
            interp.value = "Strong readiness \\u2014 you are well-positioned to begin scoping an implementation.";
        else if (total >= 19)
            interp.value = "Moderate readiness \\u2014 address the unchecked items before engaging a partner.";
        else if (total >= 11)
            interp.value = "Significant gaps \\u2014 build your internal readiness plan before implementation.";
        else
            interp.value = "Foundation work needed \\u2014 start with process clarity and use case definition.";
    }
}

for (var s = 1; s <= 5; s++) {
    for (var i = 1; i <= 6; i++) {
        var cb = this.getField("cb_" + s + "_" + i);
        if (cb) cb.setAction("MouseUp", "calculateScores()");
    }
}
calculateScores();
"""


# ─── Page callbacks ────────────────────────────────────────────────

def on_page_cover(canvas, doc):
    pass

def on_page_content(canvas, doc):
    canvas.saveState()
    canvas.setFont("Manrope", 7.5)
    canvas.setFillColor(TEXT_MUTED)
    pn = canvas.getPageNumber()
    if pn > 1:
        canvas.drawCentredString(PAGE_W / 2, MARGIN_B - 16, str(pn))
    canvas.setFont("Manrope", 6.5)
    canvas.setFillColor(BORDER_LIGHT)
    canvas.drawRightString(PAGE_W - MARGIN_R, PAGE_H - MARGIN_T + 10,
                           "endbricks.com")
    canvas.restoreState()


# ─── Build functions ───────────────────────────────────────────────

def build_cover(story):
    logo = svg2rlg(LOGO_PATH)
    if logo:
        sc = 130 / logo.width
        logo.width *= sc; logo.height *= sc; logo.scale(sc, sc)
        story.append(logo)
    story.append(Spacer(1, 30))
    story.append(AccentBar(60, 3, ACCENT_MINT))
    story.append(Spacer(1, 20))
    story.append(Paragraph("AI Implementation<br/>Readiness", s["cover_title"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "A pre-build assessment for operations and leadership teams",
        s["cover_subtitle"]))
    story.append(Spacer(1, 20))
    story.append(SectionDivider(CONTENT_W * 0.35, BORDER_LIGHT))
    story.append(Spacer(1, 20))
    story.append(Paragraph(
        "Before you commit to a timeline, a vendor, or an internal build, confirm the "
        "conditions that determine whether an AI implementation succeeds or stalls.",
        s["cover_framing"]))
    story.append(Spacer(1, 28))

    t1 = Paragraph(
        "Most AI implementations do not fail because the technology was wrong. They fail "
        "because the process underneath it was not ready, the use case was not specific "
        "enough, or the team was not aligned before the build began.", s["intro_body"])
    t2 = Paragraph(
        "This is not a buyer\u2019s guide to AI tools. It is an operational readiness "
        "assessment \u2014 the same set of conditions that experienced practitioners "
        "evaluate before implementation begins. Check the items that are true today. "
        "The unchecked items are your pre-work list.", s["intro_body"])
    intro = Table([[t1], [Spacer(1, 4)], [t2]], colWidths=[CONTENT_W - 28])
    intro.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BG_CALLOUT),
        ("ROUNDEDCORNERS", [4, 4, 4, 4]),
        ("LEFTPADDING", (0, 0), (-1, -1), 16),
        ("RIGHTPADDING", (0, 0), (-1, -1), 16),
        ("TOPPADDING", (0, 0), (0, 0), 14),
        ("BOTTOMPADDING", (-1, -1), (-1, -1), 14),
        ("TOPPADDING", (0, 1), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -2), 0),
    ]))
    story.append(intro)
    story.append(Spacer(1, 40))
    story.append(Paragraph(
        "Endbricks \u2014 AI implementation for operations teams that need it to work.",
        s["cover_brand"]))
    story.append(PageBreak())


def build_section(story, section_data, section_idx):
    elements = []
    elements.append(Paragraph(section_data["number"], s["section_number"]))
    elements.append(Paragraph(section_data["title"], s["section_title"]))
    elements.append(Paragraph(section_data["desc"], s["section_desc"]))

    for i, item_text in enumerate(section_data["items"], 1):
        cb = CheckboxItem(item_text, s["item_text"], CONTENT_W - 8,
                          section_idx, i)
        elements.append(cb)

    elements.append(Spacer(1, 6))
    elements.append(CalloutBox(
        section_data["callout_label"], section_data["callout"],
        CONTENT_W, s["callout_label"], s["callout_text"]))

    story.append(KeepTogether(elements))
    story.append(Spacer(1, 14))


def build_scoring(story):
    story.append(SectionDivider(CONTENT_W, BORDER_LIGHT))
    story.append(Spacer(1, 12))
    story.append(ScoreCard(CONTENT_W))
    story.append(Spacer(1, 10))


def build_cta(story):
    cta = CTABlock(
        "Ready to discuss your results?",
        "If you want a second opinion on where you stand \u2014 or what to address "
        "first \u2014 this is what the initial consultation is for. No pitch. No proposal. "
        "A direct conversation about whether implementation makes sense, and where to start.",
        "Book a consultation at endbricks.com",
        CONTENT_W)
    story.append(cta)


def build_footer(story):
    story.append(Spacer(1, 10))
    story.append(SectionDivider(CONTENT_W * 0.15, BORDER_LIGHT))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Endbricks \u2014 AI implementation for operations teams that need it to work."
        "&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;<b>endbricks.com</b>",
        s["footer_brand"]))


# ─── Main ──────────────────────────────────────────────────────────

def main():
    print("Building Endbricks AI Readiness Checklist PDF...")

    doc = BaseDocTemplate(
        OUTPUT_PATH, pagesize=letter,
        leftMargin=MARGIN_L, rightMargin=MARGIN_R,
        topMargin=MARGIN_T, bottomMargin=MARGIN_B,
        title="AI Implementation Readiness \u2014 Endbricks",
        author="Endbricks",
        subject="Pre-build assessment checklist for AI implementation",
        creator="Endbricks",
    )

    frame = Frame(MARGIN_L, MARGIN_B, CONTENT_W,
                  PAGE_H - MARGIN_T - MARGIN_B, id="content")
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[frame], onPage=on_page_cover),
        PageTemplate(id="content_page", frames=[frame], onPage=on_page_content),
    ])

    from reportlab.platypus.doctemplate import NextPageTemplate
    story = []
    story.append(NextPageTemplate("content_page"))
    build_cover(story)

    # Page 2: Sections 1-2
    build_section(story, SECTIONS[0], 1)
    build_section(story, SECTIONS[1], 2)
    story.append(PageBreak())

    # Page 3: Sections 3-4
    build_section(story, SECTIONS[2], 3)
    build_section(story, SECTIONS[3], 4)
    story.append(PageBreak())

    # Page 4: Section 5 + Score Card + CTA + Footer
    build_section(story, SECTIONS[4], 5)
    build_scoring(story)
    build_cta(story)

    doc.build(story)
    print("  Base PDF built.")

    # Post-process: add JavaScript for auto-scoring
    add_javascript()
    print(f"  JavaScript injected.")
    print(f"PDF ready: {OUTPUT_PATH}")


def add_javascript():
    """Inject document-level JavaScript for score calculation."""
    from pypdf import PdfReader, PdfWriter

    reader = PdfReader(OUTPUT_PATH)
    writer = PdfWriter()
    writer.clone_document_from_reader(reader)
    writer.add_js(SCORE_JS)

    with open(OUTPUT_PATH, "wb") as f:
        writer.write(f)


if __name__ == "__main__":
    main()
