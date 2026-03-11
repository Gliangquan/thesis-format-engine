from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, File, Request, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from thesis_format_engine.core.parser import DocxParser
from thesis_format_engine.detector.engine import DetectionEngine
from thesis_format_engine.patcher.engine import PatchEngine
from thesis_format_engine.rules.loader import RuleLoader

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "output"
DEMO_DIR = BASE_DIR / "demo"
TEMPLATES = Jinja2Templates(directory=str(BASE_DIR / "templates"))

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
DEMO_DIR.mkdir(parents=True, exist_ok=True)

DEMO_DOCX_URL = "/demo/demo-paper.docx"
DEMO_RULES_URL = "/demo/demo-rules.yaml"

app = FastAPI(title="Thesis Format Engine Web")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return TEMPLATES.TemplateResponse(request, "index.html", _page_context(None, None))


@app.post("/inspect", response_class=HTMLResponse)
async def inspect(request: Request, docx_file: UploadFile = File(...), rules_file: UploadFile = File(...)):
    try:
        parser = DocxParser()
        loader = RuleLoader()
        detector = DetectionEngine()

        docx_path = await _save_upload(docx_file)
        rules_path = await _save_upload(rules_file)

        nodes = parser.parse(str(docx_path))
        rules = loader.load(str(rules_path))
        issues = detector.compare(nodes, rules)

        result = {
            "mode": "inspect",
            "document": docx_file.filename,
            "rules": rules.name,
            "node_count": len(nodes),
            "issue_count": len(issues),
            "issues": issues,
            "download_url": None,
        }
        return TEMPLATES.TemplateResponse(request, "index.html", _page_context(result, None))
    except Exception as exc:
        return TEMPLATES.TemplateResponse(request, "index.html", _page_context(None, str(exc)))


@app.post("/patch", response_class=HTMLResponse)
async def patch(request: Request, docx_file: UploadFile = File(...), rules_file: UploadFile = File(...)):
    try:
        loader = RuleLoader()
        patcher = PatchEngine()
        parser = DocxParser()
        detector = DetectionEngine()

        docx_path = await _save_upload(docx_file)
        rules_path = await _save_upload(rules_file)
        output_name = f"patched-{uuid4().hex[:8]}.docx"
        output_path = OUTPUT_DIR / output_name

        rules = loader.load(str(rules_path))
        patch_result = patcher.apply(str(docx_path), rules, str(output_path))
        nodes = parser.parse(str(output_path))
        issues = detector.compare(nodes, rules)

        result = {
            "mode": "patch",
            "document": docx_file.filename,
            "rules": rules.name,
            "node_count": len(nodes),
            "issue_count": len(issues),
            "issues": issues,
            "changes": patch_result["changes"],
            "download_url": f"/download/{output_name}",
        }
        return TEMPLATES.TemplateResponse(request, "index.html", _page_context(result, None))
    except Exception as exc:
        return TEMPLATES.TemplateResponse(request, "index.html", _page_context(None, str(exc)))


@app.get("/download/{filename}")
def download(filename: str):
    path = OUTPUT_DIR / filename
    return FileResponse(path, filename=filename, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")


@app.get("/demo/{filename}")
def demo_file(filename: str):
    path = DEMO_DIR / filename
    return FileResponse(path, filename=filename)


async def _save_upload(upload: UploadFile) -> Path:
    suffix = Path(upload.filename or "upload.bin").suffix
    path = UPLOAD_DIR / f"{uuid4().hex}{suffix}"
    content = await upload.read()
    path.write_bytes(content)
    return path


def _page_context(result, error):
    return {
        "result": result,
        "error": error,
        "demo_docx_url": DEMO_DOCX_URL,
        "demo_rules_url": DEMO_RULES_URL,
    }
