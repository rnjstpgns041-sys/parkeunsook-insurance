Rules for guide articles on 박은숙 보험상담 (insurance consultant site, Korean, general readers).

First read /home/claude/parkeunsook-insurance/_build/sample-article.json for the exact schema, tone and length. Keys: slug, title, description, lead, sections (exactly 4 items, each {"h": heading, "p": [2 paragraphs]}), checklist (5 short strings), faq (2 items {"q","a"}). Skim _build/rules/existing-titles.txt (regenerate it first; see DAILY.md) (titles already on the site) and don't repeat their angles.

Writing:
- Polite 합니다체, calm and clear, like an experienced consultant explaining to a client. No exclamation marks, no hype, no emoji.
- Title under 30 characters, starting with the common search phrase. Description 80–100 characters. Lead 130–170 characters that answers the question directly.
- Body text (all section paragraphs combined) 900–1100 characters.
- Never name an insurer. Never give specific amounts, rates or percentages that vary by product; say it differs by product, generation (세대) and 약관, and tell readers what to check.
- Don't state rules you are unsure of as fact; hedge ("~인 경우가 많습니다", "약관에 따라 다릅니다").
- Last section may briefly say that reviewing one's own policy with a consultant (보장 분석) helps. No hard sell, no promises of payment.
- Checklist: 5 concrete things to prepare or check before a consultation.

Output: write a JSON array of the articles (UTF-8, ensure_ascii False, indent 1) to the given part file. Then validate:
python3 -c "import json,sys;a=json.load(open(sys.argv[1]));assert len(a)==5;[print(x['slug'],len(x['title']),len(x['description']),sum(len(p) for s in x['sections'] for p in s['p'])) for x in a];assert all(len(x['sections'])==4 and all(len(s['p'])==2 for s in x['sections']) and len(x['checklist'])==5 and len(x['faq'])==2 and 900<=sum(len(p) for s in x['sections'] for p in s['p'])<=1100 and '!' not in json.dumps(x,ensure_ascii=False) for x in a)" FILE
Fix and re-run until it passes. Touch no other project file.
