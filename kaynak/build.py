# Sözlük dosyalarını (data/*.json) kaynak/*.txt dosyalarından üretir.
# Kullanım (depo klasöründe):  python3 kaynak/build.py
#
# Satır biçimi:  kelime=türkçe:puan,türkçe:puan|english:puan,english:puan
#   - "|" öncesi: İngilizce kelimenin Türkçe karşılıkları (en olası = 100)
#   - "|" sonrası: Türkçe soru sorulduğunda ayrıca kabul edilecek İngilizce eş anlamlılar
import glob, json, collections, re

def parse(s, drop=(), norm=True):
    best = {}
    for x in s.split(','):
        x = x.strip()
        if not x:
            continue
        t, w = x.rsplit(':', 1)
        t, w = t.strip(), int(w)
        if not t or t.lower() in drop:
            continue
        best[t] = max(best.get(t, 0), w)
    out = sorted(best.items(), key=lambda p: -p[1])
    if norm and out and out[0][1] < 100:        # en olası karşılık her zaman 100
        k = 100 / out[0][1]
        out = [(t, min(100, round(w * k))) for t, w in out]
    return [list(p) for p in out]

levels = sorted({re.match(r'.*/(\w\w)_\d+\.txt$', f).group(1) for f in glob.glob('kaynak/*_*.txt')})
counts = {}
for L in levels:
    W = {}
    for f in sorted(glob.glob(f'kaynak/{L}_*.txt')):
        for line in open(f, encoding='utf-8'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            k, rest = line.split('=', 1)
            tr, en = rest.split('|', 1)
            W[k] = [parse(tr), parse(en, drop=set(k.lower().split('/')), norm=False)]
    # Aynı Türkçe soruya denk gelen diğer İngilizce kelimeler de kabul edilir (ör. büyük -> big, large)
    by_top = collections.defaultdict(list)
    for k, (tr, en) in W.items():
        by_top[tr[0][0]].append(k.split('/')[0])
    for k, (tr, en) in W.items():
        have = {e for e, _ in en} | set(k.split('/'))
        for other in by_top[tr[0][0]]:
            if other not in have:
                en.append([other, 90]); have.add(other)
    open(f'data/{L}.json', 'w', encoding='utf-8').write(
        json.dumps({"v": 2, "w": W}, ensure_ascii=False, separators=(',', ':')))
    counts[L] = len(W)
print(counts)
