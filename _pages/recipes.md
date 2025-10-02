---
layout: default
title: Recipes
permalink: /recipes/
---

<h1>All Recipes</h1>

<div class="filters">
  <button data-filter="all">All</button>
  <button data-filter="breakfast">Breakfast</button>
  <button data-filter="entrees">Entrees</button>
  <button data-filter="dessert">Desserts</button>
  <button data-filter="burgers">Burgers</button>
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

