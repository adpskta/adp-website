#!/usr/bin/env python3
# a.d.p 新サイト静的ジェネレータ
# 使い方: python3 build.py  →  site/ に全ページを生成
import json, os, re, shutil, html

BASE = os.path.dirname(os.path.abspath(__file__))
MIG = os.path.join(BASE, '01_migration')
SITE = os.path.join(BASE, 'site')

content = json.load(open(os.path.join(MIG, 'content.json')))

# 旧ページslug → (新slug, タイトル, カテゴリ)
PROJECTS = {
 'work__american-portraiture-gr4x2-2rjwf-hn878-ery2x-yy6t6': ('renovation-of-new-wild', '生前からある都市に住む', 'house'),
 'work__american-portraiture-gr4x2-2rjwf-hn878-ery2x-yy6t6-7xs76-h8aws-6das8': ('kitakamakura', '北鎌倉の増築', 'house'),
 'work__american-portraiture-gr4x2-2rjwf-hn878-ery2x-yy6t6-7xs76-h8aws-8r8ab': ('kuppography-takanawa', 'クッポグラフィー 高輪ゲートウェイスタジオ', 'shop'),
 'work__american-portraiture-gr4x2-2rjwf-hn878-ery2x-yy6t6-7xs76-h8aws-a46n9-smr6z-azsrb-bklp4-rh9l8-jzsnr-felet-h3mrx-bz5zg-fbnl4-6fgf9': ('bistro-endroll', 'bistro endroll', 'shop'),
 'work__american-portraiture-gr4x2-2rjwf-hn878-ery2x-yy6t6-7xs76-h8aws-a46n9': ('circle-photo-studio', 'circle photo studio', 'shop'),
 'work__american-portraiture-gr4x2-2rjwf-hn878-ery2x-yy6t6-7xs76-h8aws-zttrs': ('new-case-study-house', 'New Case Study House', 'house'),
 'work__american-portraiture-gr4x2-2rjwf-hn878-ery2x-yy6t6-7xs76-h8aws': ('sugary-imaizumi', 'Sugary 今泉', 'shop'),
 'work__american-portraiture-gr4x2-2rjwf-hn878-ery2x-yy6t6-7xs76': ('table-room', 'Table Room', 'office'),
 'work__american-portraiture-gr4x2-2rjwf-hn878-ery2x': ('patisserie-minimal', 'Patisserie Minimal', 'shop'),
 'work__american-portraiture-gr4x2-2rjwf-hn878': ('backyard-in-field', '畑のBackyard', 'landscape'),
 'work__american-portraiture-gr4x2-2rjwf': ('renovation-for-green', '緑のためのリノベーション', 'house'),
 'work__american-portraiture-gr4x2': ('nkhc-landscape', 'NKHC Landscape Design 2022~', 'landscape'),
 'work__chotto-motto-5sdaj': ('tani-house', '世田谷 谷の家', 'house'),
 'work__death-by-xoko-ea6gh-3daf4-gceab': ('kuppography-komazawa', 'クッポグラフィー 駒沢公園スタジオ', 'shop'),
 'work__death-by-xoko-ea6gh-3daf4': ('kuppography-okinawa', 'クッポグラフィー 沖縄スタジオ', 'shop'),
 'work__death-by-xoko-ea6gh-8bnb4': ('luzesombra-hq', 'LUZeSOMBRA HQ', 'shop'),
 'work__death-by-xoko-ea6gh': ('office-in-komazawa', '駒沢のオフィス', 'office'),
 'portfolio-1__project-two-ky966-fkmxk-hey92': ('rounded-dining-table', 'Rounded Dining Table', 'furniture'),
 'portfolio-1__project-two-ky966-fkmxk': ('108', '108', 'furniture'),
 # 以降は新規事例（content.jsonに無いものは NEW_TEXTS に本文を書く）
 'new__sugary-hankyu': ('sugary-hankyu', 'Sugary 阪急三番街', 'shop'),
}

# content.jsonに無い新規事例の本文（段落は空行区切り。クレジットも段落として続ける）
NEW_TEXTS = {
 'sugary-hankyu': '''阪急三番街のバスターミナルに近接し、行き交う人の流れが絶えない立地に計画した小さな店舗。通過動線の中でアサイーを気軽に手に取り、日常の一部として持ち帰ることを主としたテイクアウト中心のスタンド型店舗とした。

空間の核には、全周に耳を残した欅の無垢材による一枚板のハイテーブルを据えている。自然が生み出した不均質な輪郭や力強い表情は、スーパーフードであるアサイーが持つ自然由来のエネルギーと重なり合う存在として採用した。加工されすぎない素材そのものの形や表情で、食の背景にある自然の力が伝わることを期待している。

テーブルの周囲に人が集う様子は、実を求めて枝先に集まる鳥の姿を思わせる。アサイーを求めて立ち寄る人々が一時的に集まり、またそれぞれの行き先へと散っていく。その一方で、店内で飲食を楽しまれる際には、自然と人がテーブルを囲み、短い時間ながらも場が生まれる構成とした。

「アサイーのスタンド」と「植物の魅力に引き寄せられる人」という二つの要素で空間を構成している。自然物が持つ形や力に惹かれ、人が集い、また流れていく。その繰り返しが、この場所に軽やかな滞留とリズムを生み出し、都市の動線の中にSUGARYらしい風景をつくり出し、それそのものが店舗のファサードとなる計画とした。

設計・監理：a.d.p（坂田裕貴、安部くる実）　協力：タムテ 柳館

施工：ヤシマ工業

天板：torinoki furniture

所在地：大阪府

用途：店舗（改修）

構造：鉄骨造

延床面積：26.1m²

竣工：2025年8月

写真：circle photo studio''',
}

CAT_LABELS = {'house': '住宅', 'shop': '店舗', 'office': 'オフィス', 'landscape': 'ランドスケープ・小屋', 'furniture': '家具'}

# 竣工年月（Work一覧の新しい順ソート用）。全件2026-07-14に坂田さん確認で確定。
# bistro-endroll(2013-06)はHandiHouse project時代の実績のため最下部（家具の直前）。
# 家具2件は日付に関わらず末尾固定（0000-）。新規事例はここに1行足せば自動で新しい順に並ぶ。
COMPLETION = {
 'new-case-study-house': '2025-11',
 'sugary-hankyu': '2025-08',
 'kitakamakura': '2025-07',
 'kuppography-takanawa': '2025-06',
 'sugary-imaizumi': '2025-06',
 'luzesombra-hq': '2022-08',
 'table-room': '2023-11',
 'renovation-of-new-wild': '2023-09',
 'patisserie-minimal': '2023-09',
 'backyard-in-field': '2022-11',
 'nkhc-landscape': '2022-07',
 'tani-house': '2022-04',
 'circle-photo-studio': '2021-11',
 'office-in-komazawa': '2021-09',
 'renovation-for-green': '2021-09',
 'kuppography-okinawa': '2021-08',
 'kuppography-komazawa': '2020-06',
 'bistro-endroll': '2013-06',
 # 家具は最後に固定
 'rounded-dining-table': '0000-02',
 '108': '0000-01',
}

# Work一覧・Selected Works・OGPのサムネイル指定（省略時は各事例の最初の画像）
THUMBNAILS = {
 'renovation-of-new-wild': '04_adp_nezu_takuyaseki_4362_web_sRGB.jpg',
 'kuppography-komazawa': '03_02_interior_ume.jpg',
}

# トップのSelected Works（3件・表示順）。ここを書き換えるだけで差し替えられる
FEATURED = ['renovation-of-new-wild', 'kitakamakura', 'kuppography-komazawa']

# 日本語タイトルの作品に併記する英語タイトル
SUBTITLES = {
 'renovation-of-new-wild': 'Renovation of new wild',
 'tani-house': 'Tani House in Setagaya',
 'sugary-imaizumi': 'Sugary Imaizumi',
 'kuppography-takanawa': 'Kuppography Takanawa Gateway',
 'kuppography-komazawa': 'Kuppography Komazawa',
 'kuppography-okinawa': 'Kuppography Okinawa',
 'backyard-in-field': 'Backyard in Field',
 'renovation-for-green': 'Renovation for Green',
 'office-in-komazawa': 'Office in Komazawa',
}

# 本文先頭に残っている旧タイトル行を落とすための接頭辞（h1と重複するため）
OLD_TITLE_LINES = {
 'renovation-of-new-wild': ('Renovation of new wild',),
 'tani-house': ('Tani House in Setagaya',),
 'sugary-imaizumi': ('Sugary 今泉店',),
 'kuppography-takanawa': ('Kuppography Takanawa Gateway',),
 'kuppography-komazawa': ('Kuppography Komazawa', 'クッポグラフィー'),
 'kuppography-okinawa': ('Kuppography Okinawa', 'クッポグラフィー'),
 'renovation-for-green': ('Incity cottage',),
 'office-in-komazawa': ('Office in Komazawa',),
 'patisserie-minimal': ('Patisserie Minimal Soshigaya-Okura',),
 'luzesombra-hq': ('LUZeSOMBRA HeadQuarters',),
}

# 事例ページへの追記ブロック（施主の声・掲載記事など。本文と写真の間に入る）
PROJECT_EXTRAS = {
 'renovation-of-new-wild': '''<aside class="press">
<h2>この住まいが記事になりました</h2>
<p>ご入居後、施主ご自身がリノベーションの進め方とその後の暮らしをSUUMOジャーナルで語ってくださいました。</p>
<p><a href="https://suumo.jp/journal/2024/01/16/200044/" target="_blank" rel="noopener">「要求定義」から自宅リノベを始めてみた。建築家とアイデアふくらみ想像以上の仕上がりに！（SUUMOジャーナル）→</a></p>
</aside>''',
}

NAV = '''<header class="site-header">
  <a class="logo" href="{root}index.html">a.d.p</a>
  <nav>
    <a href="{root}about.html">About</a>
    <a href="{root}work/index.html">Work</a>
    <a href="{root}flow.html">Flow</a>
    <a href="{root}recruit.html">Recruit</a>
    <a class="cta-btn" href="{root}contact.html" aria-label="ご相談・お問い合わせ"><svg class="mail-icon" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2.5" y="4.5" width="19" height="15" rx="1.5"/><path d="M3 6.5l9 7 9-7"/></svg><span class="cta-text">ご相談・お問い合わせ</span></a>
  </nav>
</header>'''

FOOTER = '''<section class="cta-section">
  <h2>建築・内装の設計のご相談を承っています</h2>
  <p>「まだ計画が固まっていない」「土地探しの段階」でも構いません。<br>設計・監理は全国各地に対応、首都圏では小規模な施工もお受けしています。<br>まずはお気軽にご相談ください。</p>
  <a class="cta-btn large" href="{root}contact.html">ご相談・お問い合わせ →</a>
</section>
<footer class="site-footer">
  <p>一級建築士事務所 a.d.p ｜ 株式会社a.d.p</p>
  <p>TOKYO OFFICE：東京都目黒区青葉台3-18-10 401</p>
  <p>一級建築士事務所 神奈川県知事登録 第18366号 ／ 建設業許可 神奈川県知事許可（般-6）第92224号</p>
  <p><a href="https://www.instagram.com/anhelo_de_plantas/" target="_blank" rel="noopener">Instagram</a>　<a href="{root}privacy.html">プライバシーポリシー</a></p>
  <p class="copy">© a.d.p</p>
</footer>'''

BASE_URL = 'https://www.adp-ad.jp'
OG_DEFAULT = ['/']  # buildの序盤でヒーロー画像パスに差し替える

# Google Analytics 4 測定ID（空文字なら計測タグを出力しない）
GA_MEASUREMENT_ID = ''

def ga_snippet():
    if not GA_MEASUREMENT_ID:
        return ''
    return f'''<script async src="https://www.googletagmanager.com/gtag/js?id={GA_MEASUREMENT_ID}"></script>
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){{dataLayer.push(arguments);}}
gtag('js', new Date());
gtag('config', '{GA_MEASUREMENT_ID}');
</script>'''

JSONLD = '''<script type="application/ld+json">
{
 "@context": "https://schema.org",
 "@type": "ProfessionalService",
 "name": "一級建築士事務所 a.d.p",
 "alternateName": "株式会社a.d.p",
 "url": "https://www.adp-ad.jp/",
 "founder": {"@type": "Person", "name": "坂田裕貴", "jobTitle": "一級建築士"},
 "address": {"@type": "PostalAddress", "addressRegion": "東京都", "addressLocality": "目黒区", "streetAddress": "青葉台3-18-10 401"},
 "sameAs": ["https://www.instagram.com/anhelo_de_plantas/"],
 "description": "建築・内装の設計・監理を全国で行う一級建築士事務所。首都圏では小規模施工も。"
}
</script>'''

def page(title, body, root='', desc='一級建築士事務所 a.d.p ─ 建築・内装の設計・監理を全国で、首都圏では小規模施工も。横浜・東京を拠点に活動。', path='', og_image=None):
    canonical = f'{BASE_URL}/{path}'
    og = og_image or OG_DEFAULT[0]
    return f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{BASE_URL}{og}">
<meta property="og:site_name" content="a.d.p">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{root}assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{root}assets/style.css">
{JSONLD}
{ga_snippet()}
</head>
<body>
{NAV.format(root=root)}
<main>
{body}
</main>
{FOOTER.format(root=root)}
</body>
</html>'''

PORTRAIT_SRC = os.path.join(BASE, 'assets_src', 'profile', 'portrait.jpg')

def build_portrait():
    """代表ポートレート（assets_src/profile/portrait.jpg）からWeb用2種を生成。
    横長版=About用 / 正方形版=トップ署名用。写真が無ければ両方Noneを返す。"""
    if not os.path.exists(PORTRAIT_SRC):
        return None, None
    from PIL import Image, ImageOps
    dstdir = os.path.join(SITE, 'assets', 'img', 'profile')
    os.makedirs(dstdir, exist_ok=True)
    im = ImageOps.exif_transpose(Image.open(PORTRAIT_SRC)).convert('RGB')
    w, h = im.size
    cx = int(w * 0.52)  # 顔がわずかに右寄りのため中心を調整
    # About用: 縦は元のまま（クロップしない）、横だけ人物中心に切って表示幅をテキスト1行に合わせる。
    # 表示アスペクト比 = ポジション文の幅468 : 現在の表示高さ296（＝縦は今の見た目のまま）
    aw = min(w, round(h * 468 / 296))
    aleft = max(0, min(w - aw, cx - aw // 2))
    wide = im.crop((aleft, 0, aleft + aw, h))
    wide.thumbnail((1600, 1600), Image.LANCZOS)
    wide.save(os.path.join(dstdir, 'portrait.jpg'), 'JPEG', quality=82, optimize=True, progressive=True)
    side = min(w, h)
    left = max(0, min(w - side, cx - side // 2))
    sq = im.crop((left, 0, left + side, side)).resize((480, 480), Image.LANCZOS)
    sq.save(os.path.join(dstdir, 'portrait_sq.jpg'), 'JPEG', quality=85, optimize=True)
    return 'assets/img/profile/portrait.jpg', 'assets/img/profile/portrait_sq.jpg'

def copy_images(old_key, new_key):
    # 新規事例は assets_src/work/<slug>/ が優先（00_inboxから最適化して配置）
    srcdir = os.path.join(BASE, 'assets_src', 'work', new_key)
    if not os.path.isdir(srcdir):
        srcdir = os.path.join(MIG, 'images_web', old_key)
    if not os.path.isdir(srcdir):
        srcdir = os.path.join(MIG, 'images', old_key)
    dstdir = os.path.join(SITE, 'assets', 'img', new_key)
    files = []
    if os.path.isdir(srcdir):
        os.makedirs(dstdir, exist_ok=True)
        for f in sorted(os.listdir(srcdir)):
            if not os.path.exists(os.path.join(dstdir, f)):
                shutil.copy2(os.path.join(srcdir, f), os.path.join(dstdir, f))
            files.append(f)
    return files

SKIP_PARAS = {'anhelo de plantas', 'Made with Squarespace'}
REPLACE_TEXT = {
    '目黒区青葉台3-18-10 CASA青葉台 401': '東京都目黒区青葉台3-18-10 401',
    'TOKYO OFFICE  :': 'TOKYO OFFICE :',
    '建築家／一級建築士　国土交通大臣登録 第372820号': '建築家／一級建築士',
}

def paragraphs(texts, skip_exact=(), skip_prefixes=()):
    out = []
    for t in texts:
        for para in t.split('\n\n'):
            para = para.strip()
            for old, new in REPLACE_TEXT.items():
                para = para.replace(old, new)
            # 所在地は都道府県までの表記に統一（事務所住所はハードコードなので影響なし）
            para = re.sub(r'^(所在地[：:]\s*)([^都道府県]*?[都道府県]).*$', r'\1\2', para, flags=re.M)
            para = re.sub(r'^(Location:\s*).*?,\s*(\S+)\s*$', r'\1\2', para, flags=re.M)
            if (para and para not in SKIP_PARAS and para not in skip_exact
                    and not any(para.startswith(p) for p in skip_prefixes)):
                out.append('<p>' + html.escape(para).replace('\n', '<br>') + '</p>')
    return '\n'.join(out)

# ---- 生成開始 ----
if os.path.isdir(SITE):
    shutil.rmtree(SITE)
os.makedirs(os.path.join(SITE, 'assets', 'img'), exist_ok=True)
os.makedirs(os.path.join(SITE, 'work'), exist_ok=True)

shutil.copy2(os.path.join(BASE, 'style.css'), os.path.join(SITE, 'assets', 'style.css'))
shutil.copy2(os.path.join(BASE, 'favicon.svg'), os.path.join(SITE, 'assets', 'favicon.svg'))

# OGP既定画像＝トップのヒーロー画像
_home_files = copy_images('home', 'home')
if _home_files:
    OG_DEFAULT[0] = f'/assets/img/home/{_home_files[0]}'

# 代表ポートレート（無ければ両方None＝写真なしで生成される）
portrait_wide, portrait_sq = build_portrait()

# --- プロジェクトページ ---
work_cards = []
for old_key, (slug, title, cat) in PROJECTS.items():
    files = copy_images(old_key, slug)
    texts = [NEW_TEXTS[slug]] if slug in NEW_TEXTS else content.get(old_key, {}).get('texts', [])
    gallery = '\n'.join(
        f'<figure><img src="../assets/img/{slug}/{f}" alt="{html.escape(title)}" loading="lazy"></figure>'
        for f in files)
    body = f'''<article class="project">
<h1>{html.escape(title)}</h1>
{f'<p class="subtitle">{html.escape(SUBTITLES[slug])}</p>' if slug in SUBTITLES else ''}
<div class="project-text">{paragraphs(texts, skip_exact={title}, skip_prefixes=OLD_TITLE_LINES.get(slug, ()))}</div>
{PROJECT_EXTRAS.get(slug, '')}
<div class="gallery">{gallery}</div>
<p class="backlink"><a href="index.html">← Work一覧へ戻る</a></p>
</article>'''
    thumb = THUMBNAILS.get(slug) or (files[0] if files else '')
    og = f'/assets/img/{slug}/{thumb}' if thumb else None
    with open(os.path.join(SITE, 'work', f'{slug}.html'), 'w') as f_:
        f_.write(page(f'{title} | a.d.p', body, root='../', path=f'work/{slug}.html', og_image=og))
    work_cards.append((slug,
        f'<a class="card" data-cat="{cat}" href="{slug}.html"><img src="../assets/img/{slug}/{thumb}" alt="{html.escape(title)}" loading="lazy">'
        f'<span class="cat-label">{CAT_LABELS[cat]}</span><span class="title-label">{html.escape(title)}</span></a>'))

# --- Work一覧（全件1グリッド＋カテゴリフィルタ。竣工の新しい順）---
work_cards.sort(key=lambda x: COMPLETION.get(x[0], '0000'), reverse=True)
work_cards = [card_html for _, card_html in work_cards]
FILTERS = [('all', 'すべて')] + list(CAT_LABELS.items())
filter_btns = ''.join(
    f'<button class="filter-btn{" active" if key == "all" else ""}" data-filter="{key}">{label}</button>'
    for key, label in FILTERS)
work_body = f'''<h1>Work</h1>
<div class="filters">{filter_btns}</div>
<div class="grid" id="work-grid">{''.join(work_cards)}</div>
<script>
document.querySelectorAll('.filter-btn').forEach(btn => btn.addEventListener('click', () => {{
  document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  const f = btn.dataset.filter;
  const grid = document.getElementById('work-grid');
  grid.classList.toggle('show-titles', f !== 'all');
  grid.querySelectorAll('.card').forEach(c => {{
    c.style.display = (f === 'all' || c.dataset.cat === f) ? '' : 'none';
  }});
}}));
</script>'''
with open(os.path.join(SITE, 'work', 'index.html'), 'w') as f_:
    f_.write(page('Work | a.d.p', work_body, root='../', path='work/index.html'))

# --- Home ---
# 役割分担: トップ=哲学文＋署名のみ。経歴・登録番号・住所ブロックはAboutに一本化（2026-07-07決定）
home_texts = [t for t in content.get('home', {}).get('texts', [])
              if not t.startswith('坂田') and not t.startswith('一級建築士事務所')]
home_files = copy_images('home', 'home')
hero_img = f'<img class="hero-img" src="assets/img/home/{home_files[0]}" alt="anhelo de plantas">' if home_files else ''
featured_cards = []
_by_slug = {slug: (old, t, c) for old, (slug, t, c) in PROJECTS.items()}
for slug in FEATURED:
    old, t, c = _by_slug[slug]
    fs = copy_images(old, slug)
    if fs:
        thumb = THUMBNAILS.get(slug) or fs[0]
        featured_cards.append(
            f'<a class="card" href="work/{slug}.html"><img src="assets/img/{slug}/{thumb}" alt="{html.escape(t)}" loading="lazy"><span>{html.escape(t)}</span></a>')
home_body = f'''<section class="hero">
<h1>anhelo de plantas</h1>
<p class="tagline">a.d.pは、建築と内装の設計・監理を行う一級建築士事務所です。</p>
{hero_img}
</section>
<section class="philosophy">
{paragraphs(home_texts)}
{f'<div class="signature"><img src="{portrait_sq}" alt="代表 坂田裕貴" loading="lazy"><span>代表・一級建築士<br>坂田 裕貴</span></div>' if portrait_sq else ''}</section>
<section class="featured">
<h2>Selected Works</h2>
<div class="grid">{''.join(featured_cards)}</div>
<p class="more"><a href="work/index.html">すべての事例を見る →</a></p>
</section>'''
with open(os.path.join(SITE, 'index.html'), 'w') as f_:
    f_.write(page('a.d.p | 一級建築士事務所（横浜・東京）', home_body))

# --- About ---
# 役割分担: About=経歴・事務所概要・掲載メディアのみ。哲学文はトップに一本化（2026-07-07決定）
about_body = f'''<h1>About</h1>
<p class="position">a.d.pは、建築と内装の設計・監理を行う一級建築士事務所です。</p>
<div class="profile">
<p class="profile-name">坂田 裕貴<span>Yuki Sakata</span></p>
<p class="profile-title">建築家／一級建築士</p>
<ul class="career">
<li><span>1986</span>福岡県生まれ</li>
<li><span>2006</span>ICS College of Arts</li>
<li><span>2009</span>設計事務所勤務</li>
<li><span>2011</span>フリーランス活動開始・HandiHouse project 共同創業</li>
<li><span>2018</span>株式会社 HandiHouse project 設立</li>
<li><span>2022</span>株式会社 a.d.p 設立</li>
</ul>
</div>
{f'<figure class="portrait"><img src="{portrait_wide}" alt="代表 坂田裕貴" loading="lazy"><figcaption>代表　坂田 裕貴</figcaption></figure>' if portrait_wide else ''}
<h2>メンバー</h2>
<ul class="members">
<li>高橋 万里江</li>
<li>安部 くる実</li>
<li>近森 麦人</li>
<li>田部 堅大</li>
</ul>
<h2>事務所概要</h2>
<table class="office">
<tr><th>名称</th><td>一級建築士事務所 a.d.p（アデペ）／ 株式会社a.d.p</td></tr>
<tr><th>代表</th><td>坂田 裕貴（一級建築士 大臣登録第372820号）</td></tr>
<tr><th>所在地</th><td>TOKYO OFFICE：東京都目黒区青葉台3-18-10 401</td></tr>
<tr><th>登録</th><td>一級建築士事務所 神奈川県知事登録 第18366号</td></tr>
<tr><th>建設業許可</th><td>神奈川県知事許可（般-6）第92224号</td></tr>
<tr><th>設立</th><td>2022年1月</td></tr>
</table>
<h2>掲載メディア</h2>
<p class="media-list">商店建築　／　カフェの設計学（学芸出版社）　／　XXI（トルコ）　／　TOKOSIE　／　TECTURE MAG　／　architecturephoto.net</p>'''
with open(os.path.join(SITE, 'about.html'), 'w') as f_:
    f_.write(page('About | a.d.p', about_body, path='about.html'))

# --- Flow（依頼の流れ）---
flow_body = '''<h1>設計のご依頼の流れ</h1>
<p class="lead">設計事務所への依頼がはじめての方にも安心していただけるよう、ご相談から完成までの流れをご紹介します。</p>
<ol class="flow">
<li><h3>ご相談（無料）</h3><p>お問い合わせフォームよりご連絡ください。計画が固まっていない段階でも歓迎です。オンラインでのご相談も可能です。</p></li>
<li><h3>敷地・物件の調査</h3><p>敷地や既存建物の状況、法規制を確認し、計画の前提条件を整理します。</p></li>
<li><h3>基本設計のご提案</h3><p>対話を重ねながら、暮らし方・使い方に合わせた設計案をご提案します。</p></li>
<li><h3>設計契約</h3><p>内容にご納得いただけたら、設計監理契約を締結します。</p></li>
<li><h3>実施設計</h3><p>工事に必要な詳細図面を作成し、確認申請を行います。</p></li>
<li><h3>見積・施工者選定</h3><p>施工会社からの見積を精査し、適正な価格での契約をサポートします。首都圏の小規模な工事であれば、a.d.pが設計から施工まで一貫してお受けすることも可能です。</p></li>
<li><h3>工事監理</h3><p>設計図の通りに工事が行われているか、設計者の目で現場を確認します。</p></li>
<li><h3>お引き渡し</h3><p>完成後も、住まいながら・使いながらの調整やご相談に対応します。</p></li>
</ol>
<h2>よくあるご質問</h2>
<dl class="faq">
<dt>Q. 相談したら必ず契約しないといけませんか？</dt>
<dd>A. いいえ。初回のご相談は無料で、契約義務はありません。</dd>
<dt>Q. 遠方でも対応できますか？</dt>
<dd>A. 全国各地で設計・監理の実績があります。お気軽にご相談ください。</dd>
<dt>Q. 施工もお願いできますか？</dt>
<dd>A. 首都圏の小規模な工事であれば、設計から施工まで一貫してお受けできます（建設業許可 神奈川県知事許可（般-6）第92224号）。規模や地域により、信頼できる施工会社をご紹介し設計監理者として品質を確認する形も取れます。</dd>
<dt>Q. 予算が決まっていなくても相談できますか？</dt>
<dd>A. はい。予算計画の整理からご一緒します。</dd>
</dl>'''
with open(os.path.join(SITE, 'flow.html'), 'w') as f_:
    f_.write(page('設計のご依頼の流れ | a.d.p', flow_body, path='flow.html'))

# --- Recruit ---
recruit_body = '''<h1>Recruit</h1>
<div class="prose">
<p>a.d.pでは、ともに空間づくりの可能性を広げてくれる仲間を募集しています。</p>
<h2>私たちのこと</h2>
<p>住宅・店舗・保育施設など、新築・内装のさまざまな空間をデザインしています。クライアントとのコミュニケーションを大切にし、その場所にしかない魅力を見出しながら、自然と調和し、人の感覚や感情に寄り添った空間設計を行っています。小規模な事務所だからこそ、スタッフ一人ひとりがプロジェクトの中心となり、アイデアを直接反映できる環境です。</p>
<p>時には施工まで一貫して請け負うことで、自ら現場に入り込み、つくる過程で生まれるアイデアを柔軟に取り入れ、「空間を考え、つくる」ことを大切にしています。</p>
<h2>いっしょに働きたい人</h2>
<p>大切にしているのは、機嫌よく働くことです。余裕をもって気持ちよく仕事ができているときほど、良いアイデア、いいチームワークが生まれ、良いものづくりにつながると考えています。</p>
<p>コンセプトや目指す感覚をかたちにしていく過程には、ものづくりの愉しさが詰まっています。その愉しさを共有し、協力し合える人と、チームをつくっていきたいと思っています。</p>
<p>デザインの検討から現場の監理・施工まで幅広く関わること。自然や植物を活かした独自の視点。外部パートナーとの協働から生まれる多様な考え方との出会い。a.d.pでの仕事には、考えることとつくることの両方があります。主体的に学びながら、幅広い経験を積みたい方をお待ちしています。</p>
<h2>募集要項</h2>
</div>
<table class="office">
<tr><th>募集職種</th><td>建築設計スタッフ（新卒・中途）</td></tr>
<tr><th>勤務地</th><td>東京都目黒区青葉台</td></tr>
<tr><th>勤務形態</th><td>正社員（試用期間あり）</td></tr>
<tr><th>勤務時間</th><td>フレックスタイム制。打合せや現場に合わせて土日祝に稼働することもあれば、平日に休むこともあります。</td></tr>
<tr><th>給与・待遇</th><td>経験・能力に応じて決定、交通費支給、各種保険完備</td></tr>
</table>
<div class="prose">
<h2>ご応募について</h2>
<p>興味をお持ちいただいた方は、まずは<a href="contact.html">Contactページ</a>よりお気軽にご連絡ください。その後、ポートフォリオと履歴書をメールでお送りいただき、面談をさせていただきます。</p>
</div>'''
with open(os.path.join(SITE, 'recruit.html'), 'w') as f_:
    f_.write(page('Recruit | a.d.p', recruit_body, path='recruit.html'))

# --- Contact ---
contact_body = '''<h1>Contact</h1>
<div class="prose">
<p>設計・施工のご依頼・ご相談、取材等のお問い合わせは下記フォームよりご連絡ください。</p>
<ul class="reassure">
<li>初回のご相談は無料です</li>
<li>計画が具体的でない段階のご相談も歓迎します</li>
<li>設計・監理は全国各地に対応しています</li>
<li>首都圏では小規模な施工もお受けしています</li>
<li>1週間以内にメールにてご返信いたします</li>
</ul>
</div>
<form class="contact-form" action="https://formspree.io/f/mrenggya" method="POST">
<label>お名前 <span class="req">必須</span><input type="text" name="name" required></label>
<label>メールアドレス <span class="req">必須</span><input type="email" name="_replyto" required></label>
<label>ご相談の種類
<select name="type">
<option>住宅の新築</option>
<option>リノベーション・内装</option>
<option>店舗・オフィス</option>
<option>家具</option>
<option>採用について</option>
<option>取材・その他</option>
</select></label>
<label>建設予定地・物件所在地（未定でも構いません）<input type="text" name="location"></label>
<label>ご希望の時期（未定でも構いません）<input type="text" name="timing"></label>
<label>ご相談内容<textarea name="message" rows="6"></textarea></label>
<p class="privacy-note">送信いただいた個人情報は<a href="privacy.html">プライバシーポリシー</a>に基づき取り扱います。</p>
<button type="submit" class="cta-btn large">送信する</button>
</form>
<script>
const form = document.querySelector('.contact-form');
form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const btn = form.querySelector('button');
  btn.disabled = true; btn.textContent = '送信中…';
  try {
    const res = await fetch(form.action, {method: 'POST', body: new FormData(form), headers: {'Accept': 'application/json'}});
    if (!res.ok) throw new Error();
    form.innerHTML = '<p class="sent">お問い合わせありがとうございました。<br>1週間以内にメールにてご返信いたします。</p>';
  } catch {
    btn.disabled = false; btn.textContent = '送信する';
    alert('送信に失敗しました。お手数ですが、時間をおいて再度お試しください。');
  }
});
</script>'''
with open(os.path.join(SITE, 'contact.html'), 'w') as f_:
    f_.write(page('Contact | a.d.p', contact_body, path='contact.html'))

# --- プライバシーポリシー ---
privacy_body = '''<h1>プライバシーポリシー</h1>
<div class="prose">
<p>株式会社a.d.p（以下「当社」）は、当サイトをご利用いただく方の個人情報を、以下の方針に基づき取り扱います。</p>
<h2>取得する情報</h2>
<p>お問い合わせフォームより、お名前・メールアドレス・ご相談内容等をご提供いただきます。フォームの送信には外部サービス（Formspree）を利用しており、送信内容は同サービスを経由して当社に届きます。</p>
<h2>利用目的</h2>
<p>取得した個人情報は、お問い合わせへの回答、ご相談・ご依頼への対応、およびそれに付随する連絡のためにのみ利用します。</p>
<h2>第三者への提供</h2>
<p>法令に基づく場合を除き、ご本人の同意なく第三者に個人情報を提供することはありません。</p>
<h2>アクセス解析</h2>
<p>当サイトでは、サイト改善のためにアクセス解析ツールを利用する場合があります。解析データは匿名で収集され、個人を特定するものではありません。</p>
<h2>開示・訂正・削除</h2>
<p>ご自身の個人情報について開示・訂正・削除をご希望の場合は、お問い合わせフォームよりご連絡ください。すみやかに対応いたします。</p>
<p class="policy-date">制定日：2026年7月</p>
</div>'''
with open(os.path.join(SITE, 'privacy.html'), 'w') as f_:
    f_.write(page('プライバシーポリシー | a.d.p', privacy_body, path='privacy.html'))

# --- sitemap.xml / robots.txt ---
pages_for_sitemap = ['', 'about.html', 'work/index.html', 'flow.html', 'recruit.html', 'contact.html', 'privacy.html']
pages_for_sitemap += [f'work/{slug}.html' for _, (slug, _, _) in PROJECTS.items()]
sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for p in pages_for_sitemap:
    sitemap += f'  <url><loc>{BASE_URL}/{p}</loc></url>\n'
sitemap += '</urlset>\n'
with open(os.path.join(SITE, 'sitemap.xml'), 'w') as f_:
    f_.write(sitemap)
with open(os.path.join(SITE, 'robots.txt'), 'w') as f_:
    f_.write(f'User-agent: *\nAllow: /\nSitemap: {BASE_URL}/sitemap.xml\n')

# GitHub Pages 独自ドメイン（CNAMEファイル）。BASE_URLのホスト部から生成
with open(os.path.join(SITE, 'CNAME'), 'w') as f_:
    f_.write(BASE_URL.split('//', 1)[1] + '\n')

print('build complete:', SITE)
