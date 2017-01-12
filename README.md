# versioneye-slack
Send notifications from versioneye to slack channel

![Screenshot](https://raw.githubusercontent.com/Sharpek/versioneye-slack/master/data/preview.png)

# Install

```bash
pip install versioneye_slack
```

# How to use it:

```bash
versioneye_slack --versioneye-key={versioneye-key} --slack-channel="{publish channel}" --slack-hook='{registered slack hook url}'
```

To get slack hook url you have to visit: https://slack.com/apps/build and select Incoming WebHooks


# Help
```bash
versioneye_slack --help
```