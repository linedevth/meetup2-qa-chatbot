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
    BubbleContainer, CarouselContainer
)
import json
from jenkins import video_url


class TestResult(object):

    def generate_test_result_message(self, data):
        bubble = {
            "type": "bubble",
            "styles": {
                "header": {
                    "backgroundColor": data['header_color']
                }
            },
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "Test Result: {0}".format(data['test_result']),
                        "weight": "bold",
                        "color": "#ffffff",
                        "size": "md"
                    }
                ]
            },
            "hero": {
                "type": "image",
                "url": data['hero_image'],
                "size": "md"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": data['job_name'],
                        "weight": "bold",
                        "size": "xl"
                    },
                    {
                        "type": "text",
                        "text": "Build#{0} ({1})".format(data['build_no'], data['duration']),
                        "size": "xs",
                        "color": "#aaaaaa",
                        "wrap": True
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
                                "text": "Changes:",
                                "size": "xs",
                                "weight": "bold",
                                "color": "#1b1c1b",
                                "flex": 3
                            },
                            {
                                "type": "text",
                                "text": data['changes'],
                                "size": "xs",
                                "color": "#1b1c1b",
                                "flex": 6
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
                                "text": "Started By:",
                                "size": "xs",
                                "weight": "bold",
                                "color": "#1b1c1b",
                                "flex": 4
                            },
                            {
                                "type": "text",
                                "text": data['started_by'],
                                "size": "xs",
                                "color": "#1b1c1b",
                                "flex": 7
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
                                "text": "Passed/Failed/Total: ",
                                "size": "xs",
                                "weight": "bold",
                                "color": "#1b1c1b",
                                "flex": 7
                            },
                            {
                                "type": "text",
                                "text": "{0}/{1}/{2}".format(data['passed'], data['failed'], data['total']),
                                "size": "xs",
                                "color": "#1b1c1b",
                                "flex": 4
                            }
                        ]
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "button",
                        "style": "link",
                        "action": {
                            "type": "uri",
                            "label": "Test Report",
                            "uri": data['report_url']
                        }
                    }
                ]
            }
        }

        return BubbleContainer.new_from_json_dict(bubble)

    def generate_latest_result(self, data):
        carousel = CarouselContainer()
        for suite in data['suites']:
            bubble = {
                "type": "bubble",
                "styles": {
                    "header": {
                        "backgroundColor": data["header_color"]
                    }
                },
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": data["job_name"],
                            "color": "#000000",
                            "size": "lg",
                            "weight": "bold"
                        },
                        {
                            "type": "text",
                            "text": "Build#{0}, {1}".format(data["build_no"], data['run_at']),
                            "color": "#000000",
                            "size": "xs"
                        }
                    ]
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "md",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": suite['suite_name'],
                                    "size": "xs"
                                }
                            ]
                        },
                        {
                            "type": "separator"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": []
                        }
                    ]
                }
            }
            bubble_test_contents = bubble['body']['contents'][2]['contents']
            for test in suite['tests']:
                bubble_test_contents.append(
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": test["test_name"],
                                "size": "sm",
                                "wrap": True,
                                "flex": 4,
                                "action": {
                                    "type": "postback",
                                    "data": "video={0}&name={1}".format(video_url.format(data['job_name'], data["build_no"], test["test_name"]), test["test_name"])
                                }
                            },
                            {
                                "type": "text",
                                "text": test["status"],
                                "color": test['status_color'],
                                "size": "xs",
                                "align": "end"
                            }
                        ]
                    }
                )
            bubble_container = BubbleContainer.new_from_json_dict(bubble)
            carousel.contents.append(bubble_container)
        return carousel

