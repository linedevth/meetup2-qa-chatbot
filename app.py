# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

from flask import Flask, request, abort, jsonify
from argparse import ArgumentParser
import sys
import os
import errno
import json
from testresult import TestResult

from linebot import (
    LineBotApi, WebhookHandler
)

from linebot.exceptions import (
    LineBotApiError, InvalidSignatureError
)

from linebot.models import (
    MessageEvent, FollowEvent, UnfollowEvent, PostbackEvent, TextMessage, TextSendMessage, SourceUser,
    SourceGroup, SourceRoom, FlexSendMessage,
)

app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)
test_result = TestResult()

static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except LineBotApiError as e:
        print("Got exception from LINE Messaging API: %s\n" % e.message)
        for m in e.error.details:
            print("  %s: %s" % (m.property, m.message))
        print("\n")
    except InvalidSignatureError:
        abort(400)

    return 'OK'


def make_static_tmp_dir():
    try:
        os.makedirs(static_tmp_path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(static_tmp_path):
            pass
        else:
            raise


@app.route('/testresult', methods=['POST'])
def send_test_result():
    data = dict()
    data['test_result'] = request.form.get('test_result')
    if data['test_result'] == 'SUCCESS':
        data['header_color'] = '#2ac12f'
    else:
        data['header_color'] = '#ba0900'
    data['start_time'] = request.form.get('start_time')
    data['end_time'] = request.form.get('end_time')
    data['duration'] = request.form.get('duration')
    data['passed'] = request.form.get('passed')
    data['failed'] = request.form.get('failed')
    data['total'] = request.form.get('total')
    data['report_url'] = request.form.get('report_url')
    data['changes'] = request.form.get('changes')
    data['started_by'] = request.form.get('started_by')
    data['job_name'] = request.form.get('job_name')
    data['build_no'] = request.form.get('build_no')
    data['to'] = request.form.get('to')
    result = {
        'result_code': 0,
        'result_message': 'success'
    }
    bubble_container = test_result.generate_test_result_message(data)
    line_bot_api.push_message(data['to'], messages=FlexSendMessage('Test Result', contents=bubble_container))
    return jsonify(result)


@handler.add(FollowEvent)
def handle_follow_event(event):
    print('Got Follow Event')


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    print('Got Text Message Event')
    print('user_id: {}'.format(event.source.user_id))


@handler.add(PostbackEvent)
def handle_postback_event(event):
    print('Got Postback Event')


if __name__ == '__main__':
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + '[--port <port> [--help]'
    )
    arg_parser.add_argument('-p', '--port', type=int, default=6000, help='port')
    arg_parser.add_argument('-d', '--debug', default=True, help='debug')
    options = arg_parser.parse_args()

    # create tmp dir for download content
    make_static_tmp_dir()

    app.run(host='0.0.0.0', debug=options.debug, port=options.port)
