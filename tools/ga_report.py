#!/usr/bin/env python3
"""a.d.p 公式サイトの計測レポート生成

GA4 と Search Console のAPIから指標を取得し、Markdownで出力する。
定期タスクから無人で実行できるようにするのが目的（画面のスクショに依存しない）。

使い方:
    ~/.adp-analytics/venv/bin/python tools/ga_report.py [--days 28]

認証情報:
    ~/.adp-analytics/service-account.json
    ※ 秘密鍵のためリポジトリには絶対に置かない（このリポジトリはGitHub public）
"""
import argparse, json, os, sys, warnings
from datetime import date, timedelta

warnings.filterwarnings('ignore')  # Python 3.9のEOL警告を抑制

CRED = os.path.expanduser('~/.adp-analytics/service-account.json')
GA4_PROPERTY_ID = os.environ.get('ADP_GA4_PROPERTY_ID', '')   # 数字のみ（例 123456789）
SC_SITE = 'sc-domain:adp-ad.jp'


def fail(msg):
    print(f'ERROR: {msg}', file=sys.stderr)
    sys.exit(1)


def load_creds(scopes):
    if not os.path.exists(CRED):
        fail(f'認証情報が見つかりません: {CRED}')
    from google.oauth2 import service_account
    return service_account.Credentials.from_service_account_file(CRED, scopes=scopes)


def ga4_report(days):
    """GA4: 全体指標・流入元・よく見られたページ"""
    from google.analytics.data_v1beta import BetaAnalyticsDataClient
    from google.analytics.data_v1beta.types import (
        DateRange, Dimension, Metric, RunReportRequest, OrderBy)

    if not GA4_PROPERTY_ID:
        fail('環境変数 ADP_GA4_PROPERTY_ID が未設定です（GA4の「プロパティID」＝数字）')

    creds = load_creds(['https://www.googleapis.com/auth/analytics.readonly'])
    client = BetaAnalyticsDataClient(credentials=creds)
    rng = [DateRange(start_date=f'{days}daysAgo', end_date='today')]
    prop = f'properties/{GA4_PROPERTY_ID}'

    def run(dims, mets, limit=25, order_metric=None):
        req = RunReportRequest(
            property=prop, date_ranges=rng,
            dimensions=[Dimension(name=d) for d in dims],
            metrics=[Metric(name=m) for m in mets],
            limit=limit,
            order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name=order_metric),
                               desc=True)] if order_metric else None)
        res = client.run_report(req)
        return [([v.value for v in r.dimension_values],
                 [v.value for v in r.metric_values]) for r in res.rows]

    return {
        'totals':   run([], ['sessions', 'totalUsers', 'screenPageViews', 'averageSessionDuration']),
        'sources':  run(['sessionSource', 'sessionMedium'], ['sessions'], 20, 'sessions'),
        'pages':    run(['pagePath'], ['screenPageViews'], 30, 'screenPageViews'),
        'devices':  run(['deviceCategory'], ['sessions'], 5, 'sessions'),
    }


def sc_report(days):
    """Search Console: 検索クエリ・ページ別の表示とクリック"""
    from googleapiclient.discovery import build
    creds = load_creds(['https://www.googleapis.com/auth/webmasters.readonly'])
    svc = build('searchconsole', 'v1', credentials=creds, cache_discovery=False)
    end = date.today() - timedelta(days=2)      # SCは反映に2日ほどかかる
    start = end - timedelta(days=days)

    def q(dimension, limit=25):
        body = {'startDate': start.isoformat(), 'endDate': end.isoformat(),
                'dimensions': [dimension], 'rowLimit': limit}
        res = svc.searchanalytics().query(siteUrl=SC_SITE, body=body).execute()
        return res.get('rows', [])

    return {'period': f'{start} 〜 {end}', 'queries': q('query'), 'pages': q('page')}


def fmt(ga, sc, days):
    L = [f'# a.d.p 公式サイト 計測レポート（直近{days}日）', '',
         f'生成日: {date.today()}', '']

    L += ['## 全体', '']
    if ga['totals']:
        _, m = ga['totals'][0]
        L += [f'- セッション: **{m[0]}**', f'- ユーザー数: **{m[1]}**',
              f'- ページビュー: **{m[2]}**',
              f'- 平均滞在時間: {float(m[3])/60:.1f}分', '']
    else:
        L += ['- データなし', '']

    L += ['## 流入元', '', '| 参照元 / メディア | セッション |', '|---|---|']
    for d, m in ga['sources']:
        L.append(f'| {d[0]} / {d[1]} | {m[0]} |')

    L += ['', '## よく見られたページ', '', '| ページ | 表示回数 |', '|---|---|']
    for d, m in ga['pages']:
        L.append(f'| {d[0]} | {m[0]} |')

    L += ['', '## デバイス', '', '| 種別 | セッション |', '|---|---|']
    for d, m in ga['devices']:
        L.append(f'| {d[0]} | {m[0]} |')

    L += ['', f'## 検索クエリ（Search Console・{sc["period"]}）', '',
          '| 検索語 | 表示 | クリック | 平均掲載順位 |', '|---|---|---|---|']
    for r in sc['queries']:
        L.append(f'| {r["keys"][0]} | {r["impressions"]} | {r["clicks"]} | {r["position"]:.1f} |')

    L += ['', '## 検索で表示されたページ', '',
          '| ページ | 表示 | クリック | 平均掲載順位 |', '|---|---|---|---|']
    for r in sc['pages']:
        L.append(f'| {r["keys"][0]} | {r["impressions"]} | {r["clicks"]} | {r["position"]:.1f} |')

    return '\n'.join(L) + '\n'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--days', type=int, default=28)
    ap.add_argument('--out', default='')
    a = ap.parse_args()

    ga = ga4_report(a.days)
    try:
        sc = sc_report(a.days)
    except Exception as e:
        sc = {'period': f'取得失敗: {e}', 'queries': [], 'pages': []}

    text = fmt(ga, sc, a.days)
    if a.out:
        os.makedirs(os.path.dirname(a.out), exist_ok=True)
        open(a.out, 'w').write(text)
        print(f'書き出しました: {a.out}')
    else:
        print(text)


if __name__ == '__main__':
    main()
