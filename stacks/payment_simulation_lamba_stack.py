from aws_cdk import (
    core,
    aws_iam as iam,
    aws_kms as kms,
    aws_kinesis as kinesis,
    aws_lambda as _lambda,
    aws_events as events,
    aws_events_targets as targets
)


class PaymentSimulationLambdaStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, stream: kinesis.Stream, stream_key: kms.Key, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        payment_simulator_role = iam.Role(self,
                                          "paymentSimulatorRole",
                                          assumed_by=iam.ServicePrincipal(service="lambda.amazonaws.com"),
                                          inline_policies={
                                              "paymentSimulatorPolicy": iam.PolicyDocument(statements=[
                                                  iam.PolicyStatement(effect=iam.Effect.ALLOW,
                                                                      actions=["kinesis:*"],
                                                                      resources=[stream.stream_arn]
                                                                      ),
                                                  iam.PolicyStatement(effect=iam.Effect.ALLOW,
                                                                      actions=["logs:*"],
                                                                      resources=[f"arn:aws:logs:{self.region}:{self.account}:*"]
                                                                      ),
                                                  iam.PolicyStatement(effect=iam.Effect.ALLOW,
                                                                      actions=["kms:*"],
                                                                      resources=[stream_key.key_arn]
                                                                      )
                                              ])
                                          })

        payment_lambda = _lambda.Function(self,
                                          id,
                                          runtime=_lambda.Runtime.PYTHON_3_7,
                                          handler="payment_activity_simulator.handler",
                                          code=_lambda.Code.from_asset("lambda/"),
                                          role=payment_simulator_role,
                                          timeout=core.Duration.minutes(5)
                                          )

        rule = events.Rule(
            self, "Rule",
            schedule=events.Schedule.cron(
                minute='3',
                hour='*',
                month='*',
                week_day='*',
                year='*'),
        )

        input_event = events.RuleTargetInput.from_object(dict(requestId="PaymentSimulatorEventRuleCron"))
        rule.add_target(targets.LambdaFunction(payment_lambda, event=input_event))
