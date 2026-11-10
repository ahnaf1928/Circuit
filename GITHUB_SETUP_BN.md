# GitHub-এ পুরো website push করার বাংলা গাইড

এই project-এ `index.html`, `assets`, `sources` ও `content`—সব ফাইল রেডি আছে। তোমাকে কোড আলাদা করে লিখতে হবে না।

## ১) নতুন GitHub repository বানাও

1. [github.com/new](https://github.com/new) ওপেন করে GitHub-এ sign in করো।
2. Repository name: `ece-1201-ct01` (ইচ্ছা করলে অন্য নাম দিতে পারো)।
3. **Public** নির্বাচন করো (GitHub Pages ব্যবহার করতে চাইলে public রাখা সহজ)।
4. `Add a README`, `.gitignore` বা `license`—কোনোটিই আগে থেকে টিক দেবে না।
5. **Create repository** চাপো।

## ২) ZIP extract করে VS Code-এ ওপেন করো

1. Download করা ZIP-এ right click → **Extract All**।
2. Extracted `ECE-1201-CT01-GitHub-Website` ফোল্ডারটি VS Code-এ **File → Open Folder** দিয়ে ওপেন করো।
3. VS Code মেনু থেকে **Terminal → New Terminal**।
4. Git ইনস্টল আছে কিনা দেখতে `git --version` চালাও। না থাকলে [git-scm.com](https://git-scm.com/) থেকে Git install করো।

## ৩) একসাথে এই commands দাও

`YOUR_USERNAME`-এর জায়গায় নিজের GitHub username লিখবে। `ece-1201-ct01` নাম আলাদা দিলে সেটাও বদলাবে।

```bash
git init
git add .
git commit -m "ECE-1201 CT-01 full study website"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/ece-1201-ct01.git
git push -u origin main
```

GitHub login চাইলে sign in করতে হবে। HTTPS authentication-এর জন্য সাধারণ GitHub password নয়—browser login / Git Credential Manager অথবা personal access token ব্যবহার হয়।

**`Author identity unknown` দেখালে:**

```bash
git config --global user.name "Your GitHub Name"
git config --global user.email "your-email@example.com"
git add .
git commit -m "ECE-1201 CT-01 full study website"
git branch -M main
git push -u origin main
```

**`remote origin already exists` দেখালে:**

```bash
git remote set-url origin https://github.com/YOUR_USERNAME/ece-1201-ct01.git
git push -u origin main
```

## ৪) GitHub Pages দিয়ে live website করো

1. Repository → **Settings** → **Pages**।
2. Build and deployment → Source: **Deploy from a branch**।
3. Branch: **main**। Folder: **/(root)**।
4. **Save** চাপো। GitHub publish করলে তোমার website URL হবে:

`https://YOUR_USERNAME.github.io/ece-1201-ct01/`

## ৫) ভবিষ্যতে update push করা

যেকোনো কোড/কন্টেন্ট পরিবর্তন করে terminal-এ:

```bash
git add .
git commit -m "Update ECE study website"
git push
```

## গুরুত্বপূর্ণ কথা

- পুরো site GitHub Pages-এ direct চলবে। `npm install`, Node বা database লাগবে না।
- MathJax দিয়ে সুন্দর formulas দেখানোর জন্য browser-এ internet থাকতে হবে।
- Public repo হলে uploaded question image এবং PDFs-ও public হয়ে যাবে। কোনো private material publish করতে না চাইলে push করার **আগে** সংশ্লিষ্ট ফাইল মুছে দিও।
