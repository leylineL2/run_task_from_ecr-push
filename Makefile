AccountId = $(shell aws sts get-caller-identity --output text --query 'Account')

.PHONY: EcrPushStack
EcrPushStack: deploy/packaged.yml
	aws cloudformation deploy --template-file $< --stack-name $@ --capabilities CAPABILITY_IAM
	python add_cwe2ecs.py

deploy/packaged.yml: cloudformation/main.yml cloudformation/TaskDefinition.yml cloudformation/components/ECR.yml
	@echo Updatefile $?
	@echo Createing $@...
		mkdir -p $(dir deploy)
	aws cloudformation package --s3-bucket $(Bucket) --template-file $< --output-template-file $@
