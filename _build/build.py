import json, html, glob, os, sys
# Run from anywhere: python3 _build/build.py
SP = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(SP)
BASE = 'https://parkeunsook-insurance.netlify.app'
PHONE = '010-6378-6964'
TODAY = '2026-10-13'
ORDER = """silson-generations silson-4th-switch silson-claim-docs silson-duplicate silson-dosu silson-mri-ultrasound silson-overseas silson-group-personal silson-renewal-increase silson-senior silson-mental-health silson-rejoin silson-pharmacy silson-hospital-level silson-exclusions silson-hospital-stay silson-korean-medicine silson-dental silson-dermatology silson-pregnancy silson-infertility silson-emergency silson-physical-therapy silson-eye-disease silson-injection silson-child silson-cancer-patient silson-claim-rejected silson-after-surgery silson-family-check silson-with-disease silson-cancel-regret silson-nonpay-rejected silson-doc-missing silson-claim-small-amounts silson-premium-after-claims silson-elderly-parents
brain-coverage-range heart-coverage-range cancer-amount similar-cancer cancer-exemption-period anticancer-drug-rider cancer-recurrence disability-rider hospital-daily fracture-rider cancer-treatment-rider ci-insurance heart-procedure-rider cancer-nursing-hospital injury-vs-disease cataract-surgery stroke-rehab carcinoma-in-situ kidney-dialysis herniated-disc rare-disease-rider burn-rider colon-polyp prostate-cancer aortic-disease arrhythmia diabetes-complications liver-disease appendicitis ligament-injury thyroid-cancer lung-disease uterine-fibroid cerebral-aneurysm heart-failure parkinson-disease hearing-loss icu-rider spinal-stenosis shoulder-surgery gallstone-surgery hemorrhoid-surgery varicose-veins sleep-apnea kidney-stone cancer-amount-check brain-heart-check surgery-amount-check coverage-shortage-signs rider-expiry-check cancer-suspected-check biopsy-waiting-check brain-mri-abnormal heart-test-abnormal checkup-abnormal-result
renewal-vs-nonrenewal payment-period-maturity no-surrender-value premium-waiver main-vs-rider refund-type policy-loan lapse-revival paid-up-extended premium-factors policy-certificate surrender-value level-vs-increasing interest-rate-terms group-insurance-work premium-payment-tips universal-insurance life-vs-nonlife depositor-protection annuity-conversion insurance-payout-tax insured-vs-holder renewal-max-age coverage-start-date deductible-terms exclusion-clauses contract-conversion dividend-policy premium-discount maturity-payout coverage-period-choice
when-remodeling before-cancel replacement-contract reduce-premium coverage-analysis-how insurance-budget coverage-gap-priority family-history-coverage yearly-checkup-list too-many-policies keep-old-policy coverage-amount-guide direct-vs-agent analysis-documents old-cancer-policy rider-add-remove costly-riders after-diagnosis-review family-policy-review reduce-coverage-order remodel-mistakes overlap-check compare-proposals renewal-premium-shock ci-policy-review savings-policy-review job-change-gap after-birth-review premium-too-high insurance-consult-prep parents-policy-check acquaintance-policy-check second-opinion policy-check-40s policy-check-before-retire monthly-premium-review policy-duplicate-cancel insurance-too-little
fetal-insurance-timing child-insurance-maturity parents-simple-insurance newlywed-insurance single-household first-job-insurance forties-checkup fifties-checkup sixties-insurance thirties-checkup breadwinner-coverage child-turns-adult pregnancy-planning freelancer-insurance twenties-insurance dual-income-couple divorce-insurance study-abroad-insurance newborn-conversion teen-insurance single-parent grandchild-insurance military-child remarried-family parents-claim-help family-caregiving early-retirement foreign-resident-insurance disabled-family child-school-accident seventies-insurance retiree-couple child-allergy-asthma adopted-child parents-hospitalized child-hospitalized spouse-diagnosed parents-dementia-signs newborn-nicu parents-cancer-diagnosed child-surgery-scheduled husband-hospitalized wife-pregnancy-hospital grandparent-fall-injury
self-employed driver-insurance driver-legal-cost daily-liability fire-insurance-business dental-insurance caregiver-daily dementia-insurance whole-vs-term surgery-rider pet-insurance travel-insurance annuity-vs-pension-savings variable-insurance women-coverage home-fire-insurance pm-bicycle-insurance savings-insurance choose-cancer-insurance nursing-hospital-cost funeral-vs-insurance business-liability golf-insurance smartphone-insurance cyber-insurance jeonse-guarantee health-vs-cancer-only inheritance-life-insurance senior-cancer-insurance accident-insurance leisure-insurance high-risk-job whole-life-cancel motorcycle-insurance long-term-care-insurance income-protection single-premium-insurance lifelong-health-insurance cancer-insurance-late kids-insurance-compare nonrenewal-switch-consult senior-premium-burden regular-before-simple cancer-insurance-compare-points brain-heart-insurance-join dementia-insurance-compare caregiver-insurance-join child-insurance-review
claim-time-limit claim-documents claim-denied hidden-claims designated-claimant claim-adjuster claim-multiple-policies car-accident-claims claim-after-death claim-digital small-claims claim-dispute claim-for-child medical-bill-detail surgery-certificate discharge-documents partial-payment medical-advisory overseas-claim-docs claim-records-habit claim-delay diagnosis-code-check hospital-transfer-claim dormant-insurance-money accident-report-writing claim-power-of-attorney cancer-diagnosed-claim stroke-diagnosed-claim heart-attack-claim surgery-scheduled-check hospitalized-now fall-injury-claim dementia-diagnosed-claim disability-claim-how dental-implant-claim fracture-claim-how claim-amount-question chemo-claim-check radiation-claim-check rehab-hospital-claim nursing-hospital-claim claim-docs-hospital-refused claim-after-surgery-days claim-for-deceased-parent traffic-injury-own-policy work-injury-own-policy
duty-to-disclose disclosure-violation simple-underwriting-355 withdrawal-right quality-guarantee-cancel read-policy-terms beneficiary-designation insurance-tax-credit chronic-disease-insurance policyholder-change illegal-contract-cancel health-checkup-disclosure insurance-age agent-registration-check phone-sales-contract renewal-notice review-before-signing electronic-contract contract-copy-request agent-left address-update premium-autopay-change coverage-reduction-request find-my-policies insurance-complaint-steps minor-contract diabetes-join hypertension-join cancer-survivor-join surgery-history-join depression-history-join thyroid-history-join hepatitis-join elderly-join-80 disc-history-join stent-history-join cancel-notice-received lapse-notice-received policy-agent-change old-policy-claim claim-without-agent asthma-history-join kidney-disease-join liver-history-join arrhythmia-history-join stroke-history-join obesity-join smoker-join medication-many-join after-hospital-join pregnant-complication-join withdraw-within-15days contract-cancel-mistake beneficiary-check-now policy-loan-repay-plan premium-pause-options""".split('\n')
CATS = ['실손의료비', '진단비 · 특약', '보험 구조 이해', '리모델링 · 보장 분석', '가족 · 연령별 보험', '상품별 가이드', '보험금 청구', '가입 · 계약 제도']
cat_of = {}; order = []
for c, line in zip(CATS, ORDER):
    for s in line.split(): cat_of[s] = c; order.append(s)
assert len(order) == len(set(order)) == 355

arts = {}
# Articles in later data files were published later.
PART_DATES = {11: '2026-10-14', 12: '2026-10-14', 13: '2026-10-14', 14: '2026-10-14',
              15: '2026-10-15', 16: '2026-10-15', 17: '2026-10-15', 18: '2026-10-15', 19: '2026-10-15', 20: '2026-10-15',
              21: '2026-10-16', 22: '2026-10-16', 23: '2026-10-16', 24: '2026-10-16', 25: '2026-10-16', 26: '2026-10-16',
              **{n: '2026-10-20' for n in range(27, 37)}, **{n: '2026-10-21' for n in range(37, 47)}, **{n: '2026-10-22' for n in range(47, 57)}, **{n: '2026-10-25' for n in range(57, 67)}}
for f in sorted(glob.glob(SP + '/articles/part*.json'), key=lambda f: int(f.rsplit('part',1)[1].split('.')[0])):
    part = int(f.rsplit('part', 1)[1].split('.')[0])
    for a in json.load(open(f, encoding='utf-8')):
        a['date'] = PART_DATES.get(part, TODAY)
        arts[a['slug']] = a
missing = [s for s in order if s not in arts]
extra = [s for s in arts if s not in cat_of]
if missing or extra: print('MISSING', missing, 'EXTRA', extra); sys.exit(1)

e = html.escape
def head(title, desc, url, extra=''):
    return f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&family=Noto+Serif+KR:wght@600&display=swap">
<link rel="stylesheet" href="guide.css">
<script src="/assets/track.js" defer></script>
{extra}</head>
<body>
<header class="top"><div class="wrap">
  <a class="brand" href="../"><b>박은숙</b><span>보험 보장 분석 상담</span></a>
  <nav class="nav" aria-label="주요 메뉴"><a href="../">홈</a><a href="./">보험 가이드</a><a href="../#contact">상담 신청</a><a class="tel" href="tel:01063786964">{PHONE}</a></nav>
</div></header>
'''
FOOT = f'''<footer><div class="wrap">
  <p><strong>박은숙</strong> 보험설계사 · 상담 문의 {PHONE}</p>
  <p>이 글은 일반적인 정보 제공을 위한 것으로, 실제 보장 내용과 지급 조건은 가입하신 상품의 약관과 증권에 따릅니다. 보험계약 체결 전 상품설명서 및 약관을 반드시 읽어 보시기 바랍니다. 기존 계약 해지 후 신계약 체결 시 보험인수 거절, 보험료 인상, 보장내용 변경 등 불이익이 발생할 수 있습니다.</p>
  <p class="credit">제작 <a href="https://webstudio-4e9.pages.dev/" target="_blank" rel="noopener">웹 스튜디오</a></p>
</div></footer>
<div class="mbar"><a class="btn plain" href="tel:01063786964">전화 상담</a><a class="btn solid" href="../#contact">무료 상담 신청</a></div>
</body>
</html>
'''
def cta():
    return f'''<aside class="cta">
  <p class="cta-label">무료 보장 분석</p>
  <h2>내 보험도 이 기준으로 확인해 보세요</h2>
  <p>가입하신 보험을 약관 기준으로 정리해 부족한 보장과 중복된 보장을 알려 드립니다. 상담은 무료이며 가입을 권유하지 않습니다.</p>
  <div class="cta-row"><a class="btn amber" href="tel:01063786964">전화 상담 {PHONE}</a><a class="btn ghost" href="../#contact">상담 신청하기</a></div>
</aside>'''

os.makedirs(OUT + '/guide', exist_ok=True)
for i, s in enumerate(order):
    a = arts[s]; c = cat_of[s]; url = f'{BASE}/guide/{s}.html'
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "headline": a['title'], "description": a['description'], "datePublished": a['date'], "dateModified": a['date'],
         "author": {"@type": "Person", "name": "박은숙"}, "mainEntityOfPage": url, "inLanguage": "ko"},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q['q'], "acceptedAnswer": {"@type": "Answer", "text": q['a']}} for q in a['faq']]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "홈", "item": BASE + '/'},
            {"@type": "ListItem", "position": 2, "name": "보험 가이드", "item": BASE + '/guide/'},
            {"@type": "ListItem", "position": 3, "name": a['title'], "item": url}]}]}
    extra = '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False).replace('</', '<\\/') + '</script>\n'
    body = [head(f"{a['title']} | 박은숙 보험상담", a['description'], url, extra)]
    body.append(f'<main class="wrap article">\n<nav class="crumbs" aria-label="현재 위치"><a href="../">홈</a> › <a href="./">보험 가이드</a> › <span>{e(c)}</span></nav>')
    body.append(f'<p class="cat">{e(c)}</p>\n<h1>{e(a["title"])}</h1>\n<p class="byline">글 · 보험설계사 박은숙</p>\n<p class="lead">{e(a["lead"])}</p>')
    body.append('<nav class="toc" aria-label="목차"><p>목차</p><ol>' + ''.join(f'<li><a href="#s{j+1}">{e(sec["h"])}</a></li>' for j, sec in enumerate(a['sections'])) + '</ol></nav>')
    for j, sec in enumerate(a['sections']):
        body.append(f'<section id="s{j+1}"><h2>{e(sec["h"])}</h2>' + ''.join(f'<p>{e(p)}</p>' for p in sec['p']) + '</section>')
    body.append('<div class="checklist"><h2>상담 전 확인해 두면 좋은 것</h2><ul>' + ''.join(f'<li>{e(x)}</li>' for x in a['checklist']) + '</ul></div>')
    body.append('<section class="faq"><h2>자주 묻는 질문</h2>' + ''.join(f'<details><summary>{e(q["q"])}</summary><p>{e(q["a"])}</p></details>' for q in a['faq']) + '</section>')
    body.append(cta())
    rel = [x for x in order if cat_of[x] == c and x != s][:4]
    if len(rel) < 4: rel += [x for x in order if x != s and x not in rel][i:i + 4 - len(rel)] or [x for x in order if x != s and x not in rel][:4 - len(rel)]
    body.append('<section class="related"><h2>함께 읽으면 좋은 글</h2><ul>' + ''.join(f'<li><a href="{x}.html"><span>{e(cat_of[x])}</span>{e(arts[x]["title"])}</a></li>' for x in rel) + '</ul></section>')
    body.append('</main>')
    body.append(FOOT)
    open(f'{OUT}/guide/{s}.html', 'w', encoding='utf-8').write('\n'.join(body))

# guide index
idx = [head(f'보험 가이드 {len(order)} | 박은숙 보험상담', '실손보험, 진단비, 갱신형과 비갱신형, 보험 리모델링, 보험금 청구까지. 보험설계사 박은숙이 약관 기준으로 정리한 보험 가이드 ' + str(len(order)) + '편입니다.', BASE + '/guide/')]
idx.append('<main><section class="gi-hero"><div class="wrap"><p class="cat">보험 가이드</p><h1>보험, 알고 가입하면 다릅니다</h1><p class="lead">상담 현장에서 가장 많이 받는 질문을 약관 기준으로 정리했습니다. 주제별로 골라 읽어 보세요.</p>')
idx.append('<nav class="cat-nav" aria-label="주제">' + ''.join(f'<a href="#c{k+1}">{e(c)}</a>' for k, c in enumerate(CATS)) + '</nav></div></section><div class="wrap">')
for k, c in enumerate(CATS):
    items = [x for x in order if cat_of[x] == c]
    idx.append(f'<section class="gi-cat" id="c{k+1}"><h2>{e(c)} <small>{len(items)}편</small></h2><ul class="gi-list">' + ''.join(f'<li><a href="{x}.html"><b>{e(arts[x]["title"])}</b><span>{e(arts[x]["description"])}</span></a></li>' for x in items) + '</ul></section>')
idx.append(cta().replace('<aside class="cta">', '<aside class="cta" style="margin-bottom:72px">'))
idx.append('</div></main>')
idx.append(FOOT)
open(f'{OUT}/guide/index.html', 'w', encoding='utf-8').write('\n'.join(idx))

# sitemap
LATEST = max(arts[x]['date'] for x in order)
urls = [(BASE + '/', '1.0', LATEST), (BASE + '/guide/', '0.8', LATEST)] + [(f'{BASE}/guide/{s}.html', '0.6', arts[s]['date']) for s in order]
sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
sm += [f'  <url><loc>{u}</loc><lastmod>{d}</lastmod><priority>{p}</priority></url>' for u, p, d in urls]
sm.append('</urlset>')
open(f'{OUT}/sitemap.xml', 'w', encoding='utf-8').write('\n'.join(sm) + '\n')

# homepage guide count
import re
hp = open(OUT + '/index.html', encoding='utf-8').read()
hp = re.sub(r'자주 받는 질문 \d+가지를', f'자주 받는 질문 {len(order)}가지를', hp)
hp = re.sub(r'보험 가이드 \d+편 전체 보기', f'보험 가이드 {len(order)}편 전체 보기', hp)
open(OUT + '/index.html', 'w', encoding='utf-8').write(hp)

# page titles for the stats page
os.makedirs(OUT + '/stats', exist_ok=True)
json.dump({f'/guide/{x}.html': arts[x]['title'] for x in order}, open(OUT + '/stats/titles.json', 'w', encoding='utf-8'), ensure_ascii=False)

# featured list for homepage
feat = ['silson-generations', 'brain-coverage-range', 'renewal-vs-nonrenewal', 'before-cancel', 'claim-time-limit', 'duty-to-disclose']
json.dump([{'slug': x, 'title': arts[x]['title'], 'cat': cat_of[x]} for x in feat], open(SP + '/featured.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('built', len(order), 'articles; sitemap urls', len(urls))
