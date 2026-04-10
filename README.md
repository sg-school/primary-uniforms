# Singapore Primary School Uniforms

A visual collection of uniforms from primary schools across Singapore.

## Current Status (Updated: 2026-04-10)

- Schools in dataset: **182**
- School locations re-verified: **180 / 182**
- Uniform images referenced by dataset: **182**
- Missing image references: **0** (all dataset image paths resolve to local files)

## About This Project

This project showcases the various school uniforms worn by primary school students across Singapore. The collection includes images and basic information about schools, with data loaded from `schools.json`.

## Features

- Visual gallery of school uniforms
- Search and sorting (by index / name)
- Pagination for faster browsing
- Links to school websites
- Original image attribution
- Data status summary on the homepage

## View the Collection

You can browse the collection by visiting [sg-school.github.io/primary-uniforms](https://sg-school.github.io/primary-uniforms)

## Validate Dataset Locally

Run a quick integrity check:

```bash
python -c "import json,os;d=json.load(open('schools.json',encoding='utf-8'));m=[s['uniformImage'] for s in d if not os.path.exists(s['uniformImage'])];print(f'schools={len(d)}, missing_images={len(m)}')"
```

## Contributions

If you notice any errors or would like to contribute updated school uniform images or information, please contact us at best.yichao@gmail.com.

## Credits

All images are linked to their original sources.
