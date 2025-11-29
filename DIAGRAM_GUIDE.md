# Architecture Diagram Guide

## Viewing the Mermaid Diagram

The `architecture_diagram.mmd` file contains a Mermaid diagram that visualizes the application architecture.

### Option 1: Online Mermaid Editor

1. Go to https://mermaid.live/
2. Copy the contents of `architecture_diagram.mmd`
3. Paste into the editor
4. View the rendered diagram
5. Export as PNG/SVG using the download button

### Option 2: VS Code Extension

1. Install "Markdown Preview Mermaid Support" extension
2. Open `architecture_diagram.mmd`
3. Press `Ctrl+Shift+V` to preview
4. Right-click and save as image

### Option 3: GitHub

1. Push the `.mmd` file to GitHub
2. GitHub automatically renders Mermaid diagrams
3. View directly in the repository

### Option 4: Command Line (mmdc)

```bash
npm install -g @mermaid-js/mermaid-cli
mmdc -i architecture_diagram.mmd -o architecture_diagram.png
```

## Diagram Components

### Color Legend

- **Orange (#FF9900)**: User Interface (Streamlit)
- **Blue (#3B48CC)**: Core Logic (Python)
- **Light Blue (#527FFF)**: AWS Services
- **Purple (#8C4FFF)**: AI Models
- **Green (#2ECC71)**: Output/Results

### Flow Description

1. **User Input** → User provides text via web interface
2. **Streamlit UI** → Handles user interaction and display
3. **Validation** → Checks AWS credentials
4. **BedrockSummarizer** → Core processing logic
5. **AWS Bedrock** → Cloud AI service
6. **Claude Models** → AI model processing
7. **Summaries** → Generated in three lengths
8. **Download** → Export results
9. **Display** → Show in web interface

## Architecture Highlights

### Separation of Concerns
- **Presentation Layer**: Streamlit UI
- **Business Logic**: BedrockSummarizer class
- **External Services**: AWS Bedrock API

### Data Flow
- Unidirectional flow from input to output
- Clear separation between UI and logic
- Stateless API calls to Bedrock

### Error Handling
- Validation at each layer
- Graceful error messages
- Credential verification upfront

## Exporting the Diagram

### Recommended Settings

**For Documentation:**
- Format: PNG
- Resolution: 1920x1080
- Background: White
- Scale: 2x

**For Presentations:**
- Format: SVG (scalable)
- Background: Transparent
- High quality

**For Web:**
- Format: PNG
- Resolution: 1280x720
- Optimized file size

### Save Location

Save the exported diagram as:
```
assets/architecture_diagram.png
```

This matches the project structure and makes it easy to reference in documentation.

## Using in Documentation

### Markdown
```markdown
![Architecture Diagram](assets/architecture_diagram.png)
```

### HTML
```html
<img src="assets/architecture_diagram.png" alt="Architecture Diagram" width="800">
```

### README Integration

Add to README.md:
```markdown
## Architecture

![System Architecture](assets/architecture_diagram.png)

The application follows a clean, modular architecture with clear separation between the UI layer (Streamlit), business logic (BedrockSummarizer), and external services (AWS Bedrock).
```

## Diagram Maintenance

### When to Update

Update the diagram when:
- Adding new components
- Changing data flow
- Modifying architecture
- Adding integrations
- Changing AWS services

### Version Control

- Keep `.mmd` source in version control
- Export new PNG after changes
- Document changes in commit messages
- Tag major architecture changes

## Alternative Diagram Tools

If you prefer other tools:

### Draw.io
- Import Mermaid or recreate
- More visual customization
- Export to multiple formats

### Lucidchart
- Professional diagrams
- Collaboration features
- AWS icon library

### PlantUML
- Text-based like Mermaid
- More diagram types
- Java-based rendering

## Quick Export Instructions

**Fastest method:**

1. Open https://mermaid.live/
2. Paste `architecture_diagram.mmd` content
3. Click "Download PNG"
4. Save as `assets/architecture_diagram.png`
5. Done! ✓

---

**Note**: The Mermaid diagram is designed to be simple and clear. Feel free to enhance it with additional details as your project evolves.
