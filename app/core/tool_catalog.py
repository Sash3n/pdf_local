"""Config-driven catalog powering the generic tool workspace page.

Each entry maps directly to an existing, already-tested API route. Field `name`s must match
the FastAPI `Form(...)` parameter names exactly - see app/api/*.py for the source of truth.
"""

from dataclasses import dataclass, field


@dataclass
class ToolField:
    name: str
    label: str
    type: str  # "text" | "number" | "password" | "select" | "range"
    default: str | int | float | None = None
    options: list[tuple[str, str]] | None = None  # (value, label) pairs, for type="select"
    min: float | None = None
    max: float | None = None
    step: float | None = None
    placeholder: str | None = None
    required: bool = True


@dataclass
class Tool:
    slug: str
    label: str
    icon: str
    description: str
    endpoint: str
    file_field: str  # "file" or "files" - must match the backend param name
    multiple: bool
    accept: str
    action_label: str
    action_icon: str
    extra_fields: list[ToolField] = field(default_factory=list)


@dataclass
class ToolCategory:
    key: str
    label: str
    icon: str
    tools: list[Tool]


CATEGORIES: list[ToolCategory] = [
    ToolCategory(
        key="organize",
        label="Organize",
        icon="auto_stories",
        tools=[
            Tool(
                slug="merge",
                label="Merge PDF",
                icon="call_merge",
                description="Combine multiple PDF files into one document. Drag to reorder "
                "before merging.",
                endpoint="/api/organize/merge",
                file_field="files",
                multiple=True,
                accept="application/pdf",
                action_label="Merge Files",
                action_icon="call_merge",
            ),
            Tool(
                slug="split",
                label="Split PDF",
                icon="call_split",
                description="Split every page of a PDF into its own file, delivered as a zip.",
                endpoint="/api/organize/split",
                file_field="file",
                multiple=False,
                accept="application/pdf",
                action_label="Split File",
                action_icon="call_split",
            ),
            Tool(
                slug="remove-pages",
                label="Remove Pages",
                icon="delete_sweep",
                description="Delete specific pages from a PDF.",
                endpoint="/api/organize/remove",
                file_field="file",
                multiple=False,
                accept="application/pdf",
                action_label="Remove Pages",
                action_icon="delete_sweep",
                extra_fields=[
                    ToolField(
                        name="pages",
                        label="Pages to remove",
                        type="text",
                        placeholder="e.g. 2,4,7",
                    ),
                ],
            ),
            Tool(
                slug="extract-pages",
                label="Extract Pages",
                icon="layers",
                description="Pull specific pages out of a PDF into a new document.",
                endpoint="/api/organize/extract",
                file_field="file",
                multiple=False,
                accept="application/pdf",
                action_label="Extract Pages",
                action_icon="layers",
                extra_fields=[
                    ToolField(
                        name="pages",
                        label="Pages to extract",
                        type="text",
                        placeholder="e.g. 1,3,5",
                    ),
                ],
            ),
            Tool(
                slug="organize-pages",
                label="Organize (Reorder)",
                icon="reorder",
                description="Reorder the pages of a PDF. Page thumbnails aren't rendered yet, "
                "so specify the new order by page number.",
                endpoint="/api/organize/reorder",
                file_field="file",
                multiple=False,
                accept="application/pdf",
                action_label="Reorder Pages",
                action_icon="reorder",
                extra_fields=[
                    ToolField(
                        name="order",
                        label="New page order",
                        type="text",
                        placeholder="e.g. 3,1,2",
                    ),
                ],
            ),
            Tool(
                slug="scan-to-pdf",
                label="Scan to PDF",
                icon="scanner",
                description="Combine one or more images into a single PDF document.",
                endpoint="/api/organize/scan-to-pdf",
                file_field="files",
                multiple=True,
                accept="image/*",
                action_label="Create PDF",
                action_icon="picture_as_pdf",
            ),
        ],
    ),
    ToolCategory(
        key="optimize",
        label="Optimize",
        icon="speed",
        tools=[
            Tool(
                slug="compress",
                label="Compress PDF",
                icon="compress",
                description="Shrink file size by downsampling embedded images.",
                endpoint="/api/optimize/compress",
                file_field="file",
                multiple=False,
                accept="application/pdf",
                action_label="Compress",
                action_icon="compress",
                extra_fields=[
                    ToolField(
                        name="quality",
                        label="Image quality",
                        type="range",
                        default=60,
                        min=10,
                        max=95,
                        step=5,
                    ),
                ],
            ),
            Tool(
                slug="repair",
                label="Repair PDF",
                icon="home_repair_service",
                description="Attempt to recover a damaged or corrupted PDF file.",
                endpoint="/api/optimize/repair",
                file_field="file",
                multiple=False,
                accept="application/pdf",
                action_label="Repair",
                action_icon="home_repair_service",
            ),
        ],
    ),
    ToolCategory(
        key="convert-to-pdf",
        label="Convert to PDF",
        icon="transform",
        tools=[
            Tool(
                slug="jpg-to-pdf",
                label="JPG to PDF",
                icon="image",
                description="Combine one or more images into a single PDF document.",
                endpoint="/api/convert-to-pdf/jpg",
                file_field="files",
                multiple=True,
                accept="image/*",
                action_label="Create PDF",
                action_icon="picture_as_pdf",
            ),
            Tool(
                slug="word-to-pdf",
                label="Word to PDF",
                icon="description",
                description="Convert a Word document to PDF using LibreOffice headless. "
                "Requires LibreOffice to be installed on this machine.",
                endpoint="/api/convert-to-pdf/word",
                file_field="file",
                multiple=False,
                accept=".doc,.docx",
                action_label="Convert",
                action_icon="transform",
            ),
            Tool(
                slug="powerpoint-to-pdf",
                label="PowerPoint to PDF",
                icon="slideshow",
                description="Convert a PowerPoint presentation to PDF using LibreOffice "
                "headless. Requires LibreOffice to be installed on this machine.",
                endpoint="/api/convert-to-pdf/powerpoint",
                file_field="file",
                multiple=False,
                accept=".ppt,.pptx",
                action_label="Convert",
                action_icon="transform",
            ),
            Tool(
                slug="excel-to-pdf",
                label="Excel to PDF",
                icon="table_chart",
                description="Convert an Excel spreadsheet to PDF using LibreOffice headless. "
                "Requires LibreOffice to be installed on this machine.",
                endpoint="/api/convert-to-pdf/excel",
                file_field="file",
                multiple=False,
                accept=".xls,.xlsx",
                action_label="Convert",
                action_icon="transform",
            ),
            Tool(
                slug="html-to-pdf",
                label="HTML to PDF",
                icon="html",
                description="Convert an HTML file to PDF using LibreOffice headless. "
                "Requires LibreOffice to be installed on this machine.",
                endpoint="/api/convert-to-pdf/html",
                file_field="file",
                multiple=False,
                accept=".html,.htm",
                action_label="Convert",
                action_icon="transform",
            ),
        ],
    ),
    ToolCategory(
        key="convert-from-pdf",
        label="Convert from PDF",
        icon="picture_as_pdf",
        tools=[
            Tool(
                slug="pdf-to-jpg",
                label="PDF to JPG",
                icon="image",
                description="Rasterize every page of a PDF into a JPG, delivered as a zip.",
                endpoint="/api/convert-from-pdf/jpg",
                file_field="file",
                multiple=False,
                accept="application/pdf",
                action_label="Convert",
                action_icon="transform",
            ),
            Tool(
                slug="pdf-to-word",
                label="PDF to Word",
                icon="description",
                description="Convert a PDF into an editable Word document.",
                endpoint="/api/convert-from-pdf/word",
                file_field="file",
                multiple=False,
                accept="application/pdf",
                action_label="Convert",
                action_icon="transform",
            ),
            Tool(
                slug="pdf-to-excel",
                label="PDF to Excel",
                icon="table_chart",
                description="Extract tables from a PDF into an Excel workbook.",
                endpoint="/api/convert-from-pdf/excel",
                file_field="file",
                multiple=False,
                accept="application/pdf",
                action_label="Convert",
                action_icon="transform",
            ),
        ],
    ),
    ToolCategory(
        key="edit",
        label="Edit",
        icon="edit_note",
        tools=[
            Tool(
                slug="rotate",
                label="Rotate PDF",
                icon="rotate_right",
                description="Rotate pages of a PDF clockwise.",
                endpoint="/api/edit/rotate",
                file_field="file",
                multiple=False,
                accept="application/pdf",
                action_label="Rotate",
                action_icon="rotate_right",
                extra_fields=[
                    ToolField(
                        name="angle",
                        label="Rotation angle",
                        type="select",
                        default=90,
                        options=[("90", "90°"), ("180", "180°"), ("270", "270°")],
                    ),
                    ToolField(
                        name="pages",
                        label="Pages (leave blank for all)",
                        type="text",
                        placeholder="e.g. 1,2",
                        required=False,
                    ),
                ],
            ),
            Tool(
                slug="page-numbers",
                label="Add Page Numbers",
                icon="format_list_numbered",
                description="Stamp sequential page numbers onto every page.",
                endpoint="/api/edit/page-numbers",
                file_field="file",
                multiple=False,
                accept="application/pdf",
                action_label="Add Numbers",
                action_icon="format_list_numbered",
                extra_fields=[
                    ToolField(name="start", label="Start at", type="number", default=1),
                ],
            ),
            Tool(
                slug="watermark",
                label="Add Watermark",
                icon="water_drop",
                description="Stamp a text watermark across every page.",
                endpoint="/api/edit/watermark",
                file_field="file",
                multiple=False,
                accept="application/pdf",
                action_label="Add Watermark",
                action_icon="water_drop",
                extra_fields=[
                    ToolField(
                        name="text", label="Watermark text", type="text", placeholder="DRAFT"
                    ),
                    ToolField(
                        name="opacity",
                        label="Opacity",
                        type="range",
                        default=0.3,
                        min=0.1,
                        max=1,
                        step=0.1,
                    ),
                ],
            ),
            Tool(
                slug="crop",
                label="Crop PDF",
                icon="crop",
                description="Crop every page to a bounding box, in PDF points from the "
                "bottom-left corner. A visual crop picker is a future improvement.",
                endpoint="/api/edit/crop",
                file_field="file",
                multiple=False,
                accept="application/pdf",
                action_label="Crop",
                action_icon="crop",
                extra_fields=[
                    ToolField(name="x0", label="Left (x0)", type="number", default=0),
                    ToolField(name="y0", label="Bottom (y0)", type="number", default=0),
                    ToolField(name="x1", label="Right (x1)", type="number", default=400),
                    ToolField(name="y1", label="Top (y1)", type="number", default=600),
                ],
            ),
            Tool(
                slug="edit-text",
                label="Edit Text",
                icon="text_fields",
                description="Insert a line of text at a specific position on one page, in "
                "PDF points from the bottom-left corner.",
                endpoint="/api/edit/text",
                file_field="file",
                multiple=False,
                accept="application/pdf",
                action_label="Insert Text",
                action_icon="text_fields",
                extra_fields=[
                    ToolField(name="page", label="Page number", type="number", default=1),
                    ToolField(name="content", label="Text", type="text", placeholder="Hello"),
                    ToolField(name="x", label="X position", type="number", default=50),
                    ToolField(name="y", label="Y position", type="number", default=50),
                ],
            ),
        ],
    ),
    ToolCategory(
        key="security",
        label="PDF Security",
        icon="lock",
        tools=[
            Tool(
                slug="unlock",
                label="Unlock PDF",
                icon="lock_open",
                description="Remove password protection from a PDF you have the password for.",
                endpoint="/api/security/unlock",
                file_field="file",
                multiple=False,
                accept="application/pdf",
                action_label="Unlock",
                action_icon="lock_open",
                extra_fields=[
                    ToolField(name="password", label="Current password", type="password"),
                ],
            ),
            Tool(
                slug="protect",
                label="Protect PDF",
                icon="lock",
                description="Encrypt a PDF with AES-256 and a password.",
                endpoint="/api/security/protect",
                file_field="file",
                multiple=False,
                accept="application/pdf",
                action_label="Protect",
                action_icon="lock",
                extra_fields=[
                    ToolField(name="user_password", label="Password", type="password"),
                    ToolField(
                        name="owner_password",
                        label="Owner password (optional)",
                        type="password",
                        required=False,
                    ),
                ],
            ),
        ],
    ),
    ToolCategory(
        key="intelligence",
        label="PDF Intelligence",
        icon="psychology",
        tools=[
            Tool(
                slug="pdf-to-markdown",
                label="PDF to Markdown",
                icon="markdown",
                description="Extract structured Markdown from a PDF - headings and bullet "
                "lists are detected automatically.",
                endpoint="/api/intelligence/pdf-to-markdown",
                file_field="file",
                multiple=False,
                accept="application/pdf",
                action_label="Convert",
                action_icon="markdown",
            ),
        ],
    ),
]


def all_tools() -> list[Tool]:
    return [tool for category in CATEGORIES for tool in category.tools]


def get_tool(slug: str) -> Tool | None:
    for tool in all_tools():
        if tool.slug == slug:
            return tool
    return None
