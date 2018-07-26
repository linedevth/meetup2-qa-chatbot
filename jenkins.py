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

import requests
import os

jenkins_user = os.getenv('JENKINS_USER')
jenkins_user_token = os.getenv('JENKINS_USER_TOKEN')


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
                if job['color'] == 'red':
                    job_list.append(
                        {
                            'name': job['name'],
                            'url': job['url']
                        }
                    )
        return job_list
