# timestamp converter

This is a basic tool for converting timestamps of varying formats to ISO 8601.

For those coming from the BDFR project, the following should convert old timestamps into ISO format:

```bash
python3 -m timestampconverter DESTINATION '(\d{4}-\d{2}-\d{2}_\d{2}-\d{2})' '%Y-%m-%d_%H-%M'
```

Note that this tool is recursive, and will attempt to change every file in the given directory and any subdirectories.

## Arguments and Options

The following options and arguments are available:

- `destination`
- `regex`
- `time-format`
- `-n, --no-act`
- `-v, --verbose`