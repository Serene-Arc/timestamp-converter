# timestamp converter

This is a basic tool for converting timestamps of varying formats to ISO 8601.

For those coming from the BDFR project, the following should convert old timestamps into ISO format:

```bash
python3 -m timestampconverter DESTINATION '(\d{4}-\d{2}-\d{2}_\d{2}-\d{2})' '%Y-%m-%d_%H-%M' --recursive
```

To change the folders in a directory, use the following command. Note that the `--recursive` and `--include-folders` options are mutually exclusive, as changing the folder name while there are still files to change will result in an error. Thus, to change folder titles, it must be done one directory at a time.

```bash
python3 -m timestampconverter DESTINATION '(\d{4}-\d{2}-\d{2}_\d{2}-\d{2})' '%Y-%m-%d_%H-%M' --include-folders
```

## Arguments and Options

The following options and arguments are available:

- `destination`
- `regex`
- `time-format`
- `-r, --recursive`
- `--include-folders`
- `-n, --no-act`
- `-v, --verbose`
