"""This lambda function reads a message from an SQS Queue in AWS, Passes it to a step machine, and then deletes the
Message when we have succesfully started our state machine"""


import json
import boto3
import logging
import os

logger = logging.getLogger()
logging.getLogger().setLevel(logging.INFO)
account_number = os.environ["acc_num"]
statemachine_name = os.environ["state_machine"]
aws_region = os.environ["region"]


def dict_to_json(dict_to_convert: dict):
    """returns a json string from a python dictionary for sqs message
    :param dict_to_convert: python dictionary to convert """
    logging.info("attempting to convert python dictionary to a string")
    sqs_message = json.dumps(dict_to_convert)
    return sqs_message


def start_state_machine(state_machine_arn:str, sqs_message:str):
    """starts specified state machine passing the sqs_message to the step function
    :param state_machine_arn: is the arn of the state machine we want to start
    :param sqs_message message: from sqs we want to pass to the the state machine
    :return response from starting the state machine
    """

    client = boto3.client('stepfunctions')
    logging.info('attempting to start the state machine')
    response = client.start_execution(
        stateMachineArn=state_machine_arn,
        input=sqs_message)
    logging.info(response)
    logging.info('state machine started successfully')
    return response


def sqs_source_arn_to_QueueUrl(eventSourceARN:str):
    """retreives the QueueName and QueueOwnerAWSAccountId from the sqs message and converts it to QueueUrl for the
     delete_sqs_message method
    :param eventSourceARN: the eventSource coming from the SQS Message
    :return QueueUrl: sqs Queue URL
    """
    client = boto3.client('sqs')
    logging.info('parsing the eventSourceARN from the sqs message...')
    split_eventSourceARN = eventSourceARN.split(':')
    QueueName = split_eventSourceARN[5]
    QueueOwnerAWSAccountId = split_eventSourceARN[4]
    logging.info('getting the queue_url from the get_queue_url boto3 function')
    logging.info(QueueName)
    logging.info(QueueOwnerAWSAccountId)
    response = client.get_queue_url(QueueName=QueueName, QueueOwnerAWSAccountId=QueueOwnerAWSAccountId)
    logging.info('queue_url retrieved successfully')
    QueueUrl = response['QueueUrl']
    logging.info(QueueUrl)
    logging.info(f"the QueueUrl = {QueueUrl}")
    return QueueUrl


def delete_sqs_message(QueueUrl:str, ReceiptHandle:str):
    """deletes a message from a SQS Queue
    :param QueueUrl: the url of the queue
    :param ReceiptHandle: ReceiptHandle passed by the sqs message"""
    client = boto3.client('sqs')
    try:
        response = client.delete_message(
            QueueUrl=QueueUrl,
            ReceiptHandle=ReceiptHandle)
    except:
        logging.error("failed to do delete message from the queue")
    logging.info("message deleted succesfully from the queue")



def lambda_handler(event, context):

    record = event['Records'][0]
    receiptHandle = record['receiptHandle']  # name of the ReceiptHandle provided by SQS Function
    logging.info(f"the receiptHandle= {receiptHandle}")
    eventSource = record['eventSourceARN']  # name of the event source
    logging.info(f"the eventSource = eventSource")
    sqs_message = dict_to_json(event)
    start_state_machine(f"arn:aws:states:{aws_region}:{account_number}:stateMachine:{statemachine_name}", sqs_message)
    QueueUrl = sqs_source_arn_to_QueueUrl(eventSource)
    delete_sqs_message(QueueUrl, receiptHandle)