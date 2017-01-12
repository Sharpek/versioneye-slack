#!/usr/bin/env python
import json
import os

import requests
import click

from os.path import expanduser


# noinspection PyMethodMayBeStatic
class VersionEyeNotification:
    def __init__(self, api_key, slack_hook, slack_channel):
        self._slack_hook = slack_hook
        self._slack_channel = slack_channel
        self._api_key = api_key
        self._cache_file = os.path.join(
            expanduser('~'),
            '.versioneye.slack.cache'
        )

    def run(self):
        result = []

        for project in self._fetch_projects():
            result += self._get_packages(project['ids'])

        outdated = self._filter_outdated(result)
        outdated = self._filter_cached(outdated)

        if outdated:
            message = self._get_attachment(outdated)
            assert self._send_message(message).status_code == 200
            self._save_notification(outdated)

    def _fetch_projects(self):
        url = 'https://www.versioneye.com/api/v2/projects?api_key={}'.format(self._api_key)
        return requests.get(url).json()

    def _get_packages(self, project_key):
        url = 'https://www.versioneye.com/api/v2/projects/{project_key}?api_key={api_key}'.format(
            api_key=self._api_key, project_key=project_key)
        return requests.get(url).json()['dependencies']

    def _filter_outdated(self, packages):
        return [x for x in packages if x['outdated']]

    def _get_attachment(self, outdated):
        messages = []

        for package in outdated:
            package['security_vulnerabilities'] = package['security_vulnerabilities'] or 'no'
            messages.append({
                'text': '''Package: {name} ({language})
        current version: {version_current}, our version: {version_requested}
        security_vulnerabilities: {security_vulnerabilities}'''.format(
                    **package),
                'color-code': 'danger'
            })

        return messages

    def _send_message(self, attachments):
        payload = {
            "channel": self._slack_channel,
            "username": "VersionEye",
            "attachments": attachments,
            'icon_url': 'https://raw.githubusercontent.com/Sharpek/versioneye-slack/master/data/verisoneye-logo-small.png'
        }

        return requests.post(
            url=self._slack_hook,
            data=json.dumps(payload),
        )

    def _filter_cached(self, outdated):
        cached = {}
        if os.path.exists(self._cache_file):
            with open(self._cache_file) as cache_file:
                cached = self._get_cached_content(cache_file)

        outdated = [x for x in outdated if x['version_current'] != cached.get(self._get_package_key(x))]

        return outdated

    def _get_package_key(self, package):
        return '{language}:{prod_key}'.format(**package)

    def _get_cached_content(self, cache_file):
        try:
            return json.loads(cache_file.read())
        except Exception:
            return {}

    def _save_notification(self, outdated):
        with open(self._cache_file, 'a+') as cache_file:
            cached = self._get_cached_content(cache_file)

            cache_file.seek(0)

            for package in outdated:
                key = self._get_package_key(package)
                cached[key] = package['version_current']

            cache_file.write(
                json.dumps(cached)
            )
            cache_file.truncate()


@click.command()
@click.option('--versioneye-key', help='Versioneye API KEY', required=True)
@click.option('--slack-hook', help='Slack integration HOOK', required=True)
@click.option('--slack-channel', default='#general', help='Slack channel', required=True)
def run(versioneye_key, slack_hook, slack_channel):
    VersionEyeNotification(
        versioneye_key,
        slack_hook,
        slack_channel
    ).run()


if __name__ == '__main__':
    run()
