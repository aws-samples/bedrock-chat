"""
Document generation tools: DOCX, PPTX, XLSX, and chart (PNG) output.

All documents are uploaded to S3 (DOCUMENT_BUCKET) under agent-workspace/
and returned as a presigned URL valid for 1 hour.

Ported from aws-samples/sample-aws-idp-pipeline .skills/ definitions,
adapted to run as native Strands tools without code_interpreter/AgentCore.
"""

from __future__ import annotations

import io
import json
import logging
import os
import re
import textwrap
import uuid
from datetime import datetime
from typing import Any

import boto3
from app.repositories.models.custom_bot import BotModel
from strands import tool
from strands.types.tools import AgentTool as StrandsAgentTool

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

DOCUMENT_BUCKET = os.environ.get("DOCUMENT_BUCKET", "")
REGION = os.environ.get("REGION", "us-east-1")
WORKSPACE_PREFIX = "agent-workspace"


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------


def _s3_client():
    return boto3.client("s3", region_name=REGION)


def _upload_and_presign(
    data: bytes,
    filename: str,
    content_type: str,
    presign_expiry: int = 3600,
) -> str:
    """Upload bytes to S3 and return a 1-hour presigned download URL."""
    datestamp = datetime.utcnow().strftime("%Y/%m/%d")
    artifact_id = str(uuid.uuid4())
    key = f"{WORKSPACE_PREFIX}/documents/{datestamp}/{artifact_id}/{filename}"

    s3 = _s3_client()
    s3.put_object(
        Bucket=DOCUMENT_BUCKET,
        Key=key,
        Body=data,
        ContentType=content_type,
        ContentDisposition=f'attachment; filename="{filename}"',
    )
    logger.info(f"[DOC_GEN] Uploaded {filename} → s3://{DOCUMENT_BUCKET}/{key}")

    url = s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": DOCUMENT_BUCKET, "Key": key},
        ExpiresIn=presign_expiry,
    )
    return url


def _parse_json_arg(value: str | list | dict, default: Any = None) -> Any:
    """Accept either a JSON string or a Python object; return parsed value."""
    if isinstance(value, (list, dict)):
        return value
    if isinstance(value, str):
        try:
            return json.loads(value)
        except (json.JSONDecodeError, ValueError):
            pass
    return default


# ---------------------------------------------------------------------------
# DOCX tool
# ---------------------------------------------------------------------------


def create_docx_tool(bot: BotModel | None = None) -> StrandsAgentTool:
    @tool
    def generate_docx(
        filename: str,
        content: str,
        title: str = "",
    ) -> str:
        """
        Generate a Word document (.docx) from structured Markdown-style content
        and return a presigned download URL (valid 1 hour).

        Supports the following Markdown conventions in `content`:
          - # Heading 1 / ## Heading 2 / ### Heading 3
          - **bold** and *italic* inline formatting
          - Unordered lists starting with "- " or "* "
          - Ordered lists starting with "1. ", "2. " etc.
          - Simple pipe tables: | Col A | Col B |\\n|---|---|\\n| val | val |
          - Blank lines between paragraphs

        Args:
            filename: Output filename, e.g. "report.docx". Must end with .docx.
            content:  Document body as Markdown-style text. The agent should
                      write well-structured content here.
            title:    Optional document title inserted as Heading 1 at the top.

        Returns:
            str: Presigned URL to download the generated document, or an error message.
        """
        if not DOCUMENT_BUCKET:
            return "Error: DOCUMENT_BUCKET environment variable is not set."

        try:
            from docx import Document
            from docx.shared import Pt, RGBColor
            from docx.oxml.ns import qn
        except ImportError:
            return (
                "Error: python-docx is not installed. "
                "Add 'python-docx' to pyproject.toml dependencies."
            )

        if not filename.lower().endswith(".docx"):
            filename = filename + ".docx"

        doc = Document()

        # Optional title as H1
        if title:
            doc.add_heading(title, level=1)

        def _add_run_with_inline(paragraph, text: str):
            """Parse **bold** and *italic* and add runs."""
            # Simple state-machine for ** and *
            pattern = re.compile(r"(\*\*.*?\*\*|\*.*?\*)")
            last = 0
            for m in pattern.finditer(text):
                if m.start() > last:
                    paragraph.add_run(text[last : m.start()])
                raw = m.group()
                if raw.startswith("**"):
                    run = paragraph.add_run(raw[2:-2])
                    run.bold = True
                else:
                    run = paragraph.add_run(raw[1:-1])
                    run.italic = True
                last = m.end()
            if last < len(text):
                paragraph.add_run(text[last:])

        def _is_table_line(line: str) -> bool:
            return line.strip().startswith("|") and line.strip().endswith("|")

        def _add_table(doc, table_lines: list[str]):
            rows = [
                [cell.strip() for cell in line.strip().strip("|").split("|")]
                for line in table_lines
                if not re.match(r"^\s*\|[-:| ]+\|\s*$", line)  # skip separator
            ]
            if not rows:
                return
            col_count = max(len(r) for r in rows)
            table = doc.add_table(rows=len(rows), cols=col_count)
            table.style = "Table Grid"
            for ri, row_data in enumerate(rows):
                for ci, cell_text in enumerate(row_data):
                    if ci < col_count:
                        cell = table.cell(ri, ci)
                        cell.text = cell_text
                        if ri == 0:
                            for run in cell.paragraphs[0].runs:
                                run.bold = True

        lines = content.splitlines()
        i = 0
        while i < len(lines):
            line = lines[i]

            # Headings
            if line.startswith("### "):
                doc.add_heading(line[4:].strip(), level=3)
            elif line.startswith("## "):
                doc.add_heading(line[3:].strip(), level=2)
            elif line.startswith("# "):
                doc.add_heading(line[2:].strip(), level=1)

            # Table block
            elif _is_table_line(line):
                table_lines = []
                while i < len(lines) and _is_table_line(lines[i]):
                    table_lines.append(lines[i])
                    i += 1
                _add_table(doc, table_lines)
                continue

            # Unordered list
            elif re.match(r"^\s*[-*]\s+", line):
                para = doc.add_paragraph(style="List Bullet")
                _add_run_with_inline(para, re.sub(r"^\s*[-*]\s+", "", line))

            # Ordered list
            elif re.match(r"^\s*\d+\.\s+", line):
                para = doc.add_paragraph(style="List Number")
                _add_run_with_inline(para, re.sub(r"^\s*\d+\.\s+", "", line))

            # Blank line → skip
            elif line.strip() == "":
                pass

            # Normal paragraph
            else:
                para = doc.add_paragraph()
                _add_run_with_inline(para, line.strip())

            i += 1

        buf = io.BytesIO()
        doc.save(buf)
        buf.seek(0)

        url = _upload_and_presign(
            buf.read(),
            filename,
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
        return (
            f"Word document '{filename}' generated successfully.\n"
            f"Download (link valid 1 hour):\n{url}"
        )

    return generate_docx


# ---------------------------------------------------------------------------
# PPTX tool
# ---------------------------------------------------------------------------


def create_pptx_tool(bot: BotModel | None = None) -> StrandsAgentTool:
    @tool
    def generate_pptx(
        filename: str,
        title: str,
        slides: str,
    ) -> str:
        """
        Generate a PowerPoint presentation (.pptx) and return a presigned download URL.

        Args:
            filename: Output filename, e.g. "presentation.pptx". Must end with .pptx.
            title:    Presentation title shown on the title slide.
            slides:   JSON array of slide objects. Each object must have:
                        - "title" (str): Slide title
                        - "content" (list[str]): Bullet-point lines for the slide body.
                      Example:
                        [
                          {"title": "Overview", "content": ["Point A", "Point B"]},
                          {"title": "Details",  "content": ["Item 1", "Item 2", "Item 3"]}
                        ]

        Returns:
            str: Presigned URL to download the generated presentation, or an error message.
        """
        if not DOCUMENT_BUCKET:
            return "Error: DOCUMENT_BUCKET environment variable is not set."

        try:
            from pptx import Presentation
            from pptx.util import Inches, Pt
            from pptx.dml.color import RGBColor
        except ImportError:
            return (
                "Error: python-pptx is not installed. "
                "Add 'python-pptx' to pyproject.toml dependencies."
            )

        slides_data = _parse_json_arg(slides, default=[])
        if not slides_data:
            return "Error: 'slides' must be a non-empty JSON array of slide objects."

        prs = Presentation()
        # Use widescreen 16:9
        prs.slide_width = int(10 * 914400)   # 10 inches
        prs.slide_height = int(5.625 * 914400)  # 5.625 inches

        slide_layouts = prs.slide_layouts

        # Title slide
        title_slide_layout = slide_layouts[0]
        slide = prs.slides.add_slide(title_slide_layout)
        slide.shapes.title.text = title
        if slide.placeholders[1]:
            slide.placeholders[1].text = ""

        # Content slides
        content_layout = slide_layouts[1]  # Title and Content
        for slide_def in slides_data:
            s_title = slide_def.get("title", "")
            s_content = slide_def.get("content", [])

            s = prs.slides.add_slide(content_layout)
            s.shapes.title.text = s_title

            tf = s.placeholders[1].text_frame
            tf.clear()
            for idx, bullet in enumerate(s_content):
                if idx == 0:
                    tf.paragraphs[0].text = bullet
                else:
                    p = tf.add_paragraph()
                    p.text = bullet
                    p.level = 0

        buf = io.BytesIO()
        prs.save(buf)
        buf.seek(0)

        if not filename.lower().endswith(".pptx"):
            filename = filename + ".pptx"

        url = _upload_and_presign(
            buf.read(),
            filename,
            "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        )
        return (
            f"PowerPoint presentation '{filename}' generated successfully "
            f"({len(slides_data)} content slides + title slide).\n"
            f"Download (link valid 1 hour):\n{url}"
        )

    return generate_pptx


# ---------------------------------------------------------------------------
# XLSX tool
# ---------------------------------------------------------------------------


def create_xlsx_tool(bot: BotModel | None = None) -> StrandsAgentTool:
    @tool
    def generate_xlsx(
        filename: str,
        sheets: str,
    ) -> str:
        """
        Generate an Excel spreadsheet (.xlsx) and return a presigned download URL.

        Args:
            filename: Output filename, e.g. "data.xlsx". Must end with .xlsx.
            sheets:   JSON array of sheet objects. Each object must have:
                        - "name" (str): Sheet tab name
                        - "headers" (list[str]): Column header labels
                        - "rows" (list[list]): Data rows, each a list of cell values
                      Optionally:
                        - "title" (str): Bold title row inserted above headers
                      Example:
                        [
                          {
                            "name": "Sales",
                            "title": "Q1 Sales Report",
                            "headers": ["Region", "Product", "Revenue"],
                            "rows": [
                              ["North", "Widget A", 12500],
                              ["South", "Widget B", 9800]
                            ]
                          }
                        ]

        Returns:
            str: Presigned URL to download the generated spreadsheet, or an error message.
        """
        if not DOCUMENT_BUCKET:
            return "Error: DOCUMENT_BUCKET environment variable is not set."

        try:
            from openpyxl import Workbook
            from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
        except ImportError:
            return (
                "Error: openpyxl is not installed. "
                "Add 'openpyxl' to pyproject.toml dependencies."
            )

        sheets_data = _parse_json_arg(sheets, default=[])
        if not sheets_data:
            return "Error: 'sheets' must be a non-empty JSON array of sheet objects."

        wb = Workbook()
        wb.remove(wb.active)  # remove default empty sheet

        HEADER_FILL = PatternFill("solid", fgColor="366092")
        TITLE_FONT = Font(bold=True, size=13)
        HEADER_FONT = Font(bold=True, color="FFFFFF")
        HEADER_ALIGN = Alignment(horizontal="center", vertical="center")
        THIN = Side(style="thin", color="CCCCCC")
        CELL_BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

        for sheet_def in sheets_data:
            sheet_name = sheet_def.get("name", "Sheet")[:31]  # Excel max 31 chars
            headers = sheet_def.get("headers", [])
            rows = sheet_def.get("rows", [])
            sheet_title = sheet_def.get("title", "")

            ws = wb.create_sheet(title=sheet_name)
            current_row = 1

            # Optional bold title row
            if sheet_title:
                ws.cell(row=current_row, column=1, value=sheet_title).font = TITLE_FONT
                current_row += 1

            # Header row
            if headers:
                for col_idx, header in enumerate(headers, start=1):
                    cell = ws.cell(row=current_row, column=col_idx, value=header)
                    cell.font = HEADER_FONT
                    cell.fill = HEADER_FILL
                    cell.alignment = HEADER_ALIGN
                    cell.border = CELL_BORDER
                current_row += 1

            # Data rows
            for row_data in rows:
                for col_idx, value in enumerate(row_data, start=1):
                    cell = ws.cell(row=current_row, column=col_idx, value=value)
                    cell.border = CELL_BORDER
                current_row += 1

            # Auto-fit column widths (approximate)
            for col_cells in ws.columns:
                max_len = 0
                col_letter = col_cells[0].column_letter
                for c in col_cells:
                    if c.value is not None:
                        max_len = max(max_len, len(str(c.value)))
                ws.column_dimensions[col_letter].width = min(max_len + 4, 60)

        buf = io.BytesIO()
        wb.save(buf)
        buf.seek(0)

        if not filename.lower().endswith(".xlsx"):
            filename = filename + ".xlsx"

        url = _upload_and_presign(
            buf.read(),
            filename,
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        return (
            f"Excel spreadsheet '{filename}' generated successfully "
            f"({len(sheets_data)} sheet(s)).\n"
            f"Download (link valid 1 hour):\n{url}"
        )

    return generate_xlsx


# ---------------------------------------------------------------------------
# Chart (PNG) tool
# ---------------------------------------------------------------------------


def create_chart_tool(bot: BotModel | None = None) -> StrandsAgentTool:
    @tool
    def generate_chart(
        filename: str,
        chart_type: str,
        title: str,
        labels: str,
        values: str,
        x_label: str = "",
        y_label: str = "",
        colors: str = "",
    ) -> str:
        """
        Generate a data chart as a PNG image and return a presigned download URL.

        Supported chart types: bar, horizontal_bar, line, pie, donut, scatter.

        Args:
            filename:    Output filename, e.g. "sales_chart.png". Must end with .png.
            chart_type:  One of: bar, horizontal_bar, line, pie, donut, scatter.
            title:       Chart title.
            labels:      JSON array of category labels, e.g. ["Jan","Feb","Mar"]
                         For scatter charts: JSON array of x-values.
            values:      JSON array of numeric values, e.g. [120, 95, 140]
                         For multi-series charts: JSON array of arrays,
                         e.g. [{"label":"Series A","data":[1,2,3]},{"label":"Series B","data":[4,5,6]}]
            x_label:     Optional X-axis label (bar, line, scatter only).
            y_label:     Optional Y-axis label (bar, line, scatter only).
            colors:      Optional JSON array of hex color strings, e.g. ["#2196F3","#FF5722"].
                         Falls back to a professional default palette if not provided.

        Returns:
            str: Presigned URL to view/download the chart PNG, or an error message.
        """
        if not DOCUMENT_BUCKET:
            return "Error: DOCUMENT_BUCKET environment variable is not set."

        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
            import matplotlib.patches as mpatches
            import numpy as np
        except ImportError:
            return (
                "Error: matplotlib is not installed. "
                "Add 'matplotlib' to pyproject.toml dependencies."
            )

        VALID_TYPES = {"bar", "horizontal_bar", "line", "pie", "donut", "scatter"}
        chart_type = chart_type.lower().strip()
        if chart_type not in VALID_TYPES:
            return f"Error: chart_type must be one of {sorted(VALID_TYPES)}."

        labels_data = _parse_json_arg(labels, default=[])
        values_data = _parse_json_arg(values, default=[])
        colors_data = _parse_json_arg(colors, default=[])

        if not labels_data:
            return "Error: 'labels' must be a non-empty JSON array."
        if not values_data:
            return "Error: 'values' must be a non-empty JSON array."

        # Default colour palette (professional blue-toned)
        DEFAULT_COLORS = [
            "#2196F3", "#FF5722", "#4CAF50", "#9C27B0",
            "#FF9800", "#00BCD4", "#E91E63", "#607D8B",
        ]
        if not colors_data:
            colors_data = DEFAULT_COLORS

        # Detect multi-series (list of dicts)
        is_multi = isinstance(values_data[0], dict) if values_data else False

        fig, ax = plt.subplots(figsize=(10, 6), dpi=120)
        fig.patch.set_facecolor("#FAFAFA")
        ax.set_facecolor("#FAFAFA")

        if chart_type == "bar":
            if is_multi:
                n_series = len(values_data)
                n_groups = len(labels_data)
                x = np.arange(n_groups)
                bar_width = 0.8 / n_series
                for si, series in enumerate(values_data):
                    offset = (si - n_series / 2 + 0.5) * bar_width
                    color = colors_data[si % len(colors_data)]
                    ax.bar(x + offset, series["data"], bar_width,
                           label=series.get("label", f"Series {si+1}"),
                           color=color, alpha=0.85)
                ax.set_xticks(x)
                ax.set_xticklabels(labels_data)
                ax.legend()
            else:
                clrs = [colors_data[i % len(colors_data)] for i in range(len(labels_data))]
                ax.bar(labels_data, values_data, color=clrs, alpha=0.85)

        elif chart_type == "horizontal_bar":
            clrs = [colors_data[i % len(colors_data)] for i in range(len(labels_data))]
            ax.barh(labels_data, values_data, color=clrs, alpha=0.85)

        elif chart_type == "line":
            if is_multi:
                for si, series in enumerate(values_data):
                    color = colors_data[si % len(colors_data)]
                    ax.plot(labels_data, series["data"], marker="o", color=color,
                            label=series.get("label", f"Series {si+1}"), linewidth=2)
                ax.legend()
            else:
                ax.plot(labels_data, values_data, marker="o",
                        color=colors_data[0], linewidth=2)

        elif chart_type in ("pie", "donut"):
            clrs = [colors_data[i % len(colors_data)] for i in range(len(labels_data))]
            wedge_props = {}
            if chart_type == "donut":
                wedge_props = {"width": 0.5}
            ax.pie(values_data, labels=labels_data, colors=clrs,
                   autopct="%1.1f%%", startangle=140,
                   wedgeprops=wedge_props)
            ax.axis("equal")

        elif chart_type == "scatter":
            ax.scatter(labels_data, values_data,
                       color=colors_data[0], alpha=0.7, s=80)

        ax.set_title(title, fontsize=15, fontweight="bold", pad=12)
        if x_label and chart_type not in ("pie", "donut"):
            ax.set_xlabel(x_label)
        if y_label and chart_type not in ("pie", "donut"):
            ax.set_ylabel(y_label)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        plt.tight_layout()

        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight")
        plt.close(fig)
        buf.seek(0)

        if not filename.lower().endswith(".png"):
            filename = filename + ".png"

        url = _upload_and_presign(buf.read(), filename, "image/png")
        return (
            f"Chart '{filename}' ({chart_type}) generated successfully.\n"
            f"View/download (link valid 1 hour):\n{url}"
        )

    return generate_chart


# ---------------------------------------------------------------------------
# Suite factory
# ---------------------------------------------------------------------------


def create_document_generation_tools(bot: BotModel | None = None) -> list[StrandsAgentTool]:
    """Return all document-generation tools as a list."""
    return [
        create_docx_tool(bot),
        create_pptx_tool(bot),
        create_xlsx_tool(bot),
        create_chart_tool(bot),
    ]
