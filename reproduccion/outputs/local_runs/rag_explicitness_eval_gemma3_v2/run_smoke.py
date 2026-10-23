import asyncio, json, sys
from pathlib import Path
root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(root / "scripts"))
from evaluate_rag import run_evaluation
out = Path(__file__).resolve().parent
async def main():
    for repeat in (1, 2):
        result = await run_evaluation(input_paths=[out / "smoke_input.jsonl"], output_path=out / f"smoke_{repeat}_scores.jsonl", summary_path=out / f"smoke_{repeat}_summary.json", risk_path=out / f"smoke_{repeat}_risk.jsonl", judge_model="gemma3:4b")
        print(json.dumps(result), flush=True)
asyncio.run(main())
