---
layout: default
title: Home
permalink: /
---

<section class="hero">
  <h1>Welcome to <span class="brand">Vegan &amp; Cheese</span></h1>
  <p>Easy, delicious, vegan comfort food.</p>
  <a class="btn-primary" href="/recipes/">Browse All Recipes</a>
</section>

<section class="featured-recipes">
  <h2>Featured Recipes</h2>
  <div class="recipe-grid">
    {% assign featured = site.recipes | slice: 0,6 %}
    {% for recipe in featured %}
      <a href="{{ recipe.url | relative_url }}">
        <img src="{{ recipe.image | relative_url }}" alt="{{ recipe.title }}">
        <h3>{{ recipe.title }}</h3>
      </a>
    {% endfor %}

  </div>
</section>
