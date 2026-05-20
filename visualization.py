import json
import os
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import font_manager

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "sketch" / "Paragraph_1"
OUT_DIR = BASE_DIR / "pics" / "word_prosody"
OUT_DIR.mkdir(parents=True, exist_ok=True)

EXCLUDED = {"<pause>", "start_point", "end_point"}

_CJK_CANDIDATES = [
    "Microsoft YaHei",
    "SimHei",
    "SimSun",
    "KaiTi",
    "Noto Sans CJK SC",
    "Noto Serif CJK SC",
    "WenQuanYi Zen Hei",
    "WenQuanYi Micro Hei",
    "Source Han Sans SC",
]
_available = {f.name for f in font_manager.fontManager.ttflist}
for _name in _CJK_CANDIDATES:
    if _name in _available:
        plt.rcParams["font.sans-serif"] = [_name] + plt.rcParams["font.sans-serif"]
        break
plt.rcParams["axes.unicode_minus"] = False


def _filter(words, *series):
    keep = [i for i, w in enumerate(words) if w not in EXCLUDED]
    filtered_words = [words[i] for i in keep]
    filtered_series = [[s[i] for i in keep] for s in series]
    return filtered_words, filtered_series


FIG_SIZE = (10.0, 3.6)
FIG_DPI = 150


def _plot_series(words, values, out_path: Path, label: str = None, color: str = None, marker: str = None) -> None:
    x = list(range(len(words)))
    fig, ax = plt.subplots(figsize=FIG_SIZE)

    ax.plot(x, values, marker=marker, linewidth=1.8, label=label if label else None, color=color if color else None)

    ax.set_xticks(x)
    ax.set_xticklabels(words, rotation=45, ha="right")
    ax.set_yticks([0.0, 0.5, 1.0])
    ax.set_yticklabels(["0", "0.5", "1"])
    ax.set_ylim(-0.05, 1.1)
    ax.set_xlim(-0.5, len(words) - 0.5)
    ax.grid(True, axis="y", linestyle="--", alpha=0.4)
    # ax.legend(loc="upper right", frameon=False)

    fig.tight_layout()
    fig.savefig(out_path, dpi=FIG_DPI)
    plt.close(fig)


def plot_one(json_path: Path, out_f0: Path, out_energy: Path) -> None:
    with json_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    words, (f0, energy) = _filter(data["text"], data["f0"], data["energy"])

    _plot_series(words, f0, out_f0, color="#1f77b4", marker="o")
    _plot_series(words, energy, out_energy, color="#d62728", marker="s")


def main() -> None:
    json_paths = sorted(DATA_DIR.glob("*/word_prosody.json"))
    if not json_paths:
        print(f"no word_prosody.json found under {DATA_DIR}")
        return

    for jp in json_paths:
        sample_id = jp.parent.name
        out_f0 = OUT_DIR / f"{sample_id}_f0.png"
        out_energy = OUT_DIR / f"{sample_id}_energy.png"
        plot_one(jp, out_f0, out_energy)
        print(f"saved {out_f0.relative_to(BASE_DIR)}")
        print(f"saved {out_energy.relative_to(BASE_DIR)}")


if __name__ == "__main__":
    main()
