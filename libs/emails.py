# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
import requests
from django.conf import settings


def send_email(to_email, subject="", html="", from_email="zoneke.ccy@gmail.com", files=None, **kwargs):
    #send_email_by_sendcloud(to_email, subject, html, from_email, **kwargs)
    bcc = settings.EMAIL_TO
    kwargs['bcc'] = bcc
    return send_email_by_mailgun(to_email, subject, html, from_email, files=files, **kwargs)


def send_email_by_sendcloud(to_email, subject="", html="", from_email="zoneke.ccy@gmail.com", files=None, **kwargs):
    url = "https://sendcloud.sohu.com/webapi/mail.send.xml"
    params = {
        "api_user": "postmaster@zoneke.sendcloud.org",
        "api_key": "Rdtk4b9f",
        "from": from_email,
        "to": to_email,
        "subject": subject,
        "html": html,
        }
    params.update(kwargs)
    return requests.post(url, data=params)


def send_email_by_mailgun(to_email, subject, html, from_email="zoneke.ccy@gmail.com", files=None, **kwargs):
    data = {"from": from_email,
            "to": to_email.split(";"),
            "subject": subject,
            "html": html}
    data.update(kwargs)
    if files:
        return requests.post(
            "https://api.mailgun.net/v2/zoneke.com/messages",
            auth=("api", "key-1t13ykjl8haxzxlxo99q4aoraj3u8hk2"),
            data=data,
            files=files
        )
    return requests.post(
        "https://api.mailgun.net/v2/zoneke.com/messages",
        auth=("api", "key-1t13ykjl8haxzxlxo99q4aoraj3u8hk2"),
        data=data
    )


def test():
    from_email = "zoneke.ccy@gmail.com"
    to_email = "chenchiyuan03@gmail.com"
    subject = "这是测试邮件"
    html = "Hello World"
    send_email(from_email, to_email, subject, html)