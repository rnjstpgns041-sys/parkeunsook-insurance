# Daily guide batch (runs every morning, 08:00 KST)

Goal: add 40 new guide pages a day — 30 call-intent pages (people in a situation who need help now) and 10 GEO pages (questions people ask AI assistants) — deploy them, and let IndexNow send them to Naver.

1. `git pull origin main`. Regenerate the title list:
   `python3 -c "import json,glob;open('_build/rules/existing-titles.txt','w').write('\n'.join(a['slug']+' | '+a['title'] for p in sorted(glob.glob('_build/articles/part*.json')) for a in json.load(open(p)))+'\n')"`
2. Pick 30 call-intent topics and 10 GEO topics that are not already covered (grep the title list for each keyword; give a different angle when close). New slugs must be unique.
3. In `_build/build.py`: append each slug to the matching category line of `ORDER` (index = position in `CATS`), raise the `assert ... == N` count by 40, and add the new part numbers to `PART_DATES` with today's date.
4. Recreate the schema sample: `python3 -c "import json;json.dump(json.load(open('_build/articles/part77.json'))[0],open('_build/sample-article.json','w'),ensure_ascii=False,indent=1)"`
5. Start 8 writer agents (tell each to keep its scripts under a unique name, e.g. gen<part>.py, since agents share one scratchpad) in parallel, 5 articles each, writing `_build/articles/partNNN.json` (next free numbers). Call-intent agents read `_build/rules/article-rules.md` + `_build/rules/call-intent-rules.md`; GEO agents read `_build/rules/article-rules.md` + `_build/rules/geo-rules.md`. Commit and push each file as it arrives.
6. `rm -f _build/sample-article.json && python3 _build/build.py` — must print the new total. Run the link / JSON-LD check (no broken `href`/`src`, every ld+json parses).
7. Write the new URLs (in part order) to `/mnt/project-files/new-guide-urls-<date>.txt` and all sitemap URLs to `/mnt/project-files/index-urls.txt`.
8. Commit, push to main. Netlify deploys; `netlify/functions/deploy-succeeded.mjs` submits the new sitemap URLs to Naver IndexNow automatically.
9. Add a tab for the day to the Naver checklist artifact (source copy kept at /mnt/project-files/naver-checklist/naver-checklist.html with its test ck2.cjs: run `NODE_PATH=$(npm root -g) node ck2.cjs naver-checklist.html` there; copy the edited file back after publishing; https://claude.ai/artifact/FmBT3Zo1xEmtdyahFgcnk5; DATA rows are [url,title]; bump the "전체 N개" count and the default tab), test it, republish.
10. Reply in the thread in Korean: the new total, a few topic highlights, the checklist tab, and that content is not expert-reviewed.
