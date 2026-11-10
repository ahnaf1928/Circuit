# ECE-1201 CT-01 — Full Marks Study Hub

A responsive, static GitHub Pages website based on the **L-01, L-02 and previous-question materials** supplied for ECE-1201 (Circuits & Systems-II). Preparation is limited to **Y-Y connections**. It contains Bangla explanations, detailed exam-ready English solutions, math expressions, balanced three-phase phasor illustrations, a 20-mark timed mock test, a persistent revision checklist, and links to the source PDFs and previous-question image.

## Website features

- Preparation notes and full detailed solutions presented as separate tabs.
- Phasor diagrams drawn directly with SVG.
- Mathematics displayed with **MathJax** (loaded via CDN; internet connection required for typeset formulas).
- A real 20-minute timer (starts only when you click Start timer).
- Revision checklist saved in your browser (localStorage, no account or server).
- Responsive layout, light/dark theme, and print-friendly styles.
- Uploaded PDF lecture slides and PYQ image under `sources/`.

## File structure

```text
ECE-1201-CT01-GitHub-Website/
├── index.html
├── README.md
├── build_site.py             # Optional: regenerate index.html from text transcripts
├── .nojekyll
├── assets/
│   ├── app.js
│   ├── styles.css
│   └── favicon.svg
├── content/
│   ├── preparation-original.txt
│   └── full-solutions-original.txt
└── sources/
    ├── L-01_ECE-1201.pdf
    ├── L-02_ECE-1201.pdf
    └── image(20261110-201356).png
```

## Upload with Git in VS Code terminal or Git Bash

1. Create an **empty public repository** on GitHub, such as `ece-1201-ct01` (don't pre-add a README, license, or gitignore).
2. Download and unzip the project, then open the **extracted folder** in VS Code.
3. Open Terminal and run the commands below. Replace `YOUR_USERNAME` with your GitHub username.

```bash
git init
git add .
git commit -m "Add ECE-1201 CT-01 study website"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/ece-1201-ct01.git
git push -u origin main
```

If Git asks you to identify yourself, run:

```bash
git config --global user.name "Your Name"
git config --global user.email "your-github-email@example.com"
```

Then repeat `git commit -m "Add ECE-1201 CT-01 study website"` and `git push -u origin main`.

**Authentication:** GitHub will require an authorized login (usually a browser sign-in via Git Credential Manager, or a personal access token). A normal GitHub password cannot be used for HTTPS Git authentication.

## Enable GitHub Pages

1. Open the new GitHub repository.
2. Go to **Settings → Pages**.
3. Under **Build and deployment**, select **Deploy from a branch**.
4. Select **main** and **/(root)**, then **Save**.
5. Your URL will be `https://YOUR_USERNAME.github.io/ece-1201-ct01/` once GitHub finishes publishing.

GitHub Pages serves this static site directly; there is **no npm install** and no Node build step.

## Preview locally

The simplest approach is opening `index.html` in your browser. If you prefer an HTTP server:

```bash
python -m http.server 8000
```

Open `http://localhost:8000`.

## Updating content

To change study text, edit the two `.txt` files under `content/`, then run:

```bash
python build_site.py
```

This re-generates `index.html` using Python and the `mistune` Python library. Only the optional regeneration step requires `mistune` (`python -m pip install mistune`). The published site itself does **not** require Python.

After editing/publishing:

```bash
git add .
git commit -m "Update study notes"
git push
```

## Notes and scope

- The site is a faithful visual web adaptation of the two conversation transcripts, rather than a pixel-for-pixel copy of the ChatGPT interface. Source transcript files remain included for textual fidelity.
- Delta connection material from the old PYQ is shown in the original question image only, but not taught in the notes or solutions due to the stated exam scope.
- Total real-power formulas are standard circuit-theory supplements used to solve the provided PYQ; the uploaded lecture slides do not show their full derivation.
- **Privacy:** Public GitHub repositories and GitHub Pages publicly expose all PDFs, images, and transcripts in this project. Remove any file you do not want to publish before pushing.
