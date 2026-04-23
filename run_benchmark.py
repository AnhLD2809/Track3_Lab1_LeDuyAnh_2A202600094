from __future__ import annotations
import json, os
from pathlib import Path
import typer
from rich import print

from src.reflexion_lab.reporting import build_report, save_report
from src.reflexion_lab.utils import load_dataset, save_jsonl

app = typer.Typer(add_completion=False)

@app.command()
def main(
    dataset: str = "data/hotpot_mini.json",
    out_dir: str = "outputs/sample_run",
    reflexion_attempts: int = 3,
    use_real_llm: bool = False,
) -> None:
    if use_real_llm:
        os.environ["USE_REAL_LLM"] = "1"
        mode = "real"
    else:
        mode = "mock"

    # Import ở đây để biến môi trường USE_REAL_LLM có tác dụng TRƯỚC KHI module agents được load
    from src.reflexion_lab.agents import ReActAgent, ReflexionAgent
    
    examples = load_dataset(dataset)
    react = ReActAgent()
    reflexion = ReflexionAgent(max_attempts=reflexion_attempts)

    print(f"[cyan]Running ReAct on {len(examples)} examples...[/cyan]")
    react_records = [react.run(ex) for ex in examples]

    print(f"[cyan]Running Reflexion on {len(examples)} examples...[/cyan]")
    reflexion_records = [reflexion.run(ex) for ex in examples]

    all_records = react_records + reflexion_records
    out_path = Path(out_dir)
    save_jsonl(out_path / "react_runs.jsonl", react_records)
    save_jsonl(out_path / "reflexion_runs.jsonl", reflexion_records)

    report = build_report(all_records, dataset_name=Path(dataset).name, mode=mode)
    json_path, md_path = save_report(report, out_path)

    print(f"[green]Saved[/green] {json_path}")
    print(f"[green]Saved[/green] {md_path}")
    print(f"[yellow]Records: {report.meta['num_records']} | Examples in report: {len(report.examples)}[/yellow]")
    print(json.dumps(report.summary, indent=2))

if __name__ == "__main__":
    app()
