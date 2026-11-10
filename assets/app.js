/* ECE-1201 CT Study Hub: vanilla JavaScript, no build tool or backend. */
(() => {
  'use strict';
  const views = [...document.querySelectorAll('.view-section')];
  const navigation = [...document.querySelectorAll('[data-route]')];
  const toc = document.getElementById('table-of-contents');
  const storagePrefix = 'ece1201-ct01-';
  let currentView = 'preparation';
  let headingLinks = [];

  const getSaved = (key, fallback) => {
    try { return JSON.parse(localStorage.getItem(storagePrefix + key)) ?? fallback; }
    catch (_) { return fallback; }
  };
  const save = (key, value) => {
    try { localStorage.setItem(storagePrefix + key, JSON.stringify(value)); }
    catch (_) { /* Works without storage, too. */ }
  };

  function assignHeadingIds() {
    ['preparation', 'solutions'].forEach(view => {
      document.querySelectorAll(`#article-${view} h1, #article-${view} h2, #article-${view} h3`).forEach((heading, i) => {
        heading.id = `${view}-topic-${i + 1}`;
      });
    });
  }

  function rebuildToc() {
    toc.replaceChildren();
    if (currentView === 'resources') {
      const link = document.createElement('a');
      link.className = 'toc-link active';
      link.textContent = 'Original files & downloads';
      link.href = '#resources';
      toc.append(link);
      headingLinks = [];
      return;
    }
    const headings = [...document.querySelectorAll(`#article-${currentView} h1, #article-${currentView} h2`)];
    headingLinks = headings.map(h => {
      const a = document.createElement('a');
      a.href = `#${h.id}`;
      a.className = 'toc-link ' + (h.tagName === 'H2' ? 'toc-h3' : '');
      a.textContent = h.textContent.trim();
      a.title = a.textContent;
      toc.append(a);
      return { h, a };
    });
    updateActiveToc();
  }

  function updateActiveToc() {
    let active = null;
    for (const candidate of headingLinks) {
      if (candidate.h.getBoundingClientRect().top < 180) active = candidate;
    }
    if (!active) active = headingLinks[0];
    headingLinks.forEach(({ a }) => a.classList.toggle('active', active?.a === a));
  }

  function setActiveView(view, anchor = null, scroll = true) {
    if (!['preparation', 'solutions', 'resources'].includes(view)) view = 'preparation';
    currentView = view;
    views.forEach(section => section.classList.toggle('active', section.dataset.view === view));
    navigation.forEach(link => link.classList.toggle('active', link.dataset.route === view && link.classList.contains('tab-link')));
    rebuildToc();
    document.title = `${view === 'solutions' ? 'Detailed Solutions' : view === 'resources' ? 'Resources' : 'Preparation'} | ECE-1201 CT-01`;
    if (scroll) {
      requestAnimationFrame(() => {
        const destination = anchor ? document.getElementById(anchor) : document.querySelector('.page-grid');
        destination?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
    }
    // MathJax may not measure equations inside sections hidden on initial load.
    if (window.MathJax && typeof window.MathJax.typesetPromise === 'function') {
      window.MathJax.typesetPromise([document.getElementById(`view-${view}`)]).catch(() => {});
    }
  }

  function fromHash(scroll = true) {
    let fragment = '';
    try { fragment = decodeURIComponent(location.hash.slice(1)); }
    catch (_) { fragment = location.hash.slice(1); }
    if (['preparation', 'solutions', 'resources'].includes(fragment)) {
      setActiveView(fragment, null, scroll);
      return;
    }
    const element = fragment ? document.getElementById(fragment) : null;
    if (element) {
      const owner = element.closest('.view-section');
      setActiveView(owner?.dataset.view || 'preparation', fragment, scroll);
    } else {
      setActiveView('preparation', null, false);
    }
  }

  assignHeadingIds();
  window.addEventListener('hashchange', () => fromHash(true));
  navigation.forEach(link => link.addEventListener('click', e => {
    if (location.hash === link.getAttribute('href')) {
      e.preventDefault(); fromHash(true);
    }
  }));
  fromHash(Boolean(location.hash));

  // Theme mode (saved locally in this browser).
  const themeButton = document.getElementById('theme-toggle');
  function applyTheme(mode) {
    document.documentElement.dataset.theme = mode;
    themeButton.setAttribute('aria-label', `Switch to ${mode === 'dark' ? 'light' : 'dark'} theme`);
    save('theme', mode);
  }
  applyTheme(getSaved('theme', 'light'));
  themeButton.addEventListener('click', () => applyTheme(document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark'));
  document.getElementById('print-page').addEventListener('click', () => window.print());

  // Interactive revision checklist.
  const checks = [...document.querySelectorAll('.study-check')];
  const savedChecks = getSaved('checks', []);
  if (Array.isArray(savedChecks)) {
    checks.forEach((input, i) => { input.checked = savedChecks.includes(i); });
  }
  function updateChecklist() {
    const finished = checks.flatMap((input, i) => input.checked ? [i] : []);
    document.getElementById('progress-count').textContent = `${finished.length} of ${checks.length} completed`;
    document.getElementById('progress-fill').style.width = `${(finished.length / checks.length) * 100}%`;
    save('checks', finished);
  }
  checks.forEach(input => input.addEventListener('change', updateChecklist));
  updateChecklist();

  // Real 20-minute countdown timer; no persistent background task.
  const timerDisplay = document.getElementById('timer-display');
  const startButton = document.getElementById('start-timer');
  const resetButton = document.getElementById('reset-timer');
  let remainingSeconds = 20 * 60;
  let deadline = 0;
  let intervalId = null;
  function displayTime() {
    timerDisplay.textContent = `${String(Math.floor(remainingSeconds / 60)).padStart(2, '0')}:${String(remainingSeconds % 60).padStart(2, '0')}`;
    timerDisplay.classList.toggle('finished', remainingSeconds === 0);
  }
  function stopTimer() {
    if (intervalId !== null) clearInterval(intervalId);
    intervalId = null;
    startButton.textContent = remainingSeconds === 0 ? 'Start again' : 'Start timer';
  }
  function tick() {
    remainingSeconds = Math.max(0, Math.ceil((deadline - Date.now()) / 1000));
    displayTime();
    if (remainingSeconds === 0) {
      stopTimer();
      startButton.textContent = 'Time finished';
    }
  }
  startButton.addEventListener('click', () => {
    if (intervalId !== null) {
      tick(); stopTimer(); startButton.textContent = 'Resume timer';
    } else {
      if (remainingSeconds === 0) remainingSeconds = 20 * 60;
      deadline = Date.now() + remainingSeconds * 1000;
      intervalId = setInterval(tick, 250);
      startButton.textContent = 'Pause timer';
      displayTime();
    }
  });
  resetButton.addEventListener('click', () => {
    stopTimer(); remainingSeconds = 20 * 60; displayTime();
  });
  displayTime();

  // Page-reading progress indicator and sidebar location state.
  let scheduled = false;
  function updateReading() {
    const total = Math.max(1, document.documentElement.scrollHeight - innerHeight);
    const p = Math.max(0, Math.min(100, (scrollY / total) * 100));
    document.getElementById('reading-progress').style.width = `${p}%`;
    updateActiveToc();
    scheduled = false;
  }
  window.addEventListener('scroll', () => {
    if (!scheduled) { scheduled = true; requestAnimationFrame(updateReading); }
  }, { passive: true });
  updateReading();
})();
