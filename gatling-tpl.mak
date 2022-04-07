# Makefile for Gatling container
REG_ID=ZZ-REG-ID
CREG=ZZ-CR-ID

GATLING_VER=3.4.2
IMAGE_NAME=$(CREG)/scp-2021-jan-cmpt-756/gatling:$(GATLING_VER)

DIR=.
# Convert relative pathname to absolute
ABS_DIR=$(realpath $(DIR))

CLUSTER_IP=NONE
USERS=1
SIM_NAME=ReadUserSim
SIM_PROJECT=proj756
SIM_FULL_NAME=$(SIM_PROJECT).$(SIM_NAME)

build:
	docker image build -t $(IMAGE_NAME) .

run:
	docker container run --detach --rm \
		-v ${ABS_DIR}/gatling/results:/opt/gatling/results \
		-v ${ABS_DIR}/gatling:/opt/gatling/user-files \
		-v ${ABS_DIR}/gatling/target:/opt/gatling/target \
		-e CLUSTER_IP=${CLUSTER_IP} \
		-e USERS=${USER} \
		-e SIM_NAME=${SIM_NAME} \
		--label gatling \
		${IMAGE_NAME} \
		-s ${SIM_FULL_NAME} > gatling-tmp.log

	@echo "Control-C to end output when you have seen enough."
	@echo "To stop the Gatling job, enter"
	@echo "   $ kill tools/gatling.sh $!"
	@echo "The Gatling job will continue running until it is stopped or"
	@echo "the container is exited."

	docker container logs `cat gatling-tmp.log` --follow

