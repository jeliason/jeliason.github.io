"""Demo parameter-target inference DAG for the qsp-inference project page.

Reuses ``qsp_inference.audit.plots.plot_inference_dag`` directly: builds a
small set of synthetic SubmodelTarget YAMLs that exercise the chunked-graph
visualization, then renders. No dependency on a private project's submodel
directory.
"""
import shutil
import tempfile
from pathlib import Path

import yaml

from qsp_inference.audit.plots import plot_inference_dag

OUT = Path(__file__).resolve().parent.parent / "assets" / "images" / "qsp-inference-dag.svg"

# Three illustrative chunks. The plotter discovers connected components
# from the parameter <-> target bipartite graph, so simply listing targets
# with their parameter sets is enough.
TARGETS = [
    {"target_id": "pop_PK_clearance",
     "calibration": {"parameters": [{"name": "k_PK"}],
                     "forward_model": {"type": "custom_ode"}}},
    {"target_id": "tissue_distribution",
     "calibration": {"parameters": [{"name": "V_d"}, {"name": "k_PK"}],
                     "forward_model": {"type": "algebraic"}}},
    {"target_id": "IHC_density_PDAC",
     "calibration": {"parameters": [{"name": "q_T_in"}, {"name": "q_T_out"},
                                    {"name": "k_T_prolif"}],
                     "forward_model": {"type": "algebraic"}}},
    {"target_id": "in_vitro_proliferation",
     "calibration": {"parameters": [{"name": "k_T_prolif"}],
                     "forward_model": {"type": "direct_fit"}}},
    {"target_id": "dose_response_Hill",
     "calibration": {"parameters": [{"name": "EC50_IFNg"}, {"name": "n_Hill"}],
                     "forward_model": {"type": "direct_fit"}}},
]

with tempfile.TemporaryDirectory() as td:
    submodel_dir = Path(td) / "submodel"
    submodel_dir.mkdir()
    for t in TARGETS:
        (submodel_dir / f"{t['target_id']}.yaml").write_text(yaml.safe_dump(t))

    out_dir = Path(td) / "out"
    out_dir.mkdir()
    result = plot_inference_dag(submodel_dir, out_dir)
    assert result is not None, "plot_inference_dag returned None"

    OUT.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(out_dir / "inference_dag.svg", OUT)
    print(f"wrote {OUT}")
