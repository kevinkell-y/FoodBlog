from pathlib import Path
import re

CATEGORIES = [
    ("Vegan Breakfast", "vegan-breakfast"),
    ("Vegan Burgers", "vegan-burgers"),
    ("Vegan Dinners", "vegan-dinners"),
    ("Vegan Entrees", "vegan-entrees"),
    ("Vegan Holidays", "vegan-holidays"),
    ("Vegan Casseroles", "vegan-casseroles"),
    ("Vegan Dessert", "vegan-dessert"),
]

root = Path(".")

# 1. Data file
data_dir = root / "_data"
data_dir.mkdir(exist_ok=True)

(data_dir / "categories.yml").write_text(
    "\n".join([f'- name: "{name}"\n  slug: "{slug}"' for name, slug in CATEGORIES]) + "\n",
    encoding="utf-8"
)

# 2. Category layout
layouts_dir = root / "_layouts"
(layouts_dir / "category.html").write_text("""---
layout: default
---

<section class="category-page">
  <h1>{{ page.title }}</h1>

  {% assign filtered_recipes = site.recipes | where_exp: "recipe", "recipe.categories contains page.category" %}

  {% if filtered_recipes.size > 0 %}
    <div class="recipe-grid">
      {% for recipe in filtered_recipes %}
        <a class="recipe-card" href="{{ recipe.url | relative_url }}">
          {% if recipe.image %}
            <img src="{{ recipe.image | relative_url }}" alt="{{ recipe.title }}">
          {% endif %}
          <h3>{{ recipe.title }}</h3>
        </a>
      {% endfor %}
    </div>
  {% else %}
    <p class="empty-category">No recipes in this category yet.</p>
  {% endif %}
</section>
""", encoding="utf-8")

# 3. Category pages
cat_dir = root / "_pages" / "categories"
cat_dir.mkdir(parents=True, exist_ok=True)

for name, slug in CATEGORIES:
    (cat_dir / f"{slug}.md").write_text(f"""---
layout: category
title: {name}
permalink: /categories/{slug}/
category: {name}
---
""", encoding="utf-8")

# 4. Navbar dropdown
default_path = root / "_layouts" / "default.html"
default_html = default_path.read_text(encoding="utf-8")

new_nav = """<nav>
  <a href="{{ '/' | relative_url }}">Home</a>
  <a href="{{ '/about/' | relative_url }}">About</a>

  <div class="nav-dropdown">
    <a class="nav-dropdown-trigger" href="{{ '/recipes/' | relative_url }}">Recipes</a>
    <div class="nav-dropdown-menu">
      {% for category in site.data.categories %}
        <a href="{{ '/categories/' | append: category.slug | append: '/' | relative_url }}">{{ category.name }}</a>
      {% endfor %}
    </div>
  </div>

  <a href="{{ '/search/' | relative_url }}">Search</a>
  <a href="{{ '/contact/' | relative_url }}">Contact</a>
</nav>"""

if re.search(r"<nav[\s\S]*?</nav>", default_html):
    default_html = re.sub(r"<nav[\s\S]*?</nav>", new_nav, default_html, count=1)
else:
    default_html = default_html.replace("{{ content }}", new_nav + "\n\n{{ content }}")

default_path.write_text(default_html, encoding="utf-8")

# 5. Homepage category buttons
home_path = root / "_pages" / "home.md"
home = home_path.read_text(encoding="utf-8")

category_grid = """<div class="category-grid">
  {% for category in site.data.categories %}
    <a class="category-card" href="{{ '/categories/' | append: category.slug | append: '/' | relative_url }}">
      {{ category.name }}
    </a>
  {% endfor %}
</div>"""

if "## Explore by Category" in home:
    home = re.sub(
        r"(## Explore by Category\s*\n)([\s\S]*?)(\n---)",
        r"\1\n" + category_grid + r"\3",
        home,
        count=1
    )
else:
    home += "\n\n---\n\n## Explore by Category\n\n" + category_grid + "\n"

home_path.write_text(home, encoding="utf-8")

# 6. CSS
css_path = root / "assets" / "css" / "style.css"
css = css_path.read_text(encoding="utf-8")

css_add = """
/* =====================================
   CATEGORY PAGES + RECIPE NAV DROPDOWN
===================================== */

.nav-dropdown {
  position: relative;
  display: inline-flex;
  align-items: center;
}

.nav-dropdown-trigger::after {
  content: " ▾";
  font-size: 0.8em;
}

.nav-dropdown-menu {
  position: absolute;
  top: 100%;
  left: 50%;
  z-index: 100;
  min-width: 240px;
  padding: 0.6rem;
  background: white;
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-lg);
  transform: translateX(-50%);
  display: none;
}

.nav-dropdown-menu a {
  display: block;
  padding: 0.65rem 0.85rem;
  border-radius: 8px;
  color: var(--brand);
  white-space: nowrap;
  font-size: 1rem;
}

.nav-dropdown-menu a:hover {
  background: var(--brand);
  color: white;
}

.nav-dropdown:hover .nav-dropdown-menu,
.nav-dropdown:focus-within .nav-dropdown-menu {
  display: block;
}

.category-page {
  max-width: var(--content-width);
  margin: 0 auto;
  padding: 2rem 1rem 4rem;
}

.category-page h1 {
  text-align: center;
  font-family: 'Playfair Display', serif;
  font-size: 2.5rem;
  color: var(--brand);
  margin-bottom: 2rem;
}

.empty-category {
  text-align: center;
  font-family: 'Karma', Georgia, serif;
  color: var(--muted);
  font-size: 1.2rem;
}

@media (max-width: 768px) {
  .nav-dropdown {
    display: block;
    text-align: center;
  }

  .nav-dropdown-menu {
    position: static;
    transform: none;
    margin-top: 0.5rem;
    box-shadow: none;
  }
}
"""

if "CATEGORY PAGES + RECIPE NAV DROPDOWN" not in css:
    css += "\n\n" + css_add

css_path.write_text(css, encoding="utf-8")

# 7. Auto-assign categories to existing recipes
def infer_categories(filename):
    s = filename.lower()
    cats = []

    dessert_words = ["cake", "pie", "cookie", "cookies", "cheesecake", "cobbler", "muffin", "muffins", "snickerdoodle", "tres-leches", "banana-bread", "cream-pie"]
    breakfast_words = ["breakfast", "scramble", "biscuit", "biscuits", "muffin", "muffins"]
    burger_words = ["burger", "cheeseburger", "hot-dog", "hot-dogs", "reuben"]
    casserole_words = ["casserole", "ziti", "shepherd", "stuffing"]
    holiday_words = ["holiday", "stuffing", "green-bean", "sweet-potato", "pumpkin", "mashed-potatoes"]
    dinner_words = ["pasta", "ziti", "mac", "chili", "enchilada", "burrito", "taco", "nacho", "gnocchi", "meatloaf", "pot-pie", "alfredo", "lentil", "sausage", "jackfruit", "falafel", "spring-roll", "stuffed", "queso"]

    if any(w in s for w in breakfast_words):
        cats.append("Vegan Breakfast")
    if any(w in s for w in burger_words):
        cats.append("Vegan Burgers")
    if any(w in s for w in dinner_words):
        cats.append("Vegan Dinners")
    if any(w in s for w in casserole_words):
        cats.append("Vegan Casseroles")
    if any(w in s for w in holiday_words):
        cats.append("Vegan Holidays")
    if any(w in s for w in dessert_words):
        cats.append("Vegan Dessert")

    # Entrees is broad; apply to savory/main dishes but not pure desserts/sauces.
    sauce_or_basic = ["sauce", "ricotta", "flax-egg", "pie-crust", "pesto", "tahini", "tzaziki", "tzatziki"]
    if any(c in cats for c in ["Vegan Dinners", "Vegan Burgers", "Vegan Casseroles"]) and not any(w in s for w in sauce_or_basic):
        cats.append("Vegan Entrees")

    if not cats:
        cats.append("Vegan Dinners")

    return list(dict.fromkeys(cats))

recipes_dir = root / "_recipes"

for recipe_path in recipes_dir.glob("*.md"):
    text = recipe_path.read_text(encoding="utf-8")

    if not text.startswith("---"):
        continue

    parts = text.split("---", 2)
    if len(parts) < 3:
        continue

    front = parts[1].strip("\n")
    body = parts[2].lstrip("\n")

    cats = infer_categories(recipe_path.stem)
    cats_yaml = "categories:\n" + "\n".join([f"  - {cat}" for cat in cats])

    if re.search(r"(?ms)^categories:\s*\n(?:\s+- .*\n?)*", front):
        front = re.sub(r"(?ms)^categories:\s*\n(?:\s+- .*\n?)*", cats_yaml + "\n", front)
    else:
        front += "\n" + cats_yaml

    recipe_path.write_text("---\n" + front.strip() + "\n---\n\n" + body, encoding="utf-8")

print("Category injection complete.")
