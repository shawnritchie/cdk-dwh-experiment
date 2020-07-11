from aws_cdk import (
    core,
    aws_kinesis as kinesis,
    aws_iam as iam,
    aws_ec2 as ec2,
    aws_kms as kms
)


class KinesisStreamStack(core.Stack):

    @property
    def kinesis_stream(self):
        return self._kinesis_stream

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        kms_policy = iam.PolicyDocument()
        kms_policy.add_statements(
            iam.PolicyStatement(effect=iam.Effect.ALLOW,
                                actions=["kms:*"],
                                resources=['*'],
                                principals=[iam.AccountPrincipal(account_id=self.account)]
                                )
        )

        kinesis_key = kms.Key(self,
                               "volumeKey",
                               enable_key_rotation=True,
                               policy=kms_policy,
                               removal_policy=core.RemovalPolicy.RETAIN
                               )

        self._kinesis_stream = kinesis.Stream(self,
                                              id,
                                              encryption_key=kinesis_key,
                                              retention_period=core.Duration.hours(24),
                                              shard_count=1,
                                              stream_name="PaymentStream"
                                              )