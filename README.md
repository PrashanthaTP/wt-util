![wt-util-banner](./docs/banner-wt-util.png)
# wt-util
> Script to update windows terminal settings programmatically

## Usage

```bash
usage: wt-util [-h] -s SETTINGS -p PROFILE -k KEY -v VALUE [-o OUTPUT_FILE]

Script to update windows terminal settings json

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        Updated settings will be written to this file.If not
                        given original settings file will be overwritten
                        (default: )

mandatory arguments:
  -s SETTINGS, --settings SETTINGS
                        full path to windows terminal settings.json (default:
                        None)
  -p PROFILE, --profile PROFILE
                        wt profile name (default: None)
  -k KEY, --key KEY     settings key in the given profile to be updated
                        (default: None)
  -v VALUE, --value VALUE
                        new value to be updated for the given key (default:
                        None)
```

## Example

```bash
python wt-util.py --settings="${settings_json_filepath}"\
    --profile="GitBash" \
    --key="backgroundImage"\
    --value="C:/path/to/new_wallpaper.png"
```

