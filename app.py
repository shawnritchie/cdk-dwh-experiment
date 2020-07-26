#!/usr/bin/env python3

from aws_cdk import core

from stacks.bastion_stack import BastionStack
from stacks.compute_stack import ComputeStack
from stacks.flink_stack import FlinkStack
from stacks.kinesis_firehose_stack import KinesisFirehoseStack
from stacks.kinesis_stream_stack import KinesisStreamStack
from stacks.payment_simulation_lamba_stack import PaymentSimulationLambdaStack
from stacks.redshift_stack import RedshiftStack
from stacks.vpc_stack import VpcStack

app = core.App()
vpc_stack = VpcStack(app, "vpc-stack", "10.1.0.0/16", env={"region": "us-east-1"})
bastion_stack = BastionStack(app, "bastion-stack", vpc_stack.vpc, env={"region": "us-east-1"})
redshift_stack = RedshiftStack(app, "redshift-stack", vpc_stack.vpc, env={"region": "us-east-1"})
kinesis_stream_stack = KinesisStreamStack(app, "kinesis-stream-stack", env={"region": "us-east-1"})
kinesis_firehose_stack = KinesisFirehoseStack(app, "kinesis-firehose-stack",
                                              kinesis_stream_stack.kinesis_stream,
                                              kinesis_stream_stack.kinesis_key,
                                              redshift_stack.cluster,
                                              env={"region": "us-east-1"})
payment_simulation_lambda_stack = PaymentSimulationLambdaStack(app,
                                                               "payment-simulation-lambda-stack",
                                                               kinesis_stream_stack.kinesis_stream,
                                                               kinesis_stream_stack.kinesis_key,
                                                               env={"region": "us-east-1"})
compute_stack = ComputeStack(app, "compute-stack", env={"region": "us-east-1"})
flink_stack = FlinkStack(app,
                         "flink-stack",
                         kinesis_stream_stack.kinesis_stream,
                         kinesis_stream_stack.kinesis_key,
                         env={"region": "us-east-1"})

app.synth()
