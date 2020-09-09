import sys
import os
import pycurl
import hashlib
import logging

from flask import Flask, request, abort, jsonify

LOGLEVEL = os.environ.get('LOGLEVEL', 'WARNING').upper()
logging.basicConfig(level=LOGLEVEL)

SLACK_WEBHOOK = os.environ.get('SLACK_WEBHOOK')
logging.info('Webhook: %s' % SLACK_WEBHOOK)

app = Flask(__name__)
slack_url = pycurl.Curl() 
slack_url.setopt(slack_url.URL, SLACK_WEBHOOK)

@app.route('/', methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST':
        content = request.get_json()
        wpsec_name = content['name']
        wpsec_status = content['status']
        wpsec_url = content['url']
        wpsec_reporturl = content['reportURL']
        slack_short = '<%s|%s> - <%s|%s>' % (wpsec_url, wpsec_name, wpsec_reporturl, wpsec_status)
        logging.info('Scan Results: %s' % slack_short)
        if (wpsec_status =='vuln'): 
            slack_color = 'danger'
            slack_status = 'Vulnerable'
        elif(wpsec_status =='no-vuln'): 
            slack_color = 'good'
            slack_status = 'Secure'
        else: 
            slack_color = 'warning'
            slack_status = 'Error'

        slack_data = '{"attachments":[ { "fallback":"Scan Results: %s", "color":"%s", "pretext":"Scan Results: %s", "fields":[ { "value":"URL: %s \\nStatus: %s \\nReport: %s", "short":false } ] } ] }' % (slack_short, slack_color, wpsec_name, wpsec_url, slack_status, wpsec_reporturl)
        logging.info('Slack Payload: %s' % slack_data)
        slack_url.setopt(slack_url.HTTPHEADER, ['Accept: */*',
                                                'Content-Type: application/json'])
        slack_url.setopt(slack_url.POSTFIELDS, slack_data)
        slack_url.perform()
        logging.info('Slack Status: %d' % slack_url.getinfo(slack_url.RESPONSE_CODE))
        if slack_url.getinfo(slack_url.RESPONSE_CODE) == 200:
            return jsonify({'status':'success'}), 200
        else:
            return jsonify({'status':'error'}), 401
        slack_url.close()
    else:
        return 'OK', 200

if __name__ == '__main__':
    app.run()
