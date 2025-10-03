---
layout: default
title: Home
permalink: /
---

<!-- Hero Section -->
<div class="hero">

  <img src="{{ '/assets/images/hero-banner.jpg' | relative_url }}" alt="Easy Vegan Recipes">

  <div class="hero-text">
    <h1>Delicious Vegan Recipes</h1>
    <p>Simple, vibrant, plant-based meals for every occasion.</p>
    <a href="{{ '/recipes/' | relative_url }}" class="hero-btn">Browse Recipes</a>
  </div>
</div>

---

## Featured Recipes

<div class="featured-recipes">
  {% assign featured = site.recipes | slice: 0,3 %}
  {% for recipe in featured %}
    <div class="featured-card">
      <a href="{{ recipe.url | relative_url }}">
        <img src="{{ recipe.image | relative_url }}" alt="{{ recipe.title }}">
        <h3>{{ recipe.title }}</h3>
      </a>
    </div>
  {% endfor %}
</div>

---

## Explore by Category

<div class="category-grid">
  <a href="/recipes/#Breakfast" class="category-card">Breakfast</a>
  <a href="/recipes/#Entrees" class="category-card">Entrees</a>
  <a href="/recipes/#Desserts" class="category-card">Desserts</a>
  <a href="/recipes/#Burgers" class="category-card">Burgers</a>
  <a href="/recipes/#Sauces" class="category-card">Sauces</a>
</div>

---

<div class="cta-banner">
  <h2>Cookbook Coming Soon!</h2>
  <p>Get the best of Vegan & Cheese in one beautifully designed book.</p>
  <a href="/buy/" class="cta-btn">Learn More</a>
</div>
