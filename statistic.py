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

from linebot.models import BubbleContainer
import json


class Statistic(object):

    def generate_test_stat_message(self, data):

        job_name = data['job_name']
        pass_rate_percentage = data['pass_rate_percentage']
        last_success_since = data['last_success_since']

        stat_images_contents = []
        for test_result in data['test_result_history']:
            image = {
                "type": "box",
                "layout": "vertical",
                "contents": [ {
                        "type": "image",
                        "url": test_result['stat_image'],
                        "size": "xxs",
                        "align": "center"
                    },
                    {
                        "type": "text",
                        "text": '#{}'.format(test_result['build_no']),
                        "align": "center"
                    }
                ]            
            }

            stat_images_contents.append(image)

        bubble = {
            "type": "bubble",
            "styles": {
                "header": {
                    "backgroundColor": "#367ced"
                }
            },
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "Test Statistic",
                        "weight": "bold",
                        "color": "#ffffff",
                        "size": "md"
                    }
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": job_name,
                        "weight": "bold",
                        "color": "#1b1c1b",
                        "size": "xl"
                    },
                    {
                        "type": "separator",
                        "margin": "md"
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "margin": "md",
                        "contents": [
                            {
                                "type": "text",
                                "text": "Pass Rate: {}%".format(pass_rate_percentage),
                                "size": "sm",
                                "weight": "bold",
                                "color": "#1b1c1b"
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "margin": "md",
                        "contents": [
                            {
                                "type": "text",
                                "text": "Test Result History:",
                                "size": "sm",
                                "weight": "bold",
                                "color": "#1b1c1b"
                            }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "margin": "md",
                        "contents": stat_images_contents
                    },
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "margin": "md",
                        "contents": [
                            {
                                "type": "text",
                                "text": "Last Success:",
                                "size": "sm",
                                "weight": "bold",
                                "color": "#1b1c1b",
                                "flex": 4
                            },
                            {
                                "type": "text",
                                "text": last_success_since,
                                "wrap": True,
                                "size": "xs",
                                "color": "#1b1c1b",
                                "flex": 6
                            }
                        ]
                    }
                ]
            }
        }

        return BubbleContainer.new_from_json_dict(bubble)
