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

from dateutil.relativedelta import relativedelta as rd
from datetime import datetime
import requests
import os
import sys
import json

jenkins_user = os.getenv('JENKINS_USER')
jenkins_user_token = os.getenv('JENKINS_USER_TOKEN')
fmt = '{0.minutes} mins {0.seconds}s'
fmt_result = '{0.hours} hours {0.minutes} mins {0.seconds}s ago'
bucket_url_prefix = os.getenv('VIDEO_BUCKET_URL_PREFIX')
if bucket_url_prefix is None:
    print('Specify VIDEO_BUCKET_URL_PREFIX as environment variable')
    sys.exit(1)

video_url = bucket_url_prefix + '/{0}/{1}/{2}.mp4'


class Jenkins(object):

    def build_job(self, job_name):
        jenkins_url = os.getenv('JENKINS_URL') + '/job/' + job_name + '/build'
        response = requests.post(jenkins_url, auth=(jenkins_user, jenkins_user_token))
        return response.status_code == 201

    def list_job(self):
        jenkins_url = os.getenv('JENKINS_URL') + '/api/json'
        response = requests.post(jenkins_url, auth=(jenkins_user, jenkins_user_token))
        job_list = []
        if response.status_code == 200:
            resp_json = response.json()
            for job in resp_json['jobs']:
                if 'test' in job['name'].lower():
                    job_list.append(
                        {
                            'name': job['name'],
                            'url': job['url']
                        }
                    )
        return job_list

    def list_failed_job(self):
        jenkins_url = os.getenv('JENKINS_URL') + '/api/json'
        response = requests.post(jenkins_url, auth=(jenkins_user, jenkins_user_token))
        job_list = []
        if response.status_code == 200:
            resp_json = response.json()
            for job in resp_json['jobs']:
                if job['color'] != 'blue' and 'test' in job['name'].lower():
                    job_list.append(
                        {
                            'name': job['name'],
                            'url': job['url']
                        }
                    )
        return job_list

    def get_build_info(self, job_url, build_no):
        job_url = job_url + '{0}/api/json'.format(build_no)
        response = requests.post(job_url, auth=(jenkins_user, jenkins_user_token))
        build_data = dict()
        resp_json = response.json()
        build_data['job_name'] = str(resp_json['fullDisplayName']).split(' ')[0]
        build_data['build_no'] = resp_json['number']
        build_data['run_at'] = fmt_result.format(rd(datetime.now(), datetime.fromtimestamp(int(resp_json['timestamp']/1000))))
        for action in resp_json['actions']:
            if '_class' in action:
                if 'hudson.model.CauseAction' in action['_class']:
                    build_data['started_by'] = action['causes'][0]['userName']
                    break
        if len(resp_json['changeSets']) == 0:
            build_data['changes'] = 'NO CHANGES'
        else:
            build_data['changes'] = resp_json['changeSets'][0]['items'][0]['msg']
        return build_data

    def get_test_detail_by_name(self, job_url, build_no, test_name):
        test_url = job_url + '/{0}/testReport/api/json'.format(build_no)
        response = requests.post(test_url, auth=(jenkins_user, jenkins_user_token))
        resp_json = response.json()
        for suite in resp_json['suites']:
            for case in suite['cases']:
                if case['name'] == test_name:
                    return case

    def get_test_result(self, job_url, build_no):
        data = self.get_build_info(job_url, build_no)
        job_url_api = job_url + '/{0}/testReport/api/json'.format(data['build_no'])
        response = requests.post(job_url_api, auth=(jenkins_user, jenkins_user_token))
        if response.status_code == 200:
            resp_json = response.json()
            data['duration'] = fmt.format(rd(seconds=int(resp_json['duration'])))
            if resp_json['failCount'] == 0:
                data['header_color'] = "#0ab20d"
                data['test_result'] = "SUCCESS"
                data['hero_image'] = 'https://i0.wp.com/hdsmileys.com/wp-content/uploads/2017/' \
                                     '10/brown-cony-and-sally-dancing.gif'
            else:
                data['header_color'] = "#b20a0a"
                data['test_result'] = "FAILED"
                data['hero_image'] = 'https://i2.wp.com/hdsmileys.com/wp-content/uploads' \
                                     '/2017/10/sally-crying-loudly.gif'
            data['passed'] = resp_json['passCount']
            data['failed'] = resp_json['failCount']
            data['total'] = int(data['passed']) + int(data['failed'])
            data['report_url'] = job_url + '{0}/allure'.format(build_no)
        return data


    def get_failed_tests_video(self, job_url, build_no):
        data = self.get_build_info(job_url, 'lastBuild')
        job_url_api = job_url + '/{0}/testReport/api/json'.format(build_no)
        response = requests.post(job_url_api, auth=(jenkins_user, jenkins_user_token))
        data['failed_cases'] = []
        if response.status_code == 200:
            resp_json = response.json()
            for suite in resp_json['suites']:
                for case in suite['cases']:
                    if case['errorDetails'] != None:
                        data['failed_cases'].append(video_url.format(data['job_name'], data['build_no'], case['name']))
        return data


    def get_test_latest_result(self, job_url):
        data = self.get_build_info(job_url, 'lastBuild')
        job_url_api = job_url + '/lastBuild/testReport/api/json'
        response = requests.post(job_url_api, auth=(jenkins_user, jenkins_user_token))
        if response.status_code == 200:
            resp_json = response.json()
            if resp_json['failCount'] == 0:
                data['header_color'] = "#0ab20d"
                data['test_result'] = "SUCCESS"
            else:
                data['header_color'] = "#b20a0a"
                data['test_result'] = "FAILED"
            data['suites'] = []
            suite_index = 0
            for suite in resp_json['suites']:
                suite_name = suite['cases'][0]['className']
                data['suites'].append(
                    {
                        'suite_name': suite_name,
                        'tests': []
                    }
                )
                for case in suite['cases']:
                    if case['status'].upper() == 'PASSED':
                        status_color = '#2ac12f'
                        status = 'PASSED'
                    else:
                        status_color = '#e8192e'
                        status = 'FAILED'
                    data['suites'][suite_index]['tests'].append(
                        {
                            'test_name': case['name'],
                            'status': status,
                            'status_color': status_color,
                            'duration': case['duration'],
                            'video': video_url.format(data['job_name'], data['build_no'], case['name']),
                            'error': case['errorDetails']
                        }
                    )
                suite_index += 1
        return data



