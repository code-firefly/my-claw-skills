# JSON Schemas for Learn System

This directory contains JSON Schema definitions for the learn system data structures.

## Purpose

These schemas enable:
1. **Data Validation**: Ensure data integrity and consistency
2. **Sharing**: Export and import learning packages
3. **Interoperability**: Standard format for exchanging learning data
4. **Tool Support**: Enable JSON validation in editors and IDEs

## Schema Files

### Core Data Schemas

| Schema | Description | Validates |
|--------|-------------|-----------|
| `goals.schema.json` | Learning goals structure | `.learn-system/goals.json` |
| `progress.schema.json` | Learning progress tracking | `.learn-system/progress.json` |
| `bookmarks.schema.json` | Learning bookmarks | `.learn-system/bookmarks.json` |

### Sharing Schema

| Schema | Description | Purpose |
|--------|-------------|---------|
| `learning-package.schema.json` | Learning package format | Export/import complete learning packages |

## Usage

### Validation

You can validate your JSON files against these schemas using any JSON Schema validator:

```bash
# Using ajv-cli (npm install -g ajv-cli)
ajv validate -s schemas/goals.schema.json -d .learn-system/goals.json

# Using Python jsonschema (pip install jsonschema)
python -m jsonschema .learn-system/goals.json --schema schemas/goals.schema.json
```

### Editor Support

Add schema validation to your editor:

**VSCode** (`.vscode/settings.json`):
```json
{
  "json.schemas": [
    {
      "fileMatch": [".learn-system/goals.json"],
      "url": "./schemas/goals.schema.json"
    },
    {
      "fileMatch": [".learn-system/progress.json"],
      "url": "./schemas/progress.schema.json"
    },
    {
      "fileMatch": [".learn-system/bookmarks.json"],
      "url": "./schemas/bookmarks.schema.json"
    },
    {
      "fileMatch": ["*.learning-package.json"],
      "url": "./schemas/learning-package.schema.json"
    }
  ]
}
```

## Learning Package Format

A learning package (`*.learning-package.json`) contains:

```json
{
  "version": "1.0.0",
  "package_name": "OpenClaw Development",
  "package_id": "openclaw-dev-2026",
  "author": "your-name",
  "description": "Complete learning package for OpenClaw skill development",
  "created_at": "2026-03-14",
  "tags": ["openclaw", "skill-development", "ai"],
  "goals": { ... },
  "courses": { ... },
  "cache": { ... },
  "bookmarks": { ... }
}
```

### Export a Learning Package

To export your learning data as a shareable package:

1. Combine `goals.json`, `progress.json`, `bookmarks.json`
2. Include course definitions from `cache/.metadata.json`
3. Add course content from `cache/*/` directories
4. Validate against `learning-package.schema.json`

### Import a Learning Package

To import a learning package:

1. Validate the package against `learning-package.schema.json`
2. Extract `goals` and write to `.learn-system/goals.json`
3. Extract courses and create course structure in `.learn-system/cache/`
4. Optionally import bookmarks to `.learn-system/bookmarks.json`

## Schema Versioning

All schemas follow Semantic Versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Breaking changes to structure
- **MINOR**: New features or backward-compatible changes
- **PATCH**: Bug fixes or documentation updates

Current schema version: `1.0.0`

## Contribution

When adding new fields or modifying schemas:

1. Update the relevant schema file
2. Increment the version number appropriately
3. Update this README with changes
4. Test validation with sample data

## Support

For issues or questions about these schemas:
- Check the schema validation error messages
- Review the schema definitions in this directory
- Refer to the main learn-system documentation
