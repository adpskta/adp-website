# a.d.p 公式サイト（adp-ad.jp）— プロジェクトガイド

Squarespaceから自前静的サイトへの移行プロジェクト。
**どのモデル・どのチャットから作業する場合も、まずこのファイルを読むこと。**

---

## プロジェクトの目的

1. 施主（新規顧客）が問い合わせしやすいHPにする（旧Squarespace版は導線が弱かった）
2. 固定費削減（Squarespace 年2〜4万円 → ドメイン代のみ）
3. 更新をClaude Code経由で完結させる

## 重要期日

- ~~2026年8月16日 = Squarespace契約更新日~~ → **解約済み（2026-07-13）**。8/16にサービス自動終了
- ドメイン adp-ad.jp は**お名前.com管理**（ユーザー記憶ベース・切替前に要確認）
- 切替時はMXレコード（メール設定）の有無を確認してから

## フォルダ構成

```
_HP/
├── CLAUDE.md          ← このファイル
├── build.py           ← 静的サイトジェネレータ（python3 build.py で site/ を全生成）
├── style.css          ← 全ページ共通スタイル（buildでsite/assets/にコピーされる）
├── 00_inbox/          ← 坂田さんからの素材受け渡し場所（README.md参照）
│   └── profile/      ← 顔写真・事務所写真の置き場
├── 01_migration/      ← 旧Squarespaceサイトから回収した全コンテンツ（原本・触らない）
│   ├── content.json  ← 全ページのテキスト・画像リスト
│   ├── images/       ← 回収画像295枚（78MB・原本）
│   ├── raw/ raw_html/ ← スクレイピング生データ
│   └── inventory_full.md ← コンテンツ棚卸し
├── site/              ← 生成物（=デプロイ対象）。直接編集禁止、必ずbuild.pyを編集して再生成
└── _old_2022_企画資料/ ← 旧サイト企画時の資料（アーカイブ）
```

## 公開・ホスティング（2026-07-13 本番移行）

- **本番URL: https://www.adp-ad.jp**（GitHub Pagesでホスティング・無料）
- **GitHubリポジトリ: https://github.com/adpskta/adp-website**（public・アカウント @adpskta）
- **デプロイ方法: `git push origin main` で自動公開**（.github/workflows/deploy.yml が site/ をPagesへ）
- 独自ドメイン: build.py が site/CNAME（www.adp-ad.jp）を生成。DNSはお名前.comで管理
  - Aレコード @ → 185.199.108〜111.153（GitHub Pages）／ www CNAME → adpskta.github.io
  - MX（Google）・TXT は移行時も維持（メール受信は影響なし）
- push認証: gh CLI を `~/.local/bin/gh` に常設し、`credential.helper` に登録済み（2026-08-05恒久化）。**このMacでは追加設定なしでpushできる**。別マシンでは gh のインストールと `gh auth login` が必要

## 作業ルール

1. **site/ を直接編集しない**。文言・構成の変更はすべて `build.py` を編集 → `python3 build.py` で再生成
2. **変更したら commit → `git push origin main` で本番反映**（1〜2分でGitHub Actionsがデプロイ）
3. プレビュー: `python3 -m http.server 8765 --directory site/` → http://localhost:8765（スマホ実機は http://<MacのIP>:8765）
4. 事例の追加: `00_inbox/README.md` の手順どおり。実装は次の4点セット
   - 写真を長辺1600px/JPEG82に最適化して `assets_src/work/<slug>/` へ（copy_imagesがここを最優先で見る）
   - `PROJECTS` に末尾追加（キーは `new__<slug>`。※先頭3件がトップのSelected Worksになるので末尾が安全）
   - 本文・クレジットは `NEW_TEXTS[slug]` に空行区切りで記述（content.jsonに無いため）
   - `COMPLETION[slug]` に竣工年月（Work一覧はこれで新しい順ソート）
5. 公開前に坂田さんの文言確認を必ず挟む
6. 旧Squarespace回収データ（01_migration/）と社内資料（_old_2022_企画資料/）は .gitignore でGitHub非公開。旧git履歴はローカルの archive/local-history ブランチに保全
7. **旧URLリダイレクト**: build.py が PROJECTS のキーから旧SquarespaceのURL（`work__foo` → `/work/foo`）を導出し、canonical＋meta refresh の転送ページを自動生成する（20件）。事例のslugを変えたら転送先も自動追従するので手動管理は不要

## サイト構成（2026-07-07時点）

**トップとAboutは役割分担（2026-07-07決定・重複禁止）**：トップ＝世界観（哲学文）、About＝人と信頼（経歴・概要）。同じ文章を2ページに載せない。

- Home: hero「anhelo de plantas」＋直下にポジショニング1行＋ヒーロー画像＋哲学文＋署名（丸写真＋代表名）＋Selected Works 3件＋CTA（経歴はAboutへ一本化）
- Work: 全19件を1グリッド＋カテゴリフィルタ（すべて／住宅／店舗／オフィス／ランドスケープ・小屋／家具）。カードのラベルは「すべて」表示時＝カテゴリ名、カテゴリ絞り込み時＝タイトルに切り替わる（坂田さん指示 2026-07-07）。LUZeSOMBRAは店舗扱い。サムネイル差し替えは build.py の THUMBNAILS
- About: ポジショニング1行＋経歴年表＋ポートレート＋メンバー4名（高橋万里江・安部くる実・近森麦人・田部堅大）＋事務所概要表＋掲載メディア（哲学文なし）
- Flow: 依頼の流れ8ステップ＋FAQ（費用・期間セクションは意図的に未掲載↓）
- Recruit: 機嫌よく働くことにさらっと触れる控えめな文章＋募集要項（2026-07-06に「ご機嫌」の強い打ち出しをトーンダウン・坂田さん指示）
- Contact: Formspreeフォーム稼働中（Form ID: mrenggya・送信先 info@adp-ad.jp・2026-07-13設定）

## 営業戦略（2026-07-07 坂田さん）

- **直近ターゲット＝東京・神奈川のマンションリノベ（設計施工で受注）**。住宅事例が動いていない＋設計施工は期間あたり利益が良い＋規模的に慣れていて問題が起きづらいため
- フック＝「生前からある都市に住む」（renovation-of-new-wild・台東区・設計施工）。施主が書いたSUUMOジャーナル記事（https://suumo.jp/journal/2024/01/16/200044/）を事例ページにリンク済み。Selected Works先頭に配置

## 外部メディア・広報（2026-08-08時点）

### KLASIC（月額契約・要ROI判定）
- リノベーション情報サイト klasic.jp に月額 **11,000円（税込）／年13.2万円**で掲載中（営業代行的な位置づけ）。会計上は広告宣伝費「スタジオアフロ」として計上
- 2026-08-07 に「生前からある都市に住む」のM邸記事が公開: https://www.klasic.jp/renovation/59944
- **導線の実態**: 記事本文に adp-ad.jp への直リンクは無し。記事 → KLASIC内の事務所ページ（/office/48725）→ そこに初めてHPリンク。**2クリック必要**
- 坂田さんの見立て: 3〜4年で1〜2件受注できれば、というつもりで契約
- **判定方針（2026-08-08合意）**: 4年待たずに、GA4の参照元データで半年（〜2027年2月）を目安に判断する
  - 見る指標: klasic.jp からの流入数／その訪問者がContactページに到達しているか／記事公開前後の変化
  - 流入があるのに問い合わせに繋がらない場合は、契約ではなくHP側（着地後の導線）の改善課題
  - ※アクセス解析に出ない価値（他で名前を知った施主が検索した際の裏付け・信頼形成）もある点は考慮する

## 確定済みの方針・文言ルール

- 事業内容: **建築・内装の設計・監理（全国）＋首都圏では小規模施工も**。「施工のみ」は請けない
- **神奈川の住所は非公開**。所在地表記は「TOKYO OFFICE：東京都目黒区青葉台3-18-10 401」のみ
- トップのhero直下にポジショニング1行（「a.d.pは、建築と内装の設計・監理を行う一級建築士事務所です。」）を表示（2026-07-13変更。検索スニペットが哲学文冒頭を拾い「何の会社か」不明だったため。※以前の「タグライン入れない」指示の例外・坂田さん確認済みの場合はこの注記を消す）
- 返信目安は「1週間以内」
- 事例の所在地は**都道府県まで**の表記（build.pyのparagraphs()で自動変換。事務所住所は対象外）
- 事例タイトルは**日本語主＋英語サブタイトル併記**（PROJECTSに日本語、SUBTITLESに英語）
- Flowの費用・期間目安: 設計見積もり雛形を作り直した後に掲載予定。方針=目安提示しつつ「内容を伺ってから見積もり」。参考: https://www.hata-archi.com/costflow/ / https://www.n-archi-o.com/#flow

## 未完了タスク（優先順）

- [x] 顔写真をAbout（横長）＋トップ哲学文の署名（丸アイコン）に組み込み 済 2026-07-06
  - 原本: assets_src/profile/portrait.jpg（00_inbox/profile/004.jpg 由来）。build.py の build_portrait() がWeb用2種を自動生成
- [ ] 坂田さん: 代表事例3〜5件のストーリーメモ → ケーススタディ化（施主の声も可能なら）
- [ ] **バス停前の長屋の本文差し替え**：現在はメモを整形した暫定版（2026-07-24公開）。坂田さんが正式な説明テキストを作成予定 → NEW_TEXTS['bus-stop-nagaya'] を差し替える
- [x] 事例タイトルの日本語化（方針=日本語主＋英語サブタイトル併記・店名等の固有名詞はそのまま）済 2026-07-07
  - 生前からある都市に住む／北鎌倉の増築／谷の家（2026-07-24に「世田谷」を削除）／Sugary 今泉／畑のBackyard／緑のためのリノベーション（旧Incity cottage表記は坂田さん指示で整理）／クッポグラフィー 高輪ゲートウェイスタジオ・駒沢公園スタジオ・沖縄スタジオ
  - 英語のまま: bistro endroll・circle photo studio・Patisserie Minimal・LUZeSOMBRA HQ・NKHC・New Case Study House・Table Room・家具2件（＋駒沢のオフィスに改名済みのOffice in Komazawaは除く）
  - 高輪ゲートウェイスタジオの命名も坂田さん承認済み（2026-07-07）
- [x] Office in Komazawa →「駒沢のオフィス」／Table Room→現状維持（固有名詞扱い・坂田さん決定 2026-07-07）
- [x] New Case Study House →「ニューケーススタディハウス」（英語サブタイトル併記）2026-07-24
- [ ] **本文が未執筆の事例5件**（旧サイトの "Text content coming soon." を非表示にしただけで、現在クレジットのみ表示）: 北鎌倉の増築／クッポグラフィー高輪ゲートウェイ／bistro endroll／circle photo studio／ニューケーススタディハウス → 坂田さんの本文待ち（00_inboxに `既存_事例名.txt` でメモを置けば文章化します）
- [x] トップにポジショニング1行（哲学文の手前）済 2026-07-06
- [x] 画像最適化（optimize_images.py・長辺1600px JPEG82。素材追加時は build 前に実行）済
- [x] OGP・JSON-LD・sitemap.xml・robots.txt・favicon 済
- [x] プライバシーポリシー＋フォームAJAX送信（インライン完了表示）済
- [x] Formspree稼働（Form ID mrenggya・送信先 info@adp-ad.jp）2026-07-13
- [x] 本番公開完了 2026-07-13: GitHub Pages＋独自ドメイン（HTTPS強制済・MX無傷・フォームテスト受信確認済）
- [x] Squarespace解約完了 2026-07-13（8/16に自動終了・以降課金なし。**Resubscribeボタンは押さない**。誤複製した「a.d.p (Copy)」トライアルは7/27に自動失効するので放置）
- [x] GA4導入済み 2026-08-07（測定ID: G-GV2X6LVGXT・全28ページに設置・プライバシーポリシーにオプトアウト案内も追記）
- [x] 旧URL404問題を修正 2026-08-07（移行時の積み残し。旧Squarespace URL 20件が404だった → 転送ページを自動生成。外部リンクとSEO評価を新URLへ引き継ぎ）
- [x] Search Console設定完了 2026-08-07（ドメインプロパティ `sc-domain:adp-ad.jp`・DNS TXT認証・sitemap.xml送信済み28ページ検出・トップのインデックス登録リクエスト済み）
  - ⚠️ 認証用TXT `google-site-verification=2igKFgUXG4zfp8BS_qPacH1OVvYGTa0jsQzdTTqCh0Q` は**削除禁止**（消すと所有権が外れる）
  - ドメインプロパティなのでサイトマップ送信時は**フルURL**が必要（`sitemap.xml` だけでは不可）
- [ ] （公開後）Googleビジネスプロフィール登録

## 旧サイト（Squarespace）最終アクセス実績 — 新サイトの基準線（2026-07-13記録）

- 先月（6月）: **372訪問**（前月比+30%）
- 直近1週間: 84訪問（日平均 約12）
- 傾向: 木曜にピークが出やすい。ソース内訳は未記録
- 新サイトのアクセス解析導入後、この数字と比較して移行影響と問い合わせ導線の効果を評価する

## 経緯メモ

- 当初はSquarespace上で改修予定だったが、Claude in Chromeの既知バグ（サイト編集画面のドメインが全拒否）で断念し、作り替えに方針転換（2026-07-03）
- 補助金プロジェクト（_a.d.p management/_令和8年度…補助金/）とは別プロジェクト。当初そちらのセッションで開始したため、初期の経緯はそちらのセッション履歴にある
