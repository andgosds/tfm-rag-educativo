from __future__ import annotations

import argparse
import hashlib
import json
import re
import time
import urllib.request
from collections import defaultdict
from pathlib import Path
from typing import Callable


class GenerationFailure(ValueError):
    """Model contract failure with observed usage (not an accepted answer)."""

    def __init__(self, message: str, usage: dict):
        """Conserva el motivo del fallo de contrato junto con el consumo observado."""
        super().__init__(message)
        self.usage = usage


SAFE_ID = re.compile(r"[A-Za-z0-9_.-]+")
ALLOWED_BEHAVIORS = {"answer", "grounded_correction", "abstain"}
def read_jsonl(path: Path) -> list[dict]:
    """Carga registros JSONL omitiendo líneas vacías."""
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def sha256_file(path: Path) -> str:
    """Calcula la huella SHA-256 de una entrada leyendo por bloques."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def build_messages(question: str, contexts: list[dict]) -> list[dict[str, str]]:
    """Compone las instrucciones RAG y presenta los contextos con sus identificadores exactos."""
    context_text = "\n\n".join(
        f"[{item['chunk_id']}]\n{item['text']}" for item in contexts
    )
    system = (
        "You are an educational assistant in a controlled RAG experiment. "
        "Use only the supplied contexts; do not use outside knowledge. "
        "If the contexts support the question, answer concisely and cite the supporting chunk IDs. "
        "If the question contains a false premise that the contexts contradict, correct the premise and cite the contradiction evidence. "
        "If the contexts are insufficient, answer exactly 'I cannot answer from the supplied contexts.' and use no citations. "
        "Citations must be exact chunk IDs from the supplied contexts. "
        "Use exactly three fields and no other text: "
        "'BEHAVIOR: answer OR grounded_correction OR abstain', then "
        "'ANSWER: one concise answer', then "
        "'CITATIONS: comma-separated chunk IDs, or NONE'."
    )
    user = f"Question:\n{question}\n\nSupplied contexts:\n{context_text}"
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def parse_text_contract(text: str) -> dict:
    """Extrae conducta, respuesta y citas de las dos realizaciones admitidas del contrato."""
    # Realización estricta, con **prosa opcional** entre `BEHAVIOR:` y `ANSWER:`. Algunos
    # modelos emiten un bloque de razonamiento antes del primer campo; no cambia la
    # semántica y los campos `ANSWER` y `CITATIONS` siguen siendo los autoritativos.
    match = re.fullmatch(
        r"\s*BEHAVIOR:\s*(answer|grounded_correction|abstain)\s*\n"
        r"(?:.*?\n)?"
        r"ANSWER:\s*(.*?)\s+CITATIONS:\s*(.*?)\s*",
        text,
        flags=re.DOTALL,
    )
    if match:
        behavior, answer, citation_text = match.groups()
        citations = [] if citation_text.upper() == "NONE" else [
            citation.strip() for citation in citation_text.split(",") if citation.strip()
        ]
        return {"answer": answer.strip(), "behavior": behavior, "citations": citations}

    # Realización alternativa, equivalente en contenido: la conducta se declara igual, pero
    # la respuesta sigue sin marcador `ANSWER:` y las citas van embebidas en el texto como
    # `[identificador]`. Se acepta porque las citas son identificadores exactos y el
    # validador de contenido posterior es idéntico: lo único que cambia es la maquetación.
    alt = re.fullmatch(
        r"\s*BEHAVIOR:\s*(answer|grounded_correction|abstain)\s*\n"
        r"(.*?)\s*",
        text,
        flags=re.DOTALL,
    )
    if alt and "ANSWER:" not in alt.group(2) and "CITATIONS:" not in alt.group(2):
        behavior, body = alt.groups()
        citations = []
        for marker in re.findall(r"\[([^\[\]]+)\]", body):
            for piece in marker.split(","):
                piece = piece.strip()
                if piece and piece.upper() != "NONE":
                    citations.append(piece)
        answer = re.sub(r"\s*\[[^\[\]]+\]", "", body).strip()
        if not answer:
            raise ValueError("generation did not follow the three-field text contract")
        # se conserva el orden de aparición, sin duplicados
        seen: set[str] = set()
        citations = [c for c in citations if not (c in seen or seen.add(c))]
        return {"answer": answer, "behavior": behavior, "citations": citations}

    raise ValueError("generation did not follow the three-field text contract")


def validate_generation_result(result: dict, retrieved_chunk_ids: list[str]) -> dict:
    """Valida campos, conducta y citas contra los fragmentos realmente recuperados."""
    if set(result) != {"answer", "behavior", "citations"}:
        raise ValueError("generation result must contain answer, behavior, and citations")
    if not isinstance(result["answer"], str) or not result["answer"].strip():
        raise ValueError("answer must be a non-empty string")
    if result["behavior"] not in ALLOWED_BEHAVIORS:
        raise ValueError("invalid response behavior")
    if not isinstance(result["citations"], list) or not all(
        isinstance(citation, str) for citation in result["citations"]
    ):
        raise ValueError("citations must be a list of strings")
    retrieved = set(retrieved_chunk_ids)
    if any(citation not in retrieved for citation in result["citations"]):
        raise ValueError("citation outside retrieved contexts")
    if result["behavior"] == "abstain" and result["citations"]:
        raise ValueError("abstention must not contain citations")
    return result


def generate_validated(
    messages: list[dict],
    generator: Callable[[list[dict]], tuple[dict, dict]],
    *,
    retrieved_chunk_ids: list[str],
    max_attempts: int = 2,
) -> tuple[dict, dict]:
    """Reintenta las respuestas inválidas y acumula el consumo de todos los intentos."""
    current_messages = list(messages)
    attempts: list[dict] = []
    last_error: ValueError | None = None
    for attempt in range(1, max_attempts + 1):
        try:
            generated, usage = generator(current_messages)
        except GenerationFailure as exc:
            generated, usage = {}, exc.usage
        attempts.append(usage)
        try:
            if "parse_error" in usage:
                raise ValueError(usage["parse_error"])
            validated = validate_generation_result(generated, retrieved_chunk_ids)
        except ValueError as exc:
            last_error = exc
            if attempt == max_attempts:
                combined_failure = {
                    "generation_attempts": attempt,
                    "raw_generation_attempts": [item.get("raw_generation_text") for item in attempts],
                    "attempt_usage": attempts,
                }
                for key in ("generation_latency_ms", "ollama_total_duration_ns",
                            "ollama_load_duration_ns", "prompt_tokens", "completion_tokens"):
                    values = [item[key] for item in attempts if isinstance(item.get(key), (int, float))]
                    combined_failure[key] = sum(values) if values else None
                raise GenerationFailure(str(exc), combined_failure) from exc
            allowed = ", ".join(retrieved_chunk_ids)
            current_messages = [
                *current_messages,
                {"role": "assistant", "content": usage.get("raw_generation_text", "")},
                {
                    "role": "user",
                    "content": (
                        f"Your previous output was invalid: {exc}. Regenerate all three fields. "
                        f"The only allowed citation IDs are: {allowed}."
                    ),
                },
            ]
            continue

        combined = dict(usage)
        combined["generation_attempts"] = attempt
        combined["raw_generation_attempts"] = [
            item.get("raw_generation_text") for item in attempts
        ]
        for key in (
            "generation_latency_ms",
            "ollama_total_duration_ns",
            "ollama_load_duration_ns",
            "prompt_tokens",
            "completion_tokens",
        ):
            values = [
                item[key]
                for item in attempts
                if isinstance(item.get(key), (int, float))
            ]
            combined[key] = sum(values) if values else None
        return validated, combined
    raise last_error or ValueError("generation failed validation")


def build_reference(golden: dict, resolutions: dict[str, dict]) -> tuple[str | None, str]:
    """Resuelve la referencia y la conducta esperada priorizando la auditoría de premisas."""
    # Si el registro trae ya la conducta esperada y la referencia, prevalecen: son las que
    # derivan de la auditoría humana de premisas (`question_premise_audit_v3`), que no puede
    # reconstruirse a partir de `answerability` solo. El resto de registros conserva la
    # derivación anterior sobre el fichero de resoluciones.
    if golden.get("expected_behavior") is not None and "reference" in golden:
        return golden.get("reference"), golden["expected_behavior"]
    if golden["answerability"] == "answerable":
        return golden["gold_answer"], "answer"
    resolution = resolutions.get(golden["qid"])
    if resolution:
        return resolution["corrective_reference_answer"], resolution["expected_response_behavior"]
    return None, "abstain"


def ollama_generator(
    model: str,
    *,
    seed: int = 20260902,
    endpoint: str = "http://127.0.0.1:11434/api/chat",
    num_ctx: int = 8192,
) -> Callable[[list[dict]], tuple[dict, dict]]:
    """Crea un generador Ollama con parámetros fijos y registro del consumo observado."""
    def generate(messages: list[dict]) -> tuple[dict, dict]:
        """Consulta el modelo y convierte su texto al contrato conservando los fallos de formato."""
        payload = {
            "model": model,
            "messages": messages,
            "stream": False,
            "think": False,
            # `num_ctx` se fija en 8192 para todas las condiciones: el techo por defecto de
            # Ollama (4096) se agotaba con cinco fragmentos largos y dejaba salidas vacías.
            # `num_predict` se mantiene en 300, igual que la campaña v2, para conservar la
            # comparación de latencias.
            "options": {"temperature": 0, "seed": seed, "num_predict": 300, "num_ctx": num_ctx},
            "keep_alive": "30m",
        }
        request = urllib.request.Request(
            endpoint,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        started = time.perf_counter()
        with urllib.request.urlopen(request, timeout=300) as response:
            body = json.loads(response.read().decode("utf-8"))
        elapsed_ms = (time.perf_counter() - started) * 1000
        raw_text = body["message"]["content"]
        usage = {
            "generation_latency_ms": elapsed_ms,
            "ollama_total_duration_ns": body.get("total_duration"),
            "ollama_load_duration_ns": body.get("load_duration"),
            "prompt_tokens": body.get("prompt_eval_count"),
            "completion_tokens": body.get("eval_count"),
            "raw_generation_text": raw_text,
        }
        try:
            result = parse_text_contract(raw_text)
        except ValueError as exc:
            usage["parse_error"] = str(exc)
            raise GenerationFailure(str(exc), usage) from exc
        return result, usage

    return generate


def run_experiment(
    *,
    experiment_id: str,
    retrieval_condition: str,
    retrieval_run_path: Path,
    chunks_path: Path,
    golden_path: Path,
    resolutions_path: Path,
    output_path: Path,
    top_k: int,
    generator: Callable[[list[dict]], tuple[dict, dict]],
    generator_model: str,
    prompt_version: str,
) -> dict:
    """Genera respuestas desde una run congelada y registra por separado aceptaciones y fallos."""
    if not SAFE_ID.fullmatch(experiment_id):
        raise ValueError("experiment_id must contain only letters, digits, '.', '_' or '-'")
    if not SAFE_ID.fullmatch(retrieval_condition):
        raise ValueError("retrieval_condition must contain only letters, digits, '.', '_' or '-'")
    if top_k < 1:
        raise ValueError("top_k must be positive")

    chunks = {row["chunk_id"]: row for row in read_jsonl(chunks_path)}
    golden_rows = read_jsonl(golden_path)
    run_rows = read_jsonl(retrieval_run_path)
    resolution_rows = json.loads(resolutions_path.read_text(encoding="utf-8"))["resolutions"]
    resolutions = {row["qid"]: row for row in resolution_rows}

    rankings: dict[str, list[dict]] = defaultdict(list)
    for row in run_rows:
        rankings[row["qid"]].append(row)
    for rows in rankings.values():
        rows.sort(key=lambda row: (row["rank"], row["chunk_id"]))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    completed: set[str] = set()
    if output_path.exists():
        existing = read_jsonl(output_path)
        if any(row.get("experiment_id") != experiment_id or
               row.get("retrieval_condition") != retrieval_condition for row in existing):
            raise ValueError("existing output belongs to another experiment or condition")
        completed = {row["qid"] for row in existing}

    failure_path = output_path.with_name(output_path.stem + "_failures.jsonl")
    failures = read_jsonl(failure_path) if failure_path.exists() else []
    if any(row.get("experiment_id") != experiment_id or
           row.get("retrieval_condition") != retrieval_condition for row in failures):
        raise ValueError("existing failures belong to another experiment or condition")
    failed = {row["qid"] for row in failures}
    if completed & failed:
        raise ValueError("a unit cannot be both accepted and failed")
    completed |= failed
    # La reanudación conserva también los fallos para no seleccionar solo nuevos éxitos.
    written = 0
    with output_path.open("a", encoding="utf-8") as handle:
        for golden in golden_rows:
            qid = golden["qid"]
            if qid in completed:
                continue
            selected = rankings[qid][:top_k]
            if len(selected) != top_k:
                raise ValueError(f"{qid} has {len(selected)} retrieved contexts; expected {top_k}")
            contexts = [
                {"chunk_id": row["chunk_id"], "text": chunks[row["chunk_id"]]["text"]}
                for row in selected
            ]
            chunk_ids = [item["chunk_id"] for item in contexts]
            messages = build_messages(golden["question"], contexts)
            try:
                generated, usage = generate_validated(
                    messages, generator, retrieved_chunk_ids=chunk_ids, max_attempts=3,
                )
            except GenerationFailure as exc:
                failure = {
                    "experiment_id": experiment_id, "retrieval_condition": retrieval_condition,
                    "qid": qid, "status": "failed", "error": str(exc),
                    "question": golden["question"], "retrieved_chunk_ids": chunk_ids,
                    "retrieved_contexts": [item["text"] for item in contexts],
                    "generator_model": generator_model, "prompt_version": prompt_version,
                    "top_k": top_k, **exc.usage,
                }
                with failure_path.open("a", encoding="utf-8") as failure_handle:
                    failure_handle.write(json.dumps(failure, ensure_ascii=False) + "\n")
                    failure_handle.flush()
                failed.add(qid)
                continue
            reference, expected_behavior = build_reference(golden, resolutions)
            record = {
                "experiment_id": experiment_id,
                "retrieval_condition": retrieval_condition,
                "retrieval_run_id": selected[0].get("run_id"),
                "qid": qid,
                "question": golden["question"],
                "answerability": golden["answerability"],
                "unanswerable_category": golden.get("unanswerable_category"),
                "expected_behavior": expected_behavior,
                "reference": reference,
                "retrieved_chunk_ids": chunk_ids,
                "retrieved_contexts": [item["text"] for item in contexts],
                "response": generated["answer"].strip(),
                "reported_behavior": generated["behavior"],
                "citations": generated["citations"],
                "generator_model": generator_model,
                "prompt_version": prompt_version,
                "top_k": top_k,
                **usage,
            }
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
            handle.flush()
            written += 1

    return {
        "experiment_id": experiment_id,
        "retrieval_condition": retrieval_condition,
        "row_count": len(golden_rows),
        "rows_written": written,
        "accepted_count": len(read_jsonl(output_path)),
        "failed_count": len(failed),
        "top_k": top_k,
        "generator_model": generator_model,
        "prompt_version": prompt_version,
        "input_sha256": {
            "retrieval_run": sha256_file(retrieval_run_path),
            "chunks": sha256_file(chunks_path),
            "golden": sha256_file(golden_path),
            "resolutions": sha256_file(resolutions_path),
        },
    }


def parse_args() -> argparse.Namespace:
    """Recoge las entradas congeladas y los parámetros de generación y salida."""
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="Generate controlled RAG answers from a frozen retrieval run")
    parser.add_argument("--experiment-id", required=True)
    parser.add_argument("--retrieval-condition", required=True)
    parser.add_argument("--retrieval-run", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model", default="qwen3.5:9b")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--prompt-version", default="rag_answer_prompt_v1")
    parser.add_argument("--chunks", type=Path, default=root / "data/processed/chunks_v1.jsonl")
    parser.add_argument("--golden", type=Path, default=root / "data/golden/golden_set_pilot_v1.jsonl")
    parser.add_argument(
        "--resolutions",
        type=Path,
        default=root / "data/golden/answerability_resolutions_v1_22q.json",
    )
    parser.add_argument("--metadata", type=Path)
    return parser.parse_args()


def main() -> None:
    """Ejecuta la generación RAG y guarda sus metadatos de trazabilidad."""
    args = parse_args()
    from output_safety import guard_cli_outputs
    guard_cli_outputs(args, script="run_rag_generation")
    metadata = run_experiment(
        experiment_id=args.experiment_id,
        retrieval_condition=args.retrieval_condition,
        retrieval_run_path=args.retrieval_run,
        chunks_path=args.chunks,
        golden_path=args.golden,
        resolutions_path=args.resolutions,
        output_path=args.output,
        top_k=args.top_k,
        generator=ollama_generator(args.model),
        generator_model=args.model,
        prompt_version=args.prompt_version,
    )
    metadata_path = args.metadata or args.output.with_name(args.output.stem + "_metadata.json")
    metadata_path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    main()
