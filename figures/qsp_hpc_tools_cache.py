"""Three-tier cache flow diagram for the qsp-hpc-tools project page.

A request walks down the tiers; each fall-through arrow is labeled with
what causes the miss. Standalone graphviz render — no project data
required.
"""
from pathlib import Path

import graphviz

OUT = Path(__file__).resolve().parent.parent / "assets" / "images" / "qsp-hpc-tools-cache"

LOCAL_FILL = "#3b5070"
HPC_FILL = "#5a6783"
SOURCE_FILL = "#c47a3b"
HIT_COLOR = "#2f7d4f"
MISS_COLOR = "#666666"

g = graphviz.Digraph("cache_flow", format="svg")
g.attr(
    rankdir="TB",
    bgcolor="white",
    fontname="Helvetica",
    fontsize="11",
    nodesep="0.25",
    ranksep="0.6",
    pad="0.2",
)
g.attr("node", fontname="Helvetica", fontsize="10", margin="0.18,0.10")
g.attr("edge", fontname="Helvetica", fontsize="9")


def tier(name, label, fill, sub):
    g.node(
        name,
        label=f"<<b>{label}</b><br/><font point-size='9' color='#dddddd'>{sub}</font>>",
        shape="box",
        style="rounded,filled",
        fillcolor=fill,
        color=fill,
        fontcolor="white",
    )


# Entry point
g.node(
    "request",
    label="<<b>Request</b><br/><font point-size='9'>simulate at θ, scenario S; return observable O</font>>",
    shape="box",
    style="rounded,filled",
    fillcolor="#ece8e0",
    color="#cbc6b8",
)

# Tiers
tier("local", "Tier 1 — local pool", LOCAL_FILL, "cached results on this machine")
tier("hpc_obs", "Tier 2 — HPC summary observables", HPC_FILL, "derived values on the cluster")
tier("hpc_sim", "Tier 3 — HPC full simulations", HPC_FILL, "raw trajectories on the cluster")
tier("fresh", "Fresh SLURM array", SOURCE_FILL, "rsync, submit, monitor, derive on cluster")

g.node(
    "result",
    label="<<b>Result</b><br/><font point-size='9'>observable O for θ under S</font>>",
    shape="box",
    style="rounded,filled",
    fillcolor="#ece8e0",
    color="#cbc6b8",
)

# Hit edges (right side, green)
for src in ["local", "hpc_obs", "hpc_sim", "fresh"]:
    g.edge(src, "result", label=" hit ", color=HIT_COLOR, fontcolor=HIT_COLOR,
           constraint="false")

# Miss / fall-through edges (left side, with reason labels)
g.edge("request", "local", color=MISS_COLOR)
g.edge("local", "hpc_obs",
       label="  not in local cache  ",
       color=MISS_COLOR, fontcolor=MISS_COLOR)
g.edge("hpc_obs", "hpc_sim",
       label="  new observable code  ",
       color=MISS_COLOR, fontcolor=MISS_COLOR)
g.edge("hpc_sim", "fresh",
       label=r"  new θ, model rebuild,\l  or scenario edit  \l",
       color=MISS_COLOR, fontcolor=MISS_COLOR)

OUT.parent.mkdir(parents=True, exist_ok=True)
rendered = g.render(filename=str(OUT), cleanup=True)
print(f"wrote {rendered}")
