#!/usr/bin/env python3
"""Build fully static ECE-1201 study site from the two provided transcripts."""
from pathlib import Path
import re, html
import mistune
ROOT=Path(__file__).parent
prep=(ROOT/'content/preparation-original.txt').read_text(encoding='utf-8')
sol=(ROOT/'content/full-solutions-original.txt').read_text(encoding='utf-8')

prep=re.sub(r'(## 2\. Full Marks Preparation Strategy)(.*?)(?=\n# Step 01)', r'\1\n\n%%ROADMAP%%\n', prep, flags=re.S)
prep=prep.replace('Basic positive-sequence three-phase phasor diagram (abc)', '%%PHASORABC%%')
prep=re.sub(r'(# Step 07 — তোমার 20-Mark Mock CT)(.*?)(?=\n## এখন কী করবে\?)', r'\1\n\n%%MOCK%%\n', prep, flags=re.S)
sol=sol.replace('Positive (abc)\n\nNegative (acb)', '%%DUALDIAGRAM%%')
sol=re.sub(r'(## Last-Minute Revision Checklist)(.*?)(?=\n## পরীক্ষায় যেসব Formula)', r'\1\n\nপরীক্ষার আগে এগুলো না দেখে লিখতে পারা দরকার।\n\n%%CHECKLIST%%\n', sol, flags=re.S)
sol=sol.replace('&#x20;Show Answer for Self-Checking', '%%PRACTICEANSWER%%')
sol=sol.replace('Show Answer for Self-Checking', '%%PRACTICEANSWER%%')

roadmap='''<div class="roadmap" aria-label="Preparation roadmap">
<div class="roadmap-item"><span class="number">01</span><div><b>Basics + Definitions</b><small>সহজ theory, fundamentals, important terms</small></div></div>
<div class="roadmap-item"><span class="number">02</span><div><b>Phase Sequence + Phasor</b><small>abc/acb, angles, sinusoidal equations, diagram</small></div></div>
<div class="roadmap-item"><span class="number">03</span><div><b>Balanced Y-Y Derivations</b><small>√3 voltage relation, 30° shift, current relation</small></div></div>
<div class="roadmap-item"><span class="number">04</span><div><b>Numerical + Neutral Wire</b><small>PYQ solution, power calculation, neutral current proof</small></div></div>
<div class="roadmap-item"><span class="number">05</span><div><b>20-Mark Mock CT</b><small>২০ মিনিটে solve, তারপর answer checking</small></div></div>
</div>'''

def svg_phasor(positive=True, width_class=''):
    # Rightward a reference, other two separated by ±120°; labels switched for acb.
    top='c' if positive else 'b'
    bottom='b' if positive else 'c'
    return f'''<svg class="phasor-svg {width_class}" role="img" aria-label="{'abc positive' if positive else 'acb negative'} three phase phasor diagram" viewBox="0 0 300 260" xmlns="http://www.w3.org/2000/svg">
      <defs><marker id="arrow-{'pos' if positive else 'neg'}" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0L7 3.5L0 7Z" fill="#159a93"/></marker></defs>
      <path d="M25 128H275 M150 14V240" stroke="currentColor" stroke-opacity=".14" stroke-width="1.2"/>
      <path d="M150 128L264 128" stroke="#15a39a" stroke-width="3" stroke-linecap="round"/>
      <path d="M150 128L93 29" stroke="#4f7bd5" stroke-width="3" stroke-linecap="round"/>
      <path d="M150 128L93 227" stroke="#ec924b" stroke-width="3" stroke-linecap="round"/>
      <path d="M264 128l-10 -5v10z" fill="#15a39a"/><path d="M93 29l2 11 9-5z" fill="#4f7bd5"/><path d="M93 227l10-6-9-5z" fill="#ec924b"/>
      <circle cx="150" cy="128" r="4" fill="currentColor"/>
      <text x="184" y="113" class="phase-label">a : 0°</text>
      <text x="21" y="18" class="phase-label">{top} : +120°</text>
      <text x="21" y="250" class="phase-label">{bottom} : −120°</text>
    </svg>'''

one_diagram=f'<div class="figure-card"><div class="figure-intro">Positive phase sequence (abc / RYB)</div>{svg_phasor(True)}<p class="figure-caption">Three voltages of equal magnitude, separated by 120°.</p></div>'
dual_diagram=f'''<div class="diagram-grid"><div class="figure-card"><div class="figure-intro">Positive (abc)</div>{svg_phasor(True)}<p class="figure-caption">b = −120°, c = +120°</p></div><div class="figure-card"><div class="figure-intro">Negative (acb)</div>{svg_phasor(False)}<p class="figure-caption">b = +120°, c = −120°</p></div></div>'''

mock_questions=[
('Question 1',4,'Define a balanced three-phase system. State two advantages of a three-phase system.','Definition + two advantages'),
('Question 2',4,'Define phase sequence. Write the phasor expressions for both positive and negative sequence when the phase voltage is 100 V.','abc and acb expressions'),
('Question 3',4,'Derive the relation between line voltage and phase voltage for a balanced Y-Y system of positive sequence.','Use KVL and vector addition'),
('Question 4',6,'A balanced Y-Y system has phase voltage 200 V and load impedance 10∠30° Ω per phase. Calculate all three phase currents, line currents and total real power. Assume abc sequence.','Full numerical with angles'),
('Question 5',2,'What is the neutral current in an ideal balanced Y-Y system? Explain briefly.','Show current summation')]
mock='''<div class="exam-card" id="mock-exam"><div class="exam-card-head"><div><div class="eyebrow">PRACTICE TEST 01</div><h3>20-Mark Mock CT</h3><p>ECE-1201 · Y-Y syllabus · 20 minutes</p></div><div class="score-tile"><strong>20</strong><span>MARKS</span></div></div>
<div class="timer-bar"><span id="timer-display" role="timer" aria-live="off">20:00</span><div class="timer-buttons"><button class="btn btn-primary" id="start-timer" type="button">Start timer</button><button class="btn btn-subtle" id="reset-timer" type="button">Reset</button></div></div>
<div class="exam-questions">'''
for t,m,q,h in mock_questions:
    mock+=f'<div class="exam-question"><div class="exam-question-top"><strong>{t}</strong><span>{m} marks</span></div><p>{html.escape(q)}</p><small>{html.escape(h)}</small></div>'
mock+='''</div><a class="btn btn-secondary" href="#solutions" data-route="solutions">See detailed solutions</a></div>'''

checklist_items=[
'Balanced three-phase system-এর definition ও advantages',
'Positive ও negative sequence-এর phasor expressions',
'Line voltage-এর √3 relation এবং 30° lead derivation',
'Phase currents ও line currents-এর numerical',
'Three-phase real power calculation',
'Balanced Y-Y system-এ neutral current = 0-এর explanation'
]
checklist='''<div class="checklist-card"><div class="checklist-header"><b>Revision progress</b><span id="progress-count">0 of 6</span></div><div class="progress-track"><div id="progress-fill" class="progress-fill"></div></div><div class="checklist-items">'''
for i,item in enumerate(checklist_items):
    checklist+=f'<label class="checklist-row"><input type="checkbox" class="study-check" data-check="{i}"><span>{html.escape(item)}</span></label>'
checklist+='</div></div>'

practice='''<details class="answer-reveal"><summary>Show Answer for Self-Checking <span aria-hidden="true">⌄</span></summary>
<div class="reveal-inner"><p><strong>All three phase voltages</strong></p>
<div class="math display">\\[ V_{an}=120\\angle0^\\circ\\;V,\\quad V_{bn}=120\\angle-120^\\circ\\;V,\\quad V_{cn}=120\\angle120^\\circ\\;V \\]</div>
<p><strong>All three phase currents</strong></p>
<div class="math display">\\[ I_a=8\\angle-45^\\circ\\;A,\\quad I_b=8\\angle-165^\\circ\\;A,\\quad I_c=8\\angle75^\\circ\\;A \\]</div>
<p><strong>Line current</strong></p><div class="math display">\\[I_L=I_P=8\\;A\\]</div>
<p><strong>Total real power</strong></p><div class="math display">\\[P=3(120)(8)\\cos45^\\circ=2036.47\\;W\\approx\\boxed{2.04\\;kW}\\]</div>
</div></details>'''

shortcodes={'ROADMAP':roadmap,'PHASORABC':one_diagram,'DUALDIAGRAM':dual_diagram,'MOCK':mock,'CHECKLIST':checklist,'PRACTICEANSWER':practice}
markdown=mistune.create_markdown(escape=False,plugins=['table','strikethrough'])

def render_doc(md):
    md=md.replace('\\\\[',r'\[').replace('\\\\]',r'\]').replace('\\\\(',r'\(').replace('\\\\)',r'\)')
    md=md.replace(r'\_', '_').replace(r'\.', '.').replace('&#x20;',' ')
    # A few exported inline file citations contain only a filename; link the local sources.
    md=md.replace('L-01_ECE-1201.pdf', '[L-01_ECE-1201.pdf](sources/L-01_ECE-1201.pdf)')
    md=md.replace('L-02_ECE-1201.pdf', '[L-02_ECE-1201.pdf](sources/L-02_ECE-1201.pdf)')
    expressions=[]
    def protect_block(m):
        idx=len(expressions)
        expressions.append(('block',m.group(1).strip()))
        return '\n\n' + f'ZZZMATHBLOCK{idx}ZZZ' + '\n\n'
    def protect_inline(m):
        idx=len(expressions)
        expressions.append(('inline',m.group(1).strip()))
        return f'ZZZMATHINLINE{idx}ZZZ'
    md=re.sub(r'\\\[(.*?)\\\]',protect_block,md, flags=re.S)
    md=re.sub(r'\\\((.*?)\\\)',protect_inline,md, flags=re.S)
    page=markdown(md)
    for idx,(kind,tex) in enumerate(expressions):
        if kind=='block':
            page=page.replace(f'<p>ZZZMATHBLOCK{idx}ZZZ</p>',f'<div class="math display">\\[{html.escape(tex)}\\]</div>')
            page=page.replace(f'ZZZMATHBLOCK{idx}ZZZ',f'<div class="math display">\\[{html.escape(tex)}\\]</div>')
        else:
            page=page.replace(f'ZZZMATHINLINE{idx}ZZZ',f'<span class="math inline">\\({html.escape(tex)}\\)</span>')
    for name,value in shortcodes.items():
        page=page.replace(f'<p>%%{name}%%</p>',value).replace(f'%%{name}%%',value)
    return page

prep_html=render_doc(prep)
sol_html=render_doc(sol)
head='''<!DOCTYPE html>
<html lang="bn">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<meta name="theme-color" content="#0d203a" />
<meta name="description" content="ECE-1201 Circuits & Systems-II: complete Bengali study notes, detailed 20-mark mock CT solutions, balanced Y-Y connections, phasor diagrams, and practice problems." />
<title>ECE-1201 | CT-01 Full Marks Study Hub</title>
<link rel="icon" type="image/svg+xml" href="assets/favicon.svg" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Hind+Siliguri:wght@400;500;600;700&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="assets/styles.css" />
<script>window.MathJax={tex:{inlineMath:[["\\\\(","\\\\)"]],displayMath:[["\\\\[","\\\\]"]]},svg:{fontCache:'global'},options:{skipHtmlTags:['script','noscript','style','textarea','pre','code']}};</script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
<script defer src="assets/app.js"></script>
</head>
<body>
<a class="skip-link" href="#main-content">Skip to content</a>
<div class="top-progress"><div id="reading-progress"></div></div>
<header class="site-header"><div class="header-inner">
<a class="brand" href="#preparation" data-route="preparation"><span class="brand-symbol">∿</span><span class="brand-title">ECE <b>1201</b><small>STUDY HUB</small></span></a>
<nav class="header-nav" aria-label="Main navigation"><a class="tab-link active" href="#preparation" data-route="preparation">Preparation</a><a class="tab-link" href="#solutions" data-route="solutions">Solutions</a><a class="tab-link" href="#resources" data-route="resources">Resources</a></nav>
<div class="header-actions"><button class="icon-btn" id="theme-toggle" title="Toggle light or dark mode" aria-label="Toggle theme">◐</button><button class="icon-btn" id="print-page" title="Print study notes" aria-label="Print study notes">⎙</button></div>
</div></header>
<main id="main-content">
<section class="hero"><div class="hero-inner"><div class="hero-copy"><div class="hero-kicker"><span class="kicker-dot"></span> RUET · ECE · 1st Year Even Semester</div><h1>Circuits & Systems <span>II</span></h1><p>From <strong>Zero to 20/20</strong> — বাংলা ব্যাখ্যা, exam-ready answers, step-by-step numericals, phasor diagrams, and a timed mock test.</p><div class="hero-chips"><span>⚡ Three-phase systems</span><span>◎ Y-Y Connection</span><span>✎ 20 Marks CT</span></div><div class="hero-buttons"><a href="#preparation" data-route="preparation" class="btn btn-primary">Start learning <span>→</span></a><a href="#solutions" data-route="solutions" class="btn btn-ghost">View solved mock CT</a></div></div><div class="hero-visual"><span class="orbit orbit1"></span><span class="orbit orbit2"></span><span class="orbit orbit3"></span><div class="hero-graph"><span class="sigma">∑</span><span class="hero-equation">V<sub>L</sub> = √3 V<sub>P</sub></span><div class="hero-graph-bottom">Y–Y CONNECTION <strong>20/20</strong></div></div></div></div></section>
<div class="page-grid"><aside class="sidebar"><div class="sidebar-inner"><div class="side-label">CURRENT LESSON</div><div class="side-course">ECE-1201 <span>CT-01</span></div><div class="sidebar-separator"></div><div class="side-label">ON THIS PAGE</div><nav id="table-of-contents" class="toc" aria-label="Contents"></nav><div class="side-tip"><span>✦ EXAM TIP</span><p>Understand the formula, draw the phasor, show the steps, then box the answer.</p></div></div></aside>
<div class="content-column">
<section id="view-preparation" class="view-section active" data-view="preparation"><div class="article-header"><div class="section-kicker">STUDY GUIDE · LECTURE 01 + 02</div><h2>Complete Preparation Notes</h2><p>একদম zero থেকে balanced Y-Y connection পর্যন্ত প্রতিটি গুরুত্বপূর্ণ topic।</p></div><article class="article" id="article-preparation">'''
mid='''</article><div class="next-panel"><p>READY FOR THE NEXT STEP?</p><h3>Now solve the 20-mark CT.</h3><a href="#solutions" data-route="solutions" class="btn btn-primary">Open detailed solutions →</a></div></section>
<section id="view-solutions" class="view-section" data-view="solutions"><div class="article-header"><div class="section-kicker">EXAM PRACTICE · 5 FULL SOLUTIONS</div><h2>Detailed 20-Mark Solutions</h2><p>Exam-ready English answers + সহজ বাংলা explanation + step-by-step calculation.</p></div><article class="article" id="article-solutions">'''
end='''</article><div class="next-panel"><p>REVISE & RETEST</p><h3>Practice it without looking at the answers.</h3><a href="#preparation" data-route="preparation" class="btn btn-primary">Back to preparation →</a></div></section>
<section id="view-resources" class="view-section" data-view="resources"><div class="article-header"><div class="section-kicker">DOWNLOADS · ORIGINAL COURSE FILES</div><h2>Class Resources</h2><p>তোমার আপলোড করা lecture slides এবং previous question paper, একটি জায়গায়।</p></div>
<div class="resource-grid"><a class="resource-card" href="sources/L-01_ECE-1201.pdf" target="_blank" rel="noopener"><span class="resource-icon">PDF</span><strong>Lecture 01 — ECE-1201</strong><small>Polyphase, three-phase systems, phase sequence</small><span class="resource-action">Open / Download ↗</span></a><a class="resource-card" href="sources/L-02_ECE-1201.pdf" target="_blank" rel="noopener"><span class="resource-icon">PDF</span><strong>Lecture 02 — ECE-1201</strong><small>Balanced Y-Y connection, phasor summation, neutral wire</small><span class="resource-action">Open / Download ↗</span></a><a class="resource-card" href="sources/image(20261110-201356).png" target="_blank" rel="noopener"><span class="resource-icon">PYQ</span><strong>Previous CT-01 Question</strong><small>Original uploaded question image</small><span class="resource-action">View original ↗</span></a><a class="resource-card" href="content/preparation-original.txt" download><span class="resource-icon">TXT</span><strong>Full Preparation Transcript</strong><small>Complete original text as supplied</small><span class="resource-action">Download text ↗</span></a><a class="resource-card" href="content/full-solutions-original.txt" download><span class="resource-icon">TXT</span><strong>Detailed Solutions Transcript</strong><small>Complete original solved answers</small><span class="resource-action">Download text ↗</span></a></div>
<div class="resource-preview"><h3>Previous Question Paper</h3><img src="sources/image(20261110-201356).png" alt="Uploaded CT-01 ECE-1201 question paper" loading="lazy"/><p>Note: PYQ-তে Delta অংশ আছে। এখানে প্রস্তুতি Y-Y পর্যন্ত সীমাবদ্ধ রাখা হয়েছে, আপনার শিক্ষিকার নির্দেশ অনুযায়ী।</p></div>
</section>
<footer class="footer"><span>ECE-1201 · CT-01 Study Hub</span><span>Made for study and exam practice · No backend needed</span></footer>
</div></div></main>
</body></html>'''
(ROOT/'index.html').write_text(head+prep_html+mid+sol_html+end, encoding='utf-8')
print('Generated index.html:',(ROOT/'index.html').stat().st_size,'bytes')
print('Math expressions:', sum(1 for x in re.findall(r'class="math', prep_html+sol_html)))
print('View headlines:',len(re.findall(r'<h[123]',prep_html)),len(re.findall(r'<h[123]',sol_html)))
