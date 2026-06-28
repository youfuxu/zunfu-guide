# -*- coding: utf-8 -*-
"""
尊福祭祀商行 — SEO 內容站建置腳本
讀 content/*.md（依真實商品目錄撰寫）→ 暖色紅金設計系統 HTML，
輸出文章頁 + 首頁 + 4 分類索引。重跑即重建。
"""
import re
import html
import markdown
from pathlib import Path

ROOT = Path(r"C:\u\zunfu-guide")
SRC = ROOT / "content"
BRAND = "尊福祭祀商行"
TAGLINE = "大型儀式供品 · 廟會出陣 · 精品紙紮"
SITE_DESC = "尊福祭祀商行——嘉義在地大型儀式供品專業供應商。祝壽塔、香塔、精品紙紮、罐頭塔與廟會出陣一手包辦，服務雲嘉南高屏全省配合。"
BASE = "https://youfuxu.github.io/zunfu-guide"

# 聯絡資訊（真實，來自商品目錄）
TEL1, TEL2 = "0981-118-308", "0912-753-700"
LINE_URL = "https://line.me/ti/p/Axsh3-x874"
WEB = "https://zun-fu.com/"
ADDR = "嘉義縣水上鄉溪洲村外溪洲120-18號"

# 分類：key → (顯示名, slug, 說明)
CATS = {
    "zhushou":   ("神明祝壽供品", "zhushou",   "祝壽塔、米塔、香塔——為神明壽誕準備莊重的供品"),
    "zhongyuan": ("中元普渡",     "zhongyuan", "農曆七月普渡供品與精品紙紮的準備指南"),
    "miaohui":   ("廟會慶典",     "miaohui",   "廟會出陣、罐頭塔飲料塔——慶典排場一手包辦"),
    "liyi":      ("禮儀紙紮",     "liyi",      "蓮花塔、孝獅塔、金磚塔——莊重圓滿的禮儀紙紮"),
}
CAT_ORDER = ["zhushou", "zhongyuan", "miaohui", "liyi"]

# 檔名 → 分類
FILE_CAT = {
    "shenming-zhushou-gongpin": "zhushou",
    "xiangta-size-guide": "zhushou",
    "zhongyuan-pudu-guide": "zhongyuan",
    "miaohui-chuzhen-service": "miaohui",
    "guantouta-yinliaota": "miaohui",
    "jingpin-zhizha-liyi": "liyi",
}

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@400;500;700;900&display=swap" rel="stylesheet">')


def topbar(prefix):
    nav = "".join(f'<a href="{prefix}{CATS[c][1]}.html">{CATS[c][0]}</a>' for c in CAT_ORDER)
    return (f'<div class="topbar"><div class="wrap">'
            f'<a href="{prefix}index.html" class="logo" style="display:flex;align-items:center;gap:10px">'
            f'<img src="{prefix}assets/logo.jpg" alt="尊福祭祀商行" style="height:42px;width:auto;vertical-align:middle">'
            f'<span>尊福祭祀商行</span></a>'
            f'<div class="topnav">{nav}</div></div></div>')


def cta_block():
    return (f'<div class="cta"><h3>需要大型供品或廟會出陣？歡迎洽詢</h3>'
            f'<p>祝壽塔 · 香塔 · 精品紙紮 · 罐頭塔 · 廟會出陣，皆可客製，量大優惠。</p>'
            f'<div class="phones">'
            f'<a class="ph" href="tel:{TEL1.replace("-","")}">📞 {TEL1}<span class="who">徐小姐</span></a>'
            f'<a class="ph" href="tel:{TEL2.replace("-","")}">📞 {TEL2}<span class="who">徐先生</span></a>'
            f'</div>'
            f'<p>LINE：<a href="{LINE_URL}" target="_blank" rel="noopener">點此加入好友</a>'
            f'　|　官網：<a href="{WEB}" target="_blank" rel="noopener">zun-fu.com</a></p>'
            f'<p style="font-size:15px;color:#FBE0C0;line-height:1.7">{ADDR}<br>服務範圍：嘉義、台南、雲林、彰化、高雄、屏東（全省配合）</p></div>')


def footer():
    links = " · ".join(f'<a href="{CATS[c][1]}.html">{CATS[c][0]}</a>' for c in CAT_ORDER)
    return (f'<footer><div class="wrap">'
            f'<div><strong>{BRAND}</strong>　|　{TAGLINE}</div>'
            f'<div>電話：{TEL1}（徐小姐）／ {TEL2}（徐先生）　|　<a href="{LINE_URL}" target="_blank" rel="noopener">LINE</a>　|　<a href="{WEB}" target="_blank" rel="noopener">官網 zun-fu.com</a></div>'
            f'<div>{ADDR}　·　週一～週六 08:00–20:00（週日公休）</div>'
            f'<div style="margin-top:6px">{links}</div></div></footer>')


def parse_md(path: Path):
    raw = path.read_text(encoding="utf-8")
    lines = raw.splitlines()
    h1 = next((l[2:].strip() for l in lines if l.startswith("# ")), path.stem)
    m_title = re.search(r"SEO\s*標題[*\s]*[：:]\s*(.+)", raw)
    m_desc = re.search(r"Meta\s*Description[*\s]*[：:]\s*(.+)", raw)
    seo_title = (m_title.group(1).strip() if m_title else h1).replace("**", "").strip()
    meta_desc = (m_desc.group(1).strip() if m_desc else "").replace("**", "").strip()
    body_lines = []
    for l in lines:
        if l.startswith("# "):
            continue
        if l.lstrip().startswith(">") and any(k in l for k in ("SEO 標題", "Meta Description", "分類")):
            continue
        body_lines.append(l)
    while body_lines and (body_lines[0].strip() == "" or body_lines[0].strip() == "---"):
        body_lines.pop(0)
    body_md = "\n".join(body_lines)
    body_html = markdown.markdown(body_md, extensions=["tables", "fenced_code", "sane_lists", "md_in_html"])
    body_html = body_html.replace("<table>", '<div class="table-scroll"><table>').replace("</table>", "</table></div>")
    if not meta_desc:
        txt = re.sub(r"<[^>]+>", "", body_html)
        meta_desc = txt.strip().replace("\n", "")[:70]
    return {"h1": h1, "seo_title": seo_title, "meta_desc": meta_desc, "body": body_html}


def article_page(art, cat_key, slug):
    cat_name, cat_slug, _ = CATS[cat_key]
    desc = html.escape(art["meta_desc"], quote=True)
    title = html.escape(art["seo_title"], quote=True)
    url = f"{BASE}/posts/{slug}.html"
    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}｜{BRAND}</title>
<meta name="description" content="{desc}">
<meta property="og:type" content="article">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:image" content="{BASE}/assets/logo.jpg">
<link rel="icon" href="../assets/logo.jpg">
{FONTS}
<link rel="stylesheet" href="../assets/style.css">
</head>
<body>
{topbar("../")}
<article><div class="wrap">
  <div class="crumb"><a href="../index.html">首頁</a> › <a href="../{cat_slug}.html">{cat_name}</a></div>
  <span class="pill">{cat_name}</span>
  <h1>{html.escape(art['h1'])}</h1>
  <div class="byline">尊福祭祀商行 · 嘉義在地大型儀式供品供應商</div>
  {art['body']}
  {cta_block()}
  <p class="note">本文內容為祭祀供品與民俗禮儀的參考介紹，實際品項、尺寸與價格依現場需求與商行報價為準。供品準備重在誠敬之心，各地習俗或有不同，建議依在地禮俗與宮廟指示辦理。</p>
</div></article>
{footer()}
</body>
</html>
"""


def card(art, slug, prefix="posts/"):
    desc = html.escape(art["meta_desc"][:60])
    return (f'<a class="card" href="{prefix}{slug}.html">'
            f'<div class="ct">{art["_cat_name"]}</div>'
            f'<div class="ch">{html.escape(art["h1"])}</div>'
            f'<div class="cd">{desc}…</div></a>')


def page_shell(title, desc, body, prefix=""):
    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc, quote=True)}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc, quote=True)}">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:image" content="{BASE}/assets/logo.jpg">
<link rel="icon" href="{prefix}assets/logo.jpg">
{FONTS}
<link rel="stylesheet" href="{prefix}assets/style.css">
</head>
<body>
{topbar(prefix)}
{body}
{footer()}
</body>
</html>
"""


def main():
    by_cat = {c: [] for c in CAT_ORDER}
    total = 0
    for md in sorted(SRC.glob("*.md")):
        cat_key = FILE_CAT.get(md.stem)
        if not cat_key:
            print(f"  [警告] 無分類對應，跳過: {md.stem}")
            continue
        art = parse_md(md)
        art["_cat_name"] = CATS[cat_key][0]
        art["_slug"] = md.stem
        (ROOT / "posts" / f"{md.stem}.html").write_text(article_page(art, cat_key, md.stem), encoding="utf-8")
        by_cat[cat_key].append(art)
        total += 1
    print(f"  → 已生成 {total} 篇文章頁")

    # 首頁
    secs = []
    for cat_key in CAT_ORDER:
        name, cslug, sub = CATS[cat_key]
        if not by_cat[cat_key]:
            continue
        cards = "".join(card(a, a["_slug"]) for a in by_cat[cat_key])
        secs.append(f'<div class="section-title"><span class="bar"></span>{name}'
                    f'<a href="{cslug}.html" style="font-size:14px;font-weight:500;margin-left:auto">看全部 →</a></div>'
                    f'<div class="section-sub">{sub}</div><div class="cards">{cards}</div>')
    hero = (f'<div class="hero"><div class="wrap">'
            f'<img src="assets/logo.jpg" alt="尊福祭祀商行" style="height:96px;width:auto;margin-bottom:14px">'
            f'<h1>{BRAND}</h1><div class="sub">{TAGLINE}</div>'
            f'<p>{SITE_DESC}</p></div></div>')
    home_body = hero + '<div class="wrap">' + "".join(secs) + cta_block() + '</div>'
    (ROOT / "index.html").write_text(page_shell(f"{BRAND}｜{TAGLINE}", SITE_DESC, home_body, prefix=""), encoding="utf-8")

    # 分類索引頁
    n = 0
    for cat_key in CAT_ORDER:
        name, cslug, sub = CATS[cat_key]
        if not by_cat[cat_key]:
            continue
        cards = "".join(card(a, a["_slug"]) for a in by_cat[cat_key])
        hero = f'<div class="hero"><div class="wrap"><h1>{name}</h1><p>{sub}</p></div></div>'
        body = hero + f'<div class="wrap"><div class="cards" style="margin-top:36px">{cards}</div>' + cta_block() + '</div>'
        (ROOT / f"{cslug}.html").write_text(
            page_shell(f"{name}｜{BRAND}", f"{name} — {sub}。{BRAND}", body, prefix=""), encoding="utf-8")
        n += 1
    print(f"  → 已生成 首頁 + {n} 個分類索引頁")
    print("完成。")


if __name__ == "__main__":
    main()
