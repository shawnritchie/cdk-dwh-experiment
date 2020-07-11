#!/usr/bin/env python3

from aws_cdk import core

from stacks.bastion_stack import BastionStack
from stacks.kinesis_firehose_stack import KinesisFirehoseStack
from stacks.kinesis_stream_stack import KinesisStreamStack
from stacks.redshift_stack import RedshiftStack
from stacks.vpc_stack import VpcStack

app = core.App()
vpc_stack = VpcStack(app, "vpc-stack", "10.1.0.0/16", env={"region": "us-east-1"})
bastion_stack = BastionStack(app, "bastion-stack", vpc_stack.vpc, env={"region": "us-east-1"})
redshift_stack = RedshiftStack(app, "redshift-stack", vpc_stack.vpc, env={"region": "us-east-1"})
kinesis_stream_stack = KinesisStreamStack(app, "kinesis-stream-stack", env={"region": "us-east-1"})
kinesis_firehose_stack = KinesisFirehoseStack(app, "kinesis-firehose-stack", kinesis_stream_stack.kinesis_stream,
                                              redshift_stack.cluster, env={"region": "us-east-1"})

app.synth()
