# ☕ Oatly Drinks Lab

Internal recipe management tool for **Last Mile × Oatly** — Barcelona & Madrid.

## Features

- 📚 **Database** — all Oatly drink recipes, filterable by category, source, product
- 🤖 **AI Generator** — create new recipes from available syrups/ingredients (powered by Claude)
- 🛒 **Shopping List** — select recipes + portions → consolidated ingredient list
- 📄 **Ficha Técnica** — print-ready recipe cards for café presentations

## Setup

1. Push this repo to GitHub
2. Enable GitHub Pages (Settings → Pages → Deploy from `main` branch, root `/`)
3. Access via `https://<your-username>.github.io/<repo-name>/`
4. Password: set in `index.html` line with `const PASSWORD = 'oatly2026'`

## Adding recipes

- **Via AI Generator**: generate → approve → auto-saved to database
- **Manually**: add entries directly to `recipes.json` following the existing schema

## Recipe schema

```json
{
  "id": "UNIQUE_ID",
  "name": "Recipe Name",
  "source": "Look Book Vol.3 | Flavoured Barista | Event Drinks 2026 | AI Generated | Creative Development",
  "category": "Latte | Matcha | Cold Brew | Refresher | ...",
  "oatly_product": "Oatly Barista Edition",
  "serve": "Iced | Hot | Frozen",
  "skill_level": "2/5",
  "status": "approved",
  "tags": ["tag1", "tag2"],
  "ingredients": [
    {"name": "Ingredient", "amount": 200, "unit": "ml"}
  ],
  "method": "Step by step method.",
  "notes": "Optional notes."
}
```
