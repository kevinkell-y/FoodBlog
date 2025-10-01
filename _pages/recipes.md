---
layout: default
title: "Recipes"
permalink: /recipes/
---

## All Recipes

<div class="gallery-grid">
  {% for post in site.categories["Easy Vegan Recipes"] %}
    <a href="{{ post.url }}" class="gallery-item">
      <img src="{{ post.image }}" alt="{{ post.title }}">
      <h3>{{ post.title }}</h3>
    </a>
  {% endfor %}
</div>
