#!/usr/bin/env python3
# 01_migration/images/ の原本 → 01_migration/images_web/ にWeb用最適化版を生成
# 長辺1600pxに縮小・JPEG品質82。原本は変更しない。既に生成済みのものはスキップ。
import os
from PIL import Image, ImageOps

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, '01_migration', 'images')
DST = os.path.join(BASE, '01_migration', 'images_web')
MAX_SIDE = 1600

count = skip = 0
for root, dirs, files in os.walk(SRC):
    rel = os.path.relpath(root, SRC)
    outdir = os.path.join(DST, rel)
    os.makedirs(outdir, exist_ok=True)
    for f in files:
        if not f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            continue
        src = os.path.join(root, f)
        # 出力は拡張子を .jpg に統一
        out = os.path.join(outdir, os.path.splitext(f)[0] + '.jpg')
        if os.path.exists(out) and os.path.getmtime(out) >= os.path.getmtime(src):
            skip += 1
            continue
        try:
            im = Image.open(src)
            im = ImageOps.exif_transpose(im)
            if im.mode in ('RGBA', 'P', 'LA'):
                im = im.convert('RGB')
            im.thumbnail((MAX_SIDE, MAX_SIDE), Image.LANCZOS)
            im.save(out, 'JPEG', quality=82, optimize=True, progressive=True)
            count += 1
        except Exception as e:
            print('ERROR', src, e)

print(f'optimized: {count}, skipped: {skip}')
