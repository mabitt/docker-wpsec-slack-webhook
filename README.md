# docker-wpsec-slack-webhook

Service to receive WPSec.com webhooks and call Slack incoming-webhook API to send alerts.

Usage:

```sh
docker run \
-e SLACK_WEBHOOK='url' \
-p 5000:5000 \
```

To debug, add:

```sh
-e LOGLEVEL='INFO' \
```
