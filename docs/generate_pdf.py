from __future__ import annotations

import re
from urllib.request import urlopen
from pathlib import Path

import markdown
from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = ROOT / "docs"
VENDOR_DIR = DOCS_DIR / "_vendor"
MERMAID_BUNDLE_PATH = VENDOR_DIR / "mermaid.min.js"
MERMAID_BUNDLE_URL = "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"


def maybe_fix_mojibake(text: str) -> str:
    suspects = sum(text.count(token) for token in ("\u00c3", "\u00e2", "\u00c5", "\u00f0"))
    if suspects == 0:
        return text

    try:
        repaired = text.encode("latin-1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return text

    repaired_suspects = sum(
        repaired.count(token) for token in ("\u00c3", "\u00e2", "\u00c5", "\u00f0")
    )
    return repaired if repaired_suspects < suspects else text


def replace_mermaid_blocks(text: str) -> str:
    pattern = re.compile(r"```mermaid\s*\n(.*?)```", flags=re.S)

    def repl(match: re.Match[str]) -> str:
        content = match.group(1).strip()
        return f'\n<div class="mermaid">\n{content}\n</div>\n'

    return pattern.sub(repl, text)


def normalize_markdown(text: str) -> str:
    text = maybe_fix_mojibake(text).replace("\ufeff", "")
    text = text.replace("\r\n", "\n")
    text = replace_mermaid_blocks(text)

    def replace_callout(pattern: str, css_class: str, label: str, source: str) -> str:
        regex = re.compile(
            rf"> \[!{pattern}\]\n((?:> .*(?:\n|$))*)",
            flags=re.M,
        )

        def repl(match: re.Match[str]) -> str:
            body = "\n".join(
                line[2:] for line in match.group(1).splitlines() if line.startswith("> ")
            ).strip()
            return f'<div class="callout {css_class}"><strong>{label}</strong> {body}</div>'

        return regex.sub(repl, source)

    text = replace_callout("NOTE", "note", "Note.", text)
    text = replace_callout("IMPORTANT", "important", "Important.", text)
    text = replace_callout("WARNING", "warning", "Warning.", text)
    return text


def wrap_figures(html: str) -> str:
    pattern = re.compile(r'<p><img alt="([^"]*)" src="([^"]+)" /></p>')

    def replacer(match: re.Match[str]) -> str:
        alt_text = match.group(1).strip()
        src = match.group(2)
        caption = f"<figcaption>{alt_text}</figcaption>" if alt_text else ""
        return f'<figure><img alt="{alt_text}" src="{src}" />{caption}</figure>'

    return pattern.sub(replacer, html)


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
  @page {{
    size: A4;
    margin: 18mm 16mm 20mm 16mm;
  }}

  :root {{
    --ink: #1f2933;
    --muted: #52606d;
    --line: #d9e2ec;
    --accent: #123b5d;
    --accent-soft: #edf4fb;
    --warning: #7c2d12;
    --warning-bg: #fff4e5;
  }}

  body {{
    font-family: "Segoe UI", "Noto Sans", "DejaVu Sans", Arial, sans-serif;
    color: var(--ink);
    font-size: 11pt;
    line-height: 1.58;
    max-width: 178mm;
    margin: 0 auto;
  }}

  h1, h2, h3 {{
    color: var(--accent);
    page-break-after: avoid;
    break-after: avoid-page;
  }}

  h1 {{
    font-size: 22pt;
    margin: 0 0 12pt;
    border-bottom: 2px solid var(--accent);
    padding-bottom: 8pt;
  }}

  h2 {{
    font-size: 15pt;
    margin-top: 22pt;
    padding-bottom: 4pt;
    border-bottom: 1px solid var(--line);
  }}

  h3 {{
    font-size: 12.5pt;
    margin-top: 16pt;
  }}

  p, li {{
    widows: 3;
    orphans: 3;
  }}

  ul, ol {{
    padding-left: 18pt;
  }}

  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 14pt 0;
    font-size: 10pt;
  }}

  th, td {{
    border: 1px solid var(--line);
    padding: 7pt 8pt;
    vertical-align: top;
  }}

  th {{
    background: var(--accent-soft);
    color: var(--accent);
    font-weight: 700;
  }}

  code {{
    font-family: "Cascadia Code", Consolas, monospace;
    background: #f6f8fa;
    border-radius: 3px;
    padding: 1px 4px;
    font-size: 9.5pt;
  }}

  pre {{
    font-family: "Cascadia Code", Consolas, monospace;
    background: #f6f8fa;
    border: 1px solid var(--line);
    border-radius: 8px;
    padding: 12pt;
    font-size: 8.8pt;
    line-height: 1.45;
    white-space: pre-wrap;
    word-break: break-word;
    overflow-wrap: anywhere;
    page-break-inside: auto;
  }}

  figure {{
    margin: 16pt 0;
    text-align: center;
    page-break-inside: avoid;
    break-inside: avoid-page;
  }}

  img {{
    max-width: 100%;
    max-height: 210mm;
    border: 1px solid var(--line);
    border-radius: 8px;
    box-shadow: 0 8px 20px rgba(15, 23, 42, 0.06);
  }}

  figcaption {{
    margin-top: 6pt;
    font-size: 9.2pt;
    color: var(--muted);
  }}

  blockquote {{
    margin: 12pt 0;
    padding: 10pt 12pt;
    border-left: 4px solid var(--accent);
    background: #f8fbff;
    color: var(--ink);
  }}

  .callout {{
    margin: 14pt 0;
    padding: 10pt 12pt;
    border-radius: 8px;
    border: 1px solid var(--line);
    background: var(--accent-soft);
  }}

  .callout.important {{
    border-color: #b9d6ef;
  }}

  .callout.warning {{
    border-color: #f3c7a5;
    background: var(--warning-bg);
    color: var(--warning);
  }}

  .page-break {{
    page-break-before: always;
    break-before: page;
  }}

  .mermaid {{
    margin: 18pt 0;
    padding: 14pt;
    border: 1px solid var(--line);
    border-radius: 12px;
    background: linear-gradient(180deg, #f8fbff 0%, #ffffff 100%);
    box-shadow: 0 10px 24px rgba(15, 23, 42, 0.06);
    page-break-inside: avoid;
    break-inside: avoid-page;
  }}

  .mermaid svg {{
    max-width: 100%;
    height: auto;
  }}
</style>
<script src="_vendor/mermaid.min.js"></script>
<script>
  window.addEventListener("load", async () => {{
    try {{
      mermaid.initialize({{
        startOnLoad: false,
        securityLevel: "loose",
        theme: "base",
        flowchart: {{
          curve: "basis",
          useMaxWidth: true,
          htmlLabels: true
        }},
        sequence: {{
          useMaxWidth: true,
          wrap: true
        }},
        themeVariables: {{
          primaryColor: "#edf4fb",
          primaryTextColor: "#123b5d",
          primaryBorderColor: "#123b5d",
          lineColor: "#52606d",
          secondaryColor: "#f8fbff",
          tertiaryColor: "#ffffff",
          clusterBkg: "#f6f9fc",
          clusterBorder: "#9fb3c8",
          fontFamily: "Segoe UI, Noto Sans, DejaVu Sans, Arial, sans-serif"
        }}
      }});

      const nodes = document.querySelectorAll(".mermaid");
      if (nodes.length > 0) {{
        await mermaid.run({{ nodes }});
      }}
      document.body.dataset.mermaidReady = "done";
    }} catch (error) {{
      document.body.dataset.mermaidReady = "error";
      document.body.dataset.mermaidError = error?.message || String(error);
    }}
  }});
</script>
</head>
<body>
{html}
</body>
</html>
"""


def resolve_edge_path() -> Path:
    candidates = [
        Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
        Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError("Microsoft Edge was not found for PDF generation.")


def ensure_mermaid_bundle() -> None:
    if MERMAID_BUNDLE_PATH.exists():
        return

    VENDOR_DIR.mkdir(parents=True, exist_ok=True)
    with urlopen(MERMAID_BUNDLE_URL, timeout=60) as response:
        MERMAID_BUNDLE_PATH.write_bytes(response.read())


def render_html(md_path: Path) -> str:
    text = normalize_markdown(md_path.read_text(encoding="utf-8"))
    html = markdown.markdown(
        text,
        extensions=["fenced_code", "tables", "sane_lists"],
    )
    html = wrap_figures(html)
    return HTML_TEMPLATE.format(title=md_path.stem, html=html)


def generate_pdf(md_path: Path, pdf_path: Path) -> None:
    ensure_mermaid_bundle()
    html_path = md_path.with_suffix(".html")
    html_path.write_text(render_html(md_path), encoding="utf-8")

    resolve_edge_path()

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            channel="msedge",
            headless=True,
            args=["--allow-file-access-from-files"],
        )
        page = browser.new_page()
        page.goto(html_path.resolve().as_uri(), wait_until="load")
        page.wait_for_function(
            """
            () => {
              const status = document.body.dataset.mermaidReady;
              return status === "done" || status === "error";
            }
            """,
            timeout=60000,
        )
        mermaid_status = page.evaluate("document.body.dataset.mermaidReady")
        if mermaid_status == "error":
            mermaid_error = page.evaluate("document.body.dataset.mermaidError || ''")
            browser.close()
            raise RuntimeError(
                f"Mermaid rendering failed for {md_path.name}: {mermaid_error}"
            )

        page.wait_for_timeout(1200)
        page.emulate_media(media="screen")
        page.pdf(
            path=str(pdf_path.resolve()),
            format="A4",
            print_background=True,
            margin={
                "top": "18mm",
                "right": "16mm",
                "bottom": "20mm",
                "left": "16mm",
            },
        )
        browser.close()

    html_path.unlink(missing_ok=True)
    print(f"PDF created: {pdf_path}")


def iter_markdown_documents() -> list[Path]:
    return sorted(DOCS_DIR.glob("*.md"))


def main() -> None:
    documents = iter_markdown_documents()
    if not documents:
        print("No Markdown documents were found in docs/.")
        return

    for md_path in documents:
        generate_pdf(md_path, md_path.with_suffix(".pdf"))


if __name__ == "__main__":
    main()
