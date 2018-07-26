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


from linebot.models import (
    ButtonsTemplate, PostbackAction
)
from jenkins import Jenkins

jenkins = Jenkins()


class RunTest(object):

    def display_run_test_menu(self):
        """
            Display Job List Menu.
        """
        button_template = ButtonsTemplate()
        button_template.text = 'Please Select The Job'
        job_list = jenkins.list_job()
        button_template.thumbnail_image_url = 'https://images.pexels.com/photos/5933/color-paint-palette-wall-painting.jpg'
        for job in job_list:
            job_name = job['name']
            button_template.actions.append(
                PostbackAction(label=job_name, data='start_test={}'.format(job_name))
            )
        return button_template

    def display_failed_test_menu(self):
        """
            Display Failed Tests Jobs
        """
        button_template = ButtonsTemplate()
        job_list = jenkins.list_failed_job()
        if len(job_list) > 0:
            button_template.text = 'Please Select The Failed Test Jobs'
            button_template.thumbnail_image_url = 'https://res.cloudinary.com/twenty20/private_images/' \
                                                  't_watermark-criss-cross-10/v1436383102000/photosp/' \
                                                  '28530ceb-0a66-4aaa-a795-9dbdabfddd27/stock-photo-' \
                                                  'outdoors-red-book-reading-tiles-failure-fail-better-' \
                                                  'flat-lay-28530ceb-0a66-4aaa-a795-9dbdabfddd27.jpg'
            for job in job_list:
                job_name = job['name']
                button_template.actions.append(
                    PostbackAction(label=job_name, data='rerun_test={}'.format(job_name))
                )
        else:
            button_template.text = 'Congratulations! All Tests are Passed'
            button_template.thumbnail_image_url = 'https://images.pexels.com/photos/941693/pexels-photo-941693.jpeg'
            button_template.actions.append(
                PostbackAction(label='OK', data='OK')
            )
        return button_template

