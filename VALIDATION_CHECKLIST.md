# Validation Checklist

Run this checklist every time a new synopsis version is generated, before pushing to GitHub. It was created after V7 was found to have a data-count inconsistency between GitHub screenshots and the synopsis's own tables.

## 1. Data reconciliation (why counts can drift)

The raw TRI files, the Form R + manufacturing-NAICS filter, and duplicate consolidation each produce a different row count. Any screenshot, notebook output, or GitHub figure must state **which stage** it reflects, and at least one figure must reconcile all stages against the synopsis tables.

- [ ] Re-run the filter pipeline (`src/data_prep.py` logic: Form R filter → primary NAICS starts with 31/32/33 → consolidate duplicate facility-chemical-year records) on the current raw files for every reporting year.
- [ ] Compare the resulting counts to Table 3 (preliminary data-preparation counts) and Table 4 (consecutive-year matching counts) in the synopsis. They must match exactly. If they don't, the synopsis narrative or the pipeline code is wrong — find out which before publishing.
- [ ] Confirm the sample-size totals quoted in prose (e.g., "123,688 eligible development records," "40,002 eligible holdout records") equal the sums of the relevant Table 4 columns.
- [ ] Any raw, unfiltered file shape (`df.shape` straight off disk) that is reported anywhere must be labeled as raw, and a separate reconciliation table (Table D1 in Appendix D — not a screenshot or image) must walk raw → filtered → consolidated so a reviewer can see the two views are consistent, not contradictory.
- [ ] Reporting year 2024 (the 2023→2024 transition) is the held-out test set. Any new table or figure that includes 2024 alongside development years must flag it (color, label, or note) so it's not mistaken for a development-year record.

## 2. APA 7 / Walsh template compliance

Check the actual document properties, not just visual appearance — LibreOffice/Word can visually approximate settings that aren't actually correct in the file.

- [ ] Margins: 1 inch on all sides (`section.top/bottom/left/right_margin == 914400` EMU).
- [ ] Body font: an APA-approved font (11 pt Calibri, 11 pt Arial, 12 pt Times New Roman, 12 pt Aptos, or 11 pt Georgia are pre-approved).
- [ ] Line spacing: double-spaced throughout, including references and block quotes (`paragraph_format.line_spacing == 2.0`), with **no** extra space before/after paragraphs.
- [ ] First-line paragraph indent: 0.5 in (`first_line_indent == 457200` EMU) on body paragraphs; left-aligned, ragged right margin (no justification).
- [ ] Page numbers: top right corner, on every page including the title page; no running head (student paper).
- [ ] Heading levels follow APA format and are internally consistent with the rest of the document:
  - Level 1 — centered, bold, title case
  - Level 2 — flush left, bold, title case
  - Level 3 — flush left, bold italic, title case
- [ ] Title page includes: title (bold), "Synopsis" label, student name, "Walsh College," course number/name, instructor name, term, and date — matching the QM 640 Synopsis template layout exactly.
- [ ] Title is repeated as a Level 1 heading at the top of the first page of text.
- [ ] References: alphabetical order, hanging indent (0.5 in), double-spaced, consistent APA 7 citation format with DOIs/URLs where available. At least 10 relevant papers (mandatory per assignment instructions).
- [ ] Tables and figures: numbered sequentially, labeled with the bold-number-line + italic-title-line convention already used throughout this document (e.g., "Table 3" / *Preliminary Data-Preparation Counts*), called out in the text before they appear.
- [ ] Appendices are referenced in the main text (per Walsh formatting requirement) and excluded from the main page-count check.
- [ ] Page count of the main text (excluding title page, appendices, tables, figures) is 10-15 pages per the synopsis template instructions.

## 3. Walsh synopsis template structure

Cross-check section order and required content against `QM 640 Synopsis template.pdf`:

- [ ] Background and Context → Problem Statement → Purpose of the Study → Scope and Objectives → Main Research Question → Research Questions and Hypotheses (≥4 RQs) → Sample Size Calculation → Data Description (incl. GitHub link, data dictionary, folder-tree structure, data-count reconciliation) → Analytic Approach → Recommendation and Application → References.
- [ ] GitHub repository is public, linked in the Data Description section, and contains complete data (or download instructions + sample) and code.
- [ ] Folder tree structure is shown in the report whenever the repo has multiple folders.

## 4. GitHub sync

- [ ] Old docx versions are deleted from `reports/` when a new version is pushed (only the current version should remain).
- [ ] Superseded images are deleted from `images/` when replaced.
- [ ] `README.md` and `data/README.md` version references are updated to point at the new docx filename.
- [ ] Verify each GitHub commit actually landed (navigate to the file/folder and confirm) — upload/delete clicks can silently fail to commit if the button is clicked before the page finishes staging the file.

## 5. Professor feedback / terminology and appendix discipline (added after the RQ3 category → action-type revision)

- [ ] No embedded images anywhere in the synopsis (title page logo excepted, if any). Any prior screenshot/figure must be represented as a native Word table built from the same underlying numbers, not a picture.
- [ ] Appendices contain only material genuinely needed to support the main text; remove sections that duplicate main-text tables or that reviewers flag as unnecessary (e.g., a standalone execution-timeline appendix was removed per instructor feedback).
- [ ] The Q1–Q4 summary table(s) name the actual statistical/predictive method in plain language first (e.g., "Chi-square test," "Logistic regression") before any technical detail — not just formula references.
- [ ] If RQ3 terminology changes (e.g., "category" → "action type"), search the *entire* document, including table cells (not just body paragraphs), and update every RQ3-related instance while leaving unrelated generic statistical terms (e.g., "missing category" in a diagnostics table) untouched.
- [ ] After removing any appendix or section, search the rest of the document for cross-references to it (by appendix letter and by name) and update or delete them — a removed appendix must not still be cited elsewhere as containing content that no longer exists.
- [ ] Re-check for stray empty paragraphs (0 runs, no page break) immediately before headings — these can reappear after further manual edits to the document.
