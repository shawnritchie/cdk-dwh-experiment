from aws_cdk import (
    core,
    aws_iam as iam,
    aws_ecr as ecr
)


class ComputeStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        flink_app_repo = ecr.Repository(self,
                                        id,
                                        removal_policy=core.RemovalPolicy.DESTROY,
                                        repository_name="flinkApp"
                                        )

        flink_app_repo.add_lifecycle_rule(max_image_count=1)

        flink_app_repo.add_to_resource_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=["ecr:GetDownloadUrlForLayer",
                     "ecr:BatchGetImage",
                     "ecr:BatchCheckLayerAvailability",
                     "ecr:GetAuthorizationToken"],
            principals=[iam.ServicePrincipal(service="ecs.amazonaws.com"),
                        iam.ServicePrincipal(service="ecs-tasks.amazonaws.com")],
        ))

        flink_app_repo.add_to_resource_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=["ecr:GetDownloadUrlForLayer",
                     "ecr:BatchGetImage",
                     "ecr:BatchCheckLayerAvailability",
                     "ecr:PutImage",
                     "ecr:InitiateLayerUpload",
                     "ecr:UploadLayerPart",
                     "ecr:CompleteLayerUpload"],
            principals=[iam.AccountPrincipal(account_id=self.account)]
        ))

        flink_app_repo.add_to_resource_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=["ecr:ListImages"],
            principals=[iam.AnyPrincipal()]
        ))
