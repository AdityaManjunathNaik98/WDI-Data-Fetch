import os
import json
import time
import requests
from datetime import datetime, timezone
from pathlib import Path

# ─────────────────────────────────────────────
# HARDCODED CONFIG
# ─────────────────────────────────────────────
API_URL         = "https://ig.gov-cloud.ai/mac/adhoc-tidb-query"
AUTH_TOKEN      = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICI3Ny1NUVdFRTNHZE5adGlsWU5IYmpsa2dVSkpaWUJWVmN1UmFZdHl5ejFjIn0.eyJleHAiOjE3NzMwODY4MTcsImlhdCI6MTc3MzA1MDgxNywianRpIjoiOTU5OThkNmMtMWY5Mi00MGQ1LTllODMtNjY0NDczMDFkNGJkIiwiaXNzIjoiaHR0cDovL2tleWNsb2FrLXNlcnZpY2Uua2V5Y2xvYWsuc3ZjLmNsdXN0ZXIubG9jYWw6ODA4MC9yZWFsbXMvbWFzdGVyIiwiYXVkIjpbIkJPTFRaTUFOTl9CT1RfbW9iaXVzIiwiYWNjb3VudCJdLCJzdWIiOiJmNzFmMzU5My1hNjdhLTQwYmMtYTExYS05YTQ0NjY4YjQxMGQiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJIT0xBQ1JBQ1lfbW9iaXVzIiwic2lkIjoiZWExNGVkMjktZGE5NC00NWEwLWEzMWYtZjk5Njk4ODc0N2M2IiwiYWNyIjoiMSIsImFsbG93ZWQtb3JpZ2lucyI6WyIvKiJdLCJyZXNvdXJjZV9hY2Nlc3MiOnsiSE9MQUNSQUNZX21vYml1cyI6eyJyb2xlcyI6WyJORUdPVEFUSU9OX0FQUFJPVkUiLCJQUk9EVUNUX0NSRUFUSU9OX1JFQUQiLCJBTExJQU5DRV9XUklURSIsIkFMTElBTkNFX0VYRUNVVEUiLCJURU5BTlRfV1JJVEUiLCJQTEFURk9STV9XUklURSIsIlJBVEVfQ0FSRF9XUklURSIsIkhPTEFDUkFDWV9VU0VSIiwiUkFURV9DQVJEX0FQUFJPVkUiLCJBTExJQU5DRV9BUFBST1ZFIiwiTkVHT1RBVElPTl9XUklURSIsIlRFTkFOVF9FWEVDVVRFIiwiUFJPRFVDVF9MSVNUSU5HX0FQUFJPVkUiLCJQUk9EVUNUX0xJU1RJTkdfRVhFQ1VURSIsIlNVQl9BTExJQU5DRV9XUklURSIsIlBST0RVQ1RfQ1JFQVRJT05fRVhFQ1VURSIsIk5FR09UQVRJT05fRVhFQ1VURSIsIlBST0RVQ1RfTElTVElOR19XUklURSIsIlBST0RVQ1RfQ1JFQVRJT05fQVBQUk9WRSIsIlNVUEVSQURNSU4iLCJQUk9EVUNUX0NSRUFUSU9OX1dSSVRFIiwiUFJPRFVDVF9MSVNUSU5HX1JFQUQiLCJBTExJQU5DRV9SRUFEIiwiUkFURV9DQVJEX0VYRUNVVEUiLCJTVUJfQUxMSUFOQ0VfUkVBRCIsIlRFTkFOVF9BUFBST1ZFIiwiQUdFTlRTX1JFQUQiLCJEQU9fQ1JFQVRFIiwiUExBVEZPUk1fUkVBRCIsIlRFTkFOVF9SRUFEIiwiUExBVEZPUk1fRVhFQ1VURSIsIlNVQl9BTExJQU5DRV9FWEVDVVRFIiwiU1VCX0FMTElBTkNFX0FQUFJPVkUiLCJORUdPVEFUSU9OX1JFQUQiLCJQUk9QT1NBTF9DUkVBVEUiLCJSQVRFX0NBUkRfUkVBRCIsIlBMQVRGT1JNX0FQUFJPVkUiXX0sIkJPTFRaTUFOTl9CT1RfbW9iaXVzIjp7InJvbGVzIjpbIkJPTFRaTUFOTl9CT1RfVVNFUiJdfSwiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJwcm9maWxlIGVtYWlsIiwicmVxdWVzdGVyVHlwZSI6IlRFTkFOVCIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJuYW1lIjoia3NhbXhwIGtzYW14cCIsInRlbmFudElkIjoiZjcxZjM1OTMtYTY3YS00MGJjLWExMWEtOWE0NDY2OGI0MTBkIiwicGxhdGZvcm1JZCI6Im1vYml1cyIsInByZWZlcnJlZF91c2VybmFtZSI6InBhc3N3b3JkX3RlbmFudF9rc2FteHBAbW9iaXVzZHRhYXMuYWkiLCJnaXZlbl9uYW1lIjoia3NhbXhwIiwiZmFtaWx5X25hbWUiOiJrc2FteHAiLCJlbWFpbCI6InBhc3N3b3JkX3RlbmFudF9rc2FteHBAbW9iaXVzZHRhYXMuYWkifQ.FN1z0P7IPjkZLdTLs9v2oBTYDq35IvSyPyTGJtbYQGnsioIinfnz2mRGTy7WxpTfLNtOzbpwI9MPNYV0jv6t2DFz_XiIciGPglI1B945c409TsF-o2J_KzmAxQy0m6zNH48O8csnmuua3jfFi3FMVoZvC-uJsLmR_0vIx-TH3MCiluynv7ZGiQNmkSArbFVZu1fEqbU3Ib1C7wc9s49O6gkQGL66vaoHiwf_3Xcq6E2sJgDX5WGePYYgi1x44vUiFUCIxiAEPltaPkvmAH7hSQ0Ho_gm9G6gepruGSc_fSWcYCP3CCy6XqRX_Uv4dWNueBG9fg0tLlfbfdUzab3fCw"
TABLE_NAME      = "t_68c16c9033b961627a6b7cea_t"
BATCH_SIZE      = 5000
OUTPUT_FILE     = "output_data.json"
CHECKPOINT_FILE = "checkpoint.json"
MAX_RETRIES     = 5
RETRY_DELAY     = 10    # seconds (multiplied by attempt number for back-off)
REQUEST_TIMEOUT = 120   # seconds

HEADERS = {
    "accept":        "application/json",
    "Content-Type":  "application/json",
    "Authorization": f"Bearer {AUTH_TOKEN}",
}

# ─────────────────────────────────────────────
# STRUCTURED JSON LOGGER  (Kubernetes-friendly)
# ─────────────────────────────────────────────
def log(level: str, message: str, **extra):
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "level":     level,
        "message":   message,
        **extra
    }
    print(json.dumps(record), flush=True)


# ─────────────────────────────────────────────
# CHECKPOINT
# ─────────────────────────────────────────────
def load_checkpoint() -> dict:
    if Path(CHECKPOINT_FILE).exists():
        with open(CHECKPOINT_FILE) as f:
            ckpt = json.load(f)
        log("INFO", "Resuming from checkpoint",
            offset=ckpt["offset"], total_fetched=ckpt["total_fetched"])
        return ckpt
    return {"offset": 0, "total_fetched": 0, "batches_done": 0}


def save_checkpoint(offset: int, total_fetched: int, batches_done: int):
    with open(CHECKPOINT_FILE, "w") as f:
        json.dump({
            "offset":        offset,
            "total_fetched": total_fetched,
            "batches_done":  batches_done,
            "saved_at":      datetime.now(timezone.utc).isoformat()
        }, f)


def clear_checkpoint():
    if Path(CHECKPOINT_FILE).exists():
        os.remove(CHECKPOINT_FILE)


# ─────────────────────────────────────────────
# API CALL WITH RETRY
# ─────────────────────────────────────────────
def query_api(sql: str) -> list:
    """
    POST a SQL query and return the list of row dicts.
    Expected response: {"status": "success", "data": [...]}
    """
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.post(
                API_URL,
                headers=HEADERS,
                json={"query": sql},
                timeout=REQUEST_TIMEOUT
            )

            if resp.status_code != 200:
                raise RuntimeError(f"HTTP {resp.status_code} — {resp.text[:400]}")

            body = resp.json()

            # Parse {"status": "success", "data": [...]}
            if isinstance(body, dict):
                status = body.get("status", "success")
                if status != "success":
                    raise RuntimeError(f"API status='{status}': {body}")
                rows = body.get("data", [])
            elif isinstance(body, list):
                rows = body
            else:
                rows = []

            return rows

        except Exception as exc:
            log("ERROR", "API call failed",
                attempt=attempt, max_retries=MAX_RETRIES,
                error=str(exc), sql=sql[:120])
            if attempt < MAX_RETRIES:
                wait = RETRY_DELAY * attempt   # exponential back-off
                log("INFO", f"Retrying in {wait}s", next_attempt=attempt + 1)
                time.sleep(wait)
            else:
                raise RuntimeError(
                    f"All {MAX_RETRIES} retries exhausted. Last error: {exc}"
                ) from exc


def get_total_count() -> int:
    try:
        rows = query_api(f"SELECT COUNT(*) as cnt FROM {TABLE_NAME}")
        if rows:
            first = rows[0]
            # handle different casing returned by DB
            cnt = (first.get("cnt")
                   or first.get("COUNT(*)")
                   or first.get("count(*)")
                   or 0)
            return int(cnt)
    except Exception as e:
        log("WARNING", "COUNT query failed — will stop on empty batch", error=str(e))
    return -1


# ─────────────────────────────────────────────
# OUTPUT — JSON Lines during run, then convert
# ─────────────────────────────────────────────
def write_batch(rows: list, is_first_batch: bool):
    """Append rows as JSON Lines (one object per line) — safe for resume."""
    mode = "w" if is_first_batch else "a"
    with open(OUTPUT_FILE, mode) as f:
        for row in rows:
            f.write(json.dumps(row) + "\n")


def finalise_output(total_fetched: int):
    """Convert JSON Lines file → proper JSON array."""
    tmp = OUTPUT_FILE + ".tmp"
    os.rename(OUTPUT_FILE, tmp)
    log("INFO", "Converting JSONL → JSON array…", total_records=total_fetched)
    with open(tmp, "r") as inp, open(OUTPUT_FILE, "w") as out:
        out.write("[\n")
        first = True
        for line in inp:
            line = line.strip()
            if not line:
                continue
            if not first:
                out.write(",\n")
            out.write(line)
            first = False
        out.write("\n]\n")
    os.remove(tmp)
    log("INFO", "Output file ready", output_file=OUTPUT_FILE)


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    log("INFO", "=== TiDB Extraction Started ===",
        table=TABLE_NAME, batch_size=BATCH_SIZE, output_file=OUTPUT_FILE)

    total_count = get_total_count()
    if total_count >= 0:
        log("INFO", "Table row count",
            total_count=total_count,
            estimated_batches=max(1, -(-total_count // BATCH_SIZE)))

    ckpt          = load_checkpoint()
    offset        = ckpt["offset"]
    total_fetched = ckpt["total_fetched"]
    batches_done  = ckpt["batches_done"]
    is_first      = (offset == 0)

    # If resuming but output file was lost, restart cleanly
    if offset > 0 and not Path(OUTPUT_FILE).exists():
        log("WARNING", "Checkpoint exists but output file missing — restarting from 0")
        offset = 0; total_fetched = 0; batches_done = 0; is_first = True

    start_time = time.time()

    try:
        while True:
            sql = (f"SELECT series, yearCode, id, economy, value, aggregate FROM {TABLE_NAME} "
                   f"LIMIT {BATCH_SIZE} OFFSET {offset}")

            log("INFO", "Fetching batch",
                offset=offset, batch_size=BATCH_SIZE, batches_done=batches_done)

            rows = query_api(sql)

            if not rows:
                log("INFO", "Empty batch received — all records fetched",
                    offset=offset)
                break

            write_batch(rows, is_first_batch=is_first)
            is_first = False

            total_fetched += len(rows)
            batches_done  += 1
            offset        += BATCH_SIZE

            # Persist progress after every successful batch
            save_checkpoint(offset, total_fetched, batches_done)

            elapsed = time.time() - start_time
            rate    = total_fetched / elapsed if elapsed > 0 else 0
            pct     = (f"{total_fetched / total_count * 100:.1f}%"
                       if total_count > 0 else "?")

            log("INFO", "Batch complete",
                batches_done=batches_done,
                rows_this_batch=len(rows),
                total_fetched=total_fetched,
                progress=pct,
                rows_per_sec=round(rate, 1),
                elapsed_sec=round(elapsed, 1))

            # Partial batch → we're on the last page
            if len(rows) < BATCH_SIZE:
                log("INFO", "Partial batch — this was the last page")
                break

    except Exception as exc:
        log("ERROR",
            "Extraction failed — checkpoint saved. Re-run the script to resume.",
            error=str(exc),
            last_offset=offset,
            total_fetched_so_far=total_fetched)
        raise SystemExit(1)

    # Wrap up
    finalise_output(total_fetched)
    clear_checkpoint()

    elapsed = time.time() - start_time
    log("INFO", "=== Extraction Complete ===",
        total_records=total_fetched,
        total_batches=batches_done,
        output_file=OUTPUT_FILE,
        elapsed_sec=round(elapsed, 1))


if __name__ == "__main__":
    main()