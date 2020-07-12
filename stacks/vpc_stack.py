from aws_cdk import (
    core,
    aws_ec2 as ec2
)


class VpcStack(core.Stack):
    @property
    def vpc(self):
        return self._vpc

    def __init__(self, scope: core.Construct, id: str, vpc_cidr: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self._vpc = ec2.Vpc(self,
                    id,
                    cidr=vpc_cidr,
                    enable_dns_hostnames=True,
                    enable_dns_support=True,
                    max_azs=2,
                    subnet_configuration=[ec2.SubnetConfiguration(
                        subnet_type=ec2.SubnetType.PUBLIC,
                        name="BASTION",
                        cidr_mask=24
                    ), ec2.SubnetConfiguration(
                        subnet_type=ec2.SubnetType.PRIVATE,
                        name="ECS",
                        cidr_mask=24
                    ), ec2.SubnetConfiguration(
                        subnet_type=ec2.SubnetType.PUBLIC,
                        name="DBS",
                        cidr_mask=24
                    )
                    ],
                    nat_gateway_provider=ec2.NatProvider.gateway(),
                    nat_gateway_subnets=ec2.SubnetSelection(
                        one_per_az=True,
                        subnet_group_name="BASTION"
                    ),
                    gateway_endpoints={
                        's3': ec2.GatewayVpcEndpointOptions(
                            service=ec2.GatewayVpcEndpointAwsService.S3,
                            subnets=[
                                ec2.SubnetSelection(
                                    one_per_az=True,
                                    subnet_type=ec2.SubnetType.PUBLIC
                                )
                            ]
                        )
                    }
                    )