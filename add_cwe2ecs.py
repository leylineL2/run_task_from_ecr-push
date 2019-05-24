import boto3

isAssignPublicIp = 'ENABLED'

def AddCloudWatchEventTargets(StackName):
    cloudformation = boto3.client('cloudformation',region_name='ap-northeast-1')
    events = boto3.client('events',region_name='ap-northeast-1')
    stack = cloudformation.describe_stacks(StackName=StackName)
    StackDetailDict = {}
    for outputs in stack['Stacks'][0]["Outputs"]:
        outputList = list(outputs.values())
        StackDetailDict[outputList[0]] = outputList[1]
    print(StackDetailDict)
    Rule = StackDetailDict['EventRule']

    print(hoge)
    Targets = {
        'Arn': StackDetailDict['Cluster'],
        'Id': 'deploy-ecs-target',
        'RoleArn':StackDetailDict['IAMRole'],
        'EcsParameters':{
            'TaskDefinitionArn': StackDetailDict['TaskDefinition'][:-2], # remove revision num
            'TaskCount':1,
            'PlatformVersion': 'LATEST',
            'LaunchType': 'FARGATE',
            'NetworkConfiguration':{
                'awsvpcConfiguration':{
                    'Subnets':['{SubnetIds}'.format(**StackDetailDict)],
                    'AssignPublicIp':isAssignPublicIp,
                    'SecurityGroups': [StackDetailDict['SecurityGroup']]
                }
            }
        }
    }
    print(Targets)
    eventResult = events.put_targets(
        Rule = Rule,
        Targets=[Targets]
    )
    print(eventResult)

if __name__ == "__main__":
    StackNameList = ['MigrationDeployStack']
    for StackName in StackNameList:
        AddCloudWatchEventTargets(StackName)
