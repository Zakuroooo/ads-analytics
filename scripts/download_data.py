"""Download the three public datasets into raw/ using the Kaggle CLI.

Needs a Kaggle token in ~/.kaggle (never committed). Downloads run one at a time.
Usage: python scripts/download_data.py [ipinyou|uplift|attribution ...]
"""
import subprocess
import sys
from pathlib import Path

RAW = Path(__file__).resolve().parent.parent / "raw"
KAGGLE = str(Path(sys.executable).parent / "kaggle")

# iPinYou season 3 (Oct 19-28, 2013): bid, impression, click and conversion logs + README
IPINYOU_DAYS = {
    "bid": range(19, 29),
    "imp": range(19, 28),
    "clk": range(19, 28),
    "conv": range(19, 24),
}


def kaggle(*args):
    print("$ kaggle", " ".join(args), flush=True)
    subprocess.run([KAGGLE, *args], check=True)


def ipinyou():
    out = RAW / "ipinyou"
    out.mkdir(parents=True, exist_ok=True)
    files = ["ipinyou.contest.dataset/README"]
    for kind, days in IPINYOU_DAYS.items():
        files += [f"ipinyou.contest.dataset/training3rd/{kind}.201310{d}.txt.bz2" for d in days]
    for f in files:
        name = Path(f).name
        if (out / name).exists() or (out / f"{name}.zip").exists():
            continue
        kaggle("datasets", "download", "lastsummer/ipinyou", "-f", f, "-p", str(out))


def uplift():
    kaggle("datasets", "download", "arashnic/uplift-modeling", "-p", str(RAW / "uplift"))


def attribution():
    kaggle("datasets", "download", "sharatsachin/criteo-attribution-modeling", "-p", str(RAW / "attribution"))


if __name__ == "__main__":
    jobs = {"ipinyou": ipinyou, "uplift": uplift, "attribution": attribution}
    for name in sys.argv[1:] or jobs:
        jobs[name]()
    print("done", flush=True)
