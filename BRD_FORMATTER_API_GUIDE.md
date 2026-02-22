# BRD Formatter API Usage Guide

## Overview

The `BRDFormatter` class provides a clean API for transforming analysis data into formal Business Requirements Documents. It integrates seamlessly with the existing Structify backend without modifying endpoints or request/response structures.

## Quick Start

### Import and Initialize

```python
from services.brd_generator import BRDFormatter

# Use analysis data from /analyze endpoint
formatter = BRDFormatter(analysis_data)
```

### Generate BRD Markdown

```python
# Generate formatted BRD as markdown string
brd_markdown = formatter.generate_formatted_brd()
print(brd_markdown)
```

### Export to Different Formats

```python
from services.brd_generator import BRDExporter

exporter = BRDExporter()

# Export to text
txt_buffer = exporter.to_text(brd_markdown)

# Export to Word document
docx_buffer = exporter.to_docx(brd_markdown)

# Export to PDF
pdf_buffer = exporter.to_pdf(brd_markdown)

# Export to PNG image
image_buffer = exporter.to_image(brd_markdown)
```

## Required Input Data Structure

The formatter expects a dictionary with the following keys:

```python
analysis_data = {
    # Required - Core project information
    'idea': str,                           # Business idea/project name
    'target_market': str,                  # Target market description
    'problem_statement': str,              # Problem being addressed
    'analysis': str,                       # Analysis description
    
    # Required - Viability metrics
    'compatibility_score': int,            # 0-100, viability score
    'risk_level': str,                     # 'low', 'medium', 'high'
    
    # Required - Supporting data
    'improvement_suggestions': list,       # List of suggested improvements
    'domain_tags': list,                   # Industry/domain tags
}
```

## API Methods

### BRDFormatter

#### `__init__(analysis_data: Dict[str, Any])`

Initialize formatter with analysis data.

**Parameters:**
- `analysis_data` (dict): Analysis results from AI engine

**Example:**
```python
formatter = BRDFormatter(analysis_data)
```

#### `generate_formatted_brd() -> str`

Generate complete formal BRD document in markdown format.

**Returns:** Formatted BRD as markdown string

**Example:**
```python
brd_content = formatter.generate_formatted_brd()
```

**Output Structure:**
- Header Metadata
- Executive Summary
- Project Objectives
- Project Scope
- Business Requirements (Table)
- Key Stakeholders (Table)
- Project Constraints (Table)
- Cost-Benefit Analysis (Table)

### BRDExporter

Static methods for exporting BRD content to different formats.

#### `to_text(brd_content: str) -> io.BytesIO`

Export BRD to plain text format.

**Parameters:**
- `brd_content` (str): BRD markdown content

**Returns:** BytesIO buffer with text content

**Example:**
```python
txt_buffer = BRDExporter.to_text(brd_markdown)
txt_bytes = txt_buffer.getvalue()
```

#### `to_docx(brd_content: str) -> io.BytesIO`

Export BRD to Word document format (.docx).

**Parameters:**
- `brd_content` (str): BRD markdown content

**Returns:** BytesIO buffer with Word document

**Example:**
```python
docx_buffer = BRDExporter.to_docx(brd_markdown)
# Save to file
with open('brd.docx', 'wb') as f:
    f.write(docx_buffer.getvalue())
```

**Note:** Requires `python-docx` package. Falls back to text if not installed.

#### `to_pdf(brd_content: str) -> io.BytesIO`

Export BRD to PDF format.

**Parameters:**
- `brd_content` (str): BRD markdown content

**Returns:** BytesIO buffer with PDF content

**Example:**
```python
pdf_buffer = BRDExporter.to_pdf(brd_markdown)
# Save to file
with open('brd.pdf', 'wb') as f:
    f.write(pdf_buffer.getvalue())
```

**Note:** Requires `reportlab` package. Falls back to text if not installed.

#### `to_image(brd_content: str) -> io.BytesIO`

Export BRD to PNG image format.

**Parameters:**
- `brd_content` (str): BRD markdown content

**Returns:** BytesIO buffer with PNG image

**Example:**
```python
image_buffer = BRDExporter.to_image(brd_markdown)
# Save to file
with open('brd.png', 'wb') as f:
    f.write(image_buffer.getvalue())
```

**Note:** Requires `Pillow` package.

## Complete Workflow Example

### Step 1: Analyze Business Idea

```python
from services import generate_analysis_response

analysis_result = generate_analysis_response(
    idea="AI-Powered Customer Service Platform",
    target_market="Enterprise SaaS Organizations",
    problem_statement="High customer support costs and slow response times",
    api_key=None,
    api_provider="gemini"
)
```

### Step 2: Generate Formal BRD

```python
from services import BRDFormatter

formatter = BRDFormatter(analysis_result)
brd_markdown = formatter.generate_formatted_brd()
```

### Step 3: Export to Desired Format

```python
from services import BRDExporter

# Choose format based on requirement
if format == "docx":
    buffer = BRDExporter.to_docx(brd_markdown)
elif format == "pdf":
    buffer = BRDExporter.to_pdf(brd_markdown)
elif format == "image":
    buffer = BRDExporter.to_image(brd_markdown)
else:
    buffer = BRDExporter.to_text(brd_markdown)

# Return as file download
return StreamingResponse(
    iter([buffer.getvalue()]),
    media_type=mime_type,
    headers={"Content-Disposition": f"attachment; filename=brd_{idea}.{ext}"}
)
```

## Section Details

### 1. Header Metadata
- Auto-populated with project name, PM assignment, date, and status
- Format: Markdown header with bold key-value pairs

### 2. Executive Summary
- Auto-generated from analysis data
- Incorporates viability rating
- 5-8 line business overview
- Focuses on problem, target users, business value

### 3. Project Objectives
- 5 base outcome-focused objectives
- Enhanced with improvement suggestions
- Business-driven, not feature-focused

### 4. Project Scope
- IN SCOPE: System analysis responsibilities
- OUT OF SCOPE: Implementation exclusions
- Clear boundary definition

### 5. Business Requirements
- 8 pre-defined requirement patterns
- "System shall..." format
- Priority levels: High, Medium, Low
- Criticality: Must, Should, Could
- All requirements are testable

### 6. Key Stakeholders
- 7 standard business roles
- Maps to system interactions
- Includes responsibilities

### 7. Project Constraints
- 7 constraint categories
- Auto-populated from analysis data
- Realistic operational limitations

### 8. Cost-Benefit Analysis
- Cost and benefit mapping
- Financial projection section
- ROI assessment
- Investment recommendation

## Content Generation Rules

### Viability Rating (Score-Based)

```
Score 80-100: Excellent     -> Strong investment recommendation
Score 60-79:  Good          -> Moderate investment recommendation
Score 40-59:  Fair          -> Conditional investment recommendation
Score 0-39:   Needs Dev     -> Limited investment recommendation
```

### Domain Tag Handling

- Uses first domain tag for market dependency constraint
- Defaults to "General Business" if no tags provided
- Multiple tags supported

### Risk Level Processing

- Accepts: 'low', 'medium', 'high'
- Normalized to uppercase in output
- Used for project constraints

## Error Handling

### Missing Data

If optional fields are missing, the formatter uses defaults:

```python
# With defaults applied
analysis_data = {
    'idea': analysis_data.get('idea', 'Unnamed Business Idea'),
    'target_market': analysis_data.get('target_market', 'Unspecified'),
    'problem_statement': analysis_data.get('problem_statement', 'Not specified'),
    'analysis': analysis_data.get('analysis', 'Analysis not available'),
    'compatibility_score': analysis_data.get('compatibility_score', 50),
    'risk_level': analysis_data.get('risk_level', 'medium'),
    'improvement_suggestions': analysis_data.get('improvement_suggestions', []),
    'domain_tags': analysis_data.get('domain_tags', ['General Business']),
}
```

### Export Format Fallback

If required packages are missing:
- PDF generation falls back to text
- DOCX generation falls back to text
- PNG generation falls back to text
- Text format always works

## Performance Characteristics

- **Generation time**: <100ms for typical analysis data
- **Output size**: 5-10KB for markdown, 100-300KB for images
- **Memory usage**: Minimal, no caching required
- **Scalability**: Stateless, thread-safe

## Best Practices

### 1. Always Validate Input Data

```python
required_fields = ['idea', 'target_market', 'problem_statement', 
                  'analysis', 'compatibility_score', 'risk_level',
                  'improvement_suggestions', 'domain_tags']

missing = [f for f in required_fields if f not in analysis_data]
if missing:
    raise ValueError(f"Missing required fields: {missing}")
```

### 2. Use Appropriate Export Format

```python
# For documents: DOCX or PDF
# For web viewing: Markdown or HTML
# For printing: PDF
# For presentations: PNG
```

### 3. Include Error Handling

```python
try:
    formatter = BRDFormatter(analysis_data)
    brd = formatter.generate_formatted_brd()
except Exception as e:
    logger.error(f"BRD generation failed: {e}")
    return error_response()
```

### 4. Log Generation Events

```python
logger.info(f"Generating BRD for: {analysis_data['idea']}")
formatter = BRDFormatter(analysis_data)
brd = formatter.generate_formatted_brd()
logger.info(f"BRD generated: {len(brd)} characters")
```

## Integration with Backend Endpoints

### Option A: Add New Endpoint (Recommended)

```python
from fastapi import FastAPI
from services import BRDFormatter, BRDExporter

@app.post("/generate_formal_brd")
def generate_formal_brd(request: AnalysisData):
    """Generate formal Business Requirements Document"""
    
    formatter = BRDFormatter(request.dict())
    brd_content = formatter.generate_formatted_brd()
    
    exporter = BRDExporter()
    buffer = getattr(exporter, f'to_{request.format}')(brd_content)
    
    return StreamingResponse(
        iter([buffer.getvalue()]),
        media_type=mime_type
    )
```

### Option B: Extend Existing Endpoint

```python
# Modify existing /generate_brd endpoint to support formal BRD
if request.format == "formal_brd":
    formatter = BRDFormatter(request.analysis_data)
    content = formatter.generate_formatted_brd()
else:
    # Use existing BRDGenerator
    generator = BRDGenerator(request.analysis_data)
    content = generator.generate_txt()
```

## Troubleshooting

### Issue: Empty or Generic Content

**Solution:** Check that all analysis data fields are properly populated

```python
# Validate data before formatting
if not analysis_data['idea'] or not analysis_data['target_market']:
    raise ValueError("Missing essential analysis data")
```

### Issue: Export Format Fallback

**To enable full export support:**

```bash
# Install optional dependencies
pip install python-docx reportlab Pillow
```

### Issue: Encoding Errors

**Solution:** Ensure proper encoding when exporting

```python
# Write files with UTF-8 encoding
with open('brd.txt', 'w', encoding='utf-8') as f:
    f.write(brd_markdown)
```

## Compatibility

- **Python Version**: 3.7+
- **Backend Framework**: FastAPI
- **Optional Dependencies**: python-docx, reportlab, Pillow
- **Core Dependencies**: None (uses Python standard library)
