"""config.py - central configuration."""
import os
import json

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

# --- Data source ---
DATA_DIR = os.environ.get(
    "SSS_DATA_DIR",
    r"S:\Duncan-Williams\FSG_2\Financial Services Group\SpreadSheets\BankAndCU_DataPulls\Full Bank Analysis",
)
FILENAME_PREFIX = "FullBankAnalysis_"
HEADER_ROW = 1
BANK_NAME_COLUMN = "Company Name"
SHEET_NAME = 0
STRICT_SCHEMA = False
CACHE_ENABLED = True

# --- Sales-rep assignment file (read in-place; join on SNL ID) ---
# Fixed filename on the share. UNA (or missing) = Unassigned (shown, flagged).
REP_FILE = os.environ.get(
    "SSS_REP_FILE",
    r"\\scbandt.com\shares\ISData\Duncan-Williams\FSG_2\Financial Services Group\SpreadSheets\BankAndCU_DataPulls\MidYearReview 2026\BankAssignments_KAS_2026.08.06.xlsx",
)

# --- LLM provider ---
LLM_PROVIDER = os.environ.get("LLM_PROVIDER", "off").strip().lower()
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
ANTHROPIC_MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-5")
AZURE_OPENAI_ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.environ.get("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_DEPLOYMENT = os.environ.get("AZURE_OPENAI_DEPLOYMENT")
AZURE_OPENAI_API_VERSION = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-06-01")
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.1")


def provider_available(name):
    name = (name or "").lower()
    if name == "anthropic": return bool(ANTHROPIC_API_KEY)
    if name == "azure": return bool(AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY and AZURE_OPENAI_DEPLOYMENT)
    if name == "openai": return bool(OPENAI_BASE_URL and OPENAI_API_KEY)
    if name == "ollama": return bool(OLLAMA_BASE_URL)
    return False


AI_ENABLED = LLM_PROVIDER not in ("off",) and (
    (LLM_PROVIDER == "auto" and any(provider_available(p) for p in ("anthropic","azure","openai","ollama")))
    or provider_available(LLM_PROVIDER))

# --- User settings (settings.json, live) ---
import fields as _fields

SETTINGS_PATH = os.path.join(os.path.dirname(__file__), "settings.json")
SETTINGS_DEFAULTS = {
    "MATERIALITY_PERCENTILE": 70, "NARRATIVE_TONE": "conversational",
    "PDF_INCLUDE_TREND": True, "PDF_TREND_QUARTERS": 5,
    "SIGNAL_C_REWARD_DECLINE": True, "SIGNAL_WEIGHTS": {"A": 1/3, "B": 1/3, "C": 1/3},
    "SNAPSHOT_FIELDS": list(_fields.DEFAULT_SNAPSHOT), "TREND_FIELDS": list(_fields.DEFAULT_TREND),
    "PROMPT_LIBRARY": {"conversational": {}, "analyst": {}},
    "ACTIVE_PROMPT": {"conversational": "Default", "analyst": "Default"},
    "PDF_SHOW_REP": True,
}
_OVERRIDABLE = set(SETTINGS_DEFAULTS.keys())


def load_settings():
    vals = dict(SETTINGS_DEFAULTS)
    try:
        with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
            saved = json.load(f)
        if isinstance(saved, dict):
            vals.update({k: saved[k] for k in saved if k in vals})
    except Exception:
        pass
    w = vals.get("SIGNAL_WEIGHTS") or {}
    try:
        s = float(w.get("A",0))+float(w.get("B",0))+float(w.get("C",0))
        if s > 0: vals["SIGNAL_WEIGHTS"] = {k: float(w.get(k,0))/s for k in ("A","B","C")}
    except Exception:
        vals["SIGNAL_WEIGHTS"] = dict(SETTINGS_DEFAULTS["SIGNAL_WEIGHTS"])
    vals["SNAPSHOT_FIELDS"] = _fields.sanitize(vals.get("SNAPSHOT_FIELDS"), _fields.DEFAULT_SNAPSHOT)
    vals["TREND_FIELDS"] = _fields.sanitize(vals.get("TREND_FIELDS"), _fields.DEFAULT_TREND)[:_fields.TREND_MAX]
    lib = vals.get("PROMPT_LIBRARY") or {}
    vals["PROMPT_LIBRARY"] = {"conversational": dict(lib.get("conversational") or {}), "analyst": dict(lib.get("analyst") or {})}
    act = vals.get("ACTIVE_PROMPT") or {}
    vals["ACTIVE_PROMPT"] = {"conversational": act.get("conversational","Default"), "analyst": act.get("analyst","Default")}
    for v in ("conversational","analyst"):
        if vals["ACTIVE_PROMPT"][v] != "Default" and vals["ACTIVE_PROMPT"][v] not in vals["PROMPT_LIBRARY"][v]:
            vals["ACTIVE_PROMPT"][v] = "Default"
    return vals


def save_settings(new_values):
    cur = load_settings()
    for k, v in (new_values or {}).items():
        if k in _OVERRIDABLE: cur[k] = v
    with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
        json.dump(cur, f, indent=2)
    return cur


def __getattr__(name):
    if name in _OVERRIDABLE:
        return load_settings()[name]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
