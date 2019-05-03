# -*- coding: utf-8 -*-
import boto3
sns = boto3.client('sns')
number = '+880.......'
sns.publish(PhoneNumber = number, Message='Room: pass:' )
