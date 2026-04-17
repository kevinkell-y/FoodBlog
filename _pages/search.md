---
layout: default
title: Search
permalink: /search/
---

<section class="search-page">
  <h1 class="search-page-title">Search</h1>

  <div class="search-box-wrap">
    <input
      id="search-input"
      class="search-input-large"
      type="search"
      placeholder="Search recipes..."
      autocomplete="off"
    />
  </div>

  <div id="search-results" class="recipe-grid search-results-grid"></div>
</section>

<script>
let data = [];

fetch('/search.json')
  .then(res => res.json())
  .then(json => {
    data = json;
  });

function escapeHtml(str) {
  return String(str || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function renderResults(matches, query) {
  const results = document.getElementById('search-results');

  if (!query.trim()) {
    results.innerHTML = '';
    return;
  }

  if (!matches.length) {
    results.innerHTML = '<p class="search-no-results">No recipes found.</p>';
    return;
  }

  results.innerHTML = matches.map(item => `
    <a class="recipe-card search-card" href="${item.url}">
      <div class="recipe-card-image-wrap">
        <img class="recipe-card-image" src="${item.image}" alt="${escapeHtml(item.title)}">
      </div>
      <div class="recipe-card-title">${escapeHtml(item.title)}</div>
    </a>
  `).join('');
}

document.getElementById('search-input').addEventListener('input', function(e) {
  const q = e.target.value.toLowerCase().trim();

  const matches = data.filter(item =>
    item.title.toLowerCase().includes(q) ||
    item.content.toLowerCase().includes(q)
  );

  renderResults(matches, q);
});
</script>
