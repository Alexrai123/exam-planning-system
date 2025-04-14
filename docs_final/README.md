# Exam Planning System Documentation

This directory contains the comprehensive documentation for the Exam Planning System.

## Documentation Structure

- **Source Files**: The `.rst` files contain the documentation source in reStructuredText format
- **HTML Documentation**: The generated HTML documentation is in this directory
- **Configuration**: `conf.py` contains the Sphinx configuration

## Viewing the Documentation

To view the documentation, open the `index.html` file in your web browser.

## Documentation Sections

1. **Introduction**: Overview of the Exam Planning System
2. **Architecture**: System architecture and component diagrams
3. **API Reference**: Documentation of all API endpoints
4. **Models**: Data models used in the system
5. **Database Schema**: Database tables and relationships
6. **Deployment**: Instructions for deploying the system

## Rebuilding the Documentation

If you need to rebuild the documentation, use the following commands:

```bash
# Navigate to the docs_final directory
cd docs_final

# Build the HTML documentation
python -m sphinx.cmd.build -b html . _build/html
```

This will generate updated HTML documentation in the `_build/html` directory.
