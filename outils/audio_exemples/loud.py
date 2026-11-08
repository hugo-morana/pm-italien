"""Niveau sonore homogène : chaque clip est ramené à -18 LUFS (EBU R128), crête limitée à -1,5 dBFS.
norm_bytes(b) -> octets mp3 normalisés (mêmes fréquence, canaux et débit que la source)."""
import subprocess, tempfile, os, re
T = -18.0; LIM = 0.84   # 0.84 ≈ -1,5 dBFS
def probe(f):
    o = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=sample_rate,channels,bit_rate", "-of", "csv=p=0", f], capture_output=True, text=True).stdout.split("\n")[0].split(",")
    return o[0], o[1], o[2]
def lufs(f):
    e = subprocess.run(["ffmpeg", "-nostats", "-i", f, "-af", "apad=whole_dur=1.5,ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", e)
    return float(m[-1]) if m else None
def norm_file(src, dst):
    sr, ch, br = probe(src); i = lufs(src)
    if i is None or i < -60: g = 0.0
    else: g = max(-6.0, min(18.0, T - i))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-af", f"volume={g:.2f}dB,alimiter=limit={LIM}:level=false:attack=2:release=40",
                    "-ac", ch, "-ar", sr, "-b:a", str(int(br) // 1000) + "k", "-f", "mp3", dst], check=True)
    return i, g
def norm_bytes(b):
    with tempfile.TemporaryDirectory() as d:
        a, z = os.path.join(d, "a.mp3"), os.path.join(d, "z.mp3"); open(a, "wb").write(b); i, g = norm_file(a, z); return open(z, "rb").read(), i, g
