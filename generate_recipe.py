import os, json, re, datetime
import anthropic

payload = json.loads(os.environ['PAYLOAD'])
mode        = payload.get('mode', 'single')
product     = payload.get('product', 'Oatly Barista Edition')
style       = payload.get('style', 'Iced Latte')
ingredients = payload.get('ingredients', '')
vibe        = payload.get('vibe', '')
notes       = payload.get('notes', '')
tags_list   = payload.get('tags', [])
count       = payload.get('count', 6)
focus       = payload.get('focus', 'mix of styles')
base        = payload.get('base', 'any base')

with open('recipes.json') as f:
    db = json.load(f)

existing_names = ', '.join(r['name'] for r in db['recipes'])
client = anthropic.Anthropic(api_key=os.environ['ANTHROPIC_API_KEY'])

if mode == 'single':
    prompt = f"""You are a specialty coffee drink developer working with Oatly plant-based milks for cafes in Barcelona and Madrid.

Create a creative, original, professional drink recipe. Be specific with quantities and techniques.

PARAMETERS:
- Oatly product: {product}
- Drink style: {style}
- Available syrups / key ingredients: {ingredients or 'classic cafe pantry'}
- Vibe / season: {vibe or 'everyday cafe'}
- Extra notes: {notes or 'none'}

EXISTING RECIPES (avoid duplicating): {existing_names}

Respond ONLY with a JSON object, no markdown, no explanation:
{{
  "name": "Recipe Name",
  "category": "Latte|Matcha|Cold Brew|Refresher|Mocha|Chocolate|Tea Latte|Frozen|Signature Latte",
  "serve": "Iced|Hot|Frozen",
  "skill_level": "1/5|2/5|3/5|4/5|5/5",
  "tags": ["tag1", "tag2", "tag3"],
  "ingredients": [
    {{"name": "ingredient name", "amount": 200, "unit": "ml|g|shots|pinch|handful|drops|tsp"}}
  ],
  "method": "Step by step method in 2-4 sentences.",
  "tasting_notes": "Flavor arc and sensory description for the cafe team."
}}"""

    msg = client.messages.create(
        model='claude-sonnet-4-6',
        max_tokens=1000,
        messages=[{'role': 'user', 'content': prompt}]
    )
    text = re.sub(r'```json|```', '', msg.content[0].text).strip()
    data = json.loads(text)

    new_recipe = {
        'id': 'AI' + datetime.datetime.now().strftime('%Y%m%d%H%M%S'),
        'name': data['name'],
        'source': 'AI Generated',
        'category': data.get('category', 'Latte'),
        'oatly_product': product,
        'serve': data.get('serve', 'Iced'),
        'skill_level': data.get('skill_level', '2/5'),
        'status': 'approved',
        'tags': data.get('tags', []),
        'ingredients': data.get('ingredients', []),
        'method': data.get('method', ''),
        'notes': data.get('tasting_notes', '')
    }
    db['recipes'].append(new_recipe)
    print(f"Generated: {new_recipe['name']}")

elif mode == 'batch':
    prompt = f"""You are a creative specialty coffee drink developer for Oatly, working with cafes in Barcelona and Madrid.

Available syrups / ingredients: {', '.join(tags_list)}
Oatly base: {product}
Coffee / tea base constraint: {base}
Drink focus: {focus}
Number of concepts to generate: {count}

Existing recipes to avoid duplicating: {existing_names}

Generate {count} creative drink concepts. Each should use 2-4 of the available ingredients.

Respond ONLY with a JSON array, no markdown:
[
  {{
    "name": "Creative Drink Name",
    "combination": ["Syrup 1", "Syrup 2"],
    "oatly_product": "specific Oatly Barista product",
    "style": "Iced Latte|Matcha|Cold Brew|Refresher|Signature|Mocha|Tea Latte|Frozen",
    "serve": "Iced|Hot|Frozen",
    "description": "2-sentence evocative description of flavor profile and why this works.",
    "concept_tags": ["tag1", "tag2", "tag3"],
    "complexity": "Easy|Medium|Advanced"
  }}
]"""

    msg = client.messages.create(
        model='claude-sonnet-4-6',
        max_tokens=2000,
        messages=[{'role': 'user', 'content': prompt}]
    )
    text = re.sub(r'```json|```', '', msg.content[0].text).strip()
    ideas = json.loads(text)

    for i, idea in enumerate(ideas):
        r = {
            'id': 'BATCH' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + str(i),
            'name': idea['name'],
            'source': 'Batch Ideas',
            'category': idea.get('style', 'Latte'),
            'oatly_product': idea.get('oatly_product', product),
            'serve': idea.get('serve', 'Iced'),
            'skill_level': '',
            'status': 'concept',
            'tags': idea.get('concept_tags', []),
            'ingredients': [],
            'method': idea.get('description', ''),
            'notes': f"Key combo: {', '.join(idea.get('combination', []))} | Complexity: {idea.get('complexity','')}"
        }
        db['recipes'].append(r)
        print(f"Concept: {r['name']}")

db['last_updated'] = datetime.datetime.now().strftime('%Y-%m-%d')

with open('recipes.json', 'w') as f:
    json.dump(db, f, indent=2, ensure_ascii=False)

print("Done.")
