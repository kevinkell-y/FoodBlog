---
layout: default
title: Recipes
permalink: /recipes/
---

<h1>Recipes</h1>

<div class="filters">
  <a class="filter-btn" href="{{ '/recipes/' | relative_url }}">All</a>
  <a class="filter-btn" href="{{ '/categories/vegan-breakfast/' | relative_url }}">Breakfast</a>
  <a class="filter-btn" href="{{ '/categories/vegan-entrees/' | relative_url }}">Entrees</a>
  <a class="filter-btn" href="{{ '/categories/vegan-dessert/' | relative_url }}">Desserts</a>
  <a class="filter-btn" href="{{ '/categories/vegan-burgers/' | relative_url }}">Burgers</a>
</div>

<div class="recipe-grid">
  {% for recipe in site.recipes %}
    <div class="recipe-card" data-category="{{ recipe.category }}">
      <a href="{{ recipe.url | relative_url }}">
        <img src="{{ recipe.image | relative_url }}" alt="{{ recipe.title }}">
        <h3>{{ recipe.title }}</h3>
      </a>
    </div>
  {% endfor %}
</div>

