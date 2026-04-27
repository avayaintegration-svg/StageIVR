import boto3 

def initKB():
    agent_client = boto3.client("bedrock-agent-runtime", region_name="us-east-1")
    return agent_client