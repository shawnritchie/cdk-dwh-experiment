from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_iam as iam,
)


class BastionStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # AMI
        amzn_linux = ec2.MachineImage.latest_amazon_linux(
            generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            edition=ec2.AmazonLinuxEdition.STANDARD,
            virtualization=ec2.AmazonLinuxVirt.HVM,
            storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
        )

        i = 1
        for subnet in vpc.stack.vpc.select_subnets(subnet_group_name="BASTION").subnets:
            bastion_host = ec2.BastionHostLinux(self,
                                                f"ec2-BASTION-Instance{i}",
                                                vpc=vpc,
                                                subnet_selection=ec2.SubnetSelection(
                                                    availability_zones=[subnet.availability_zone],
                                                    subnet_group_name="BASTION"
                                                ),
                                                instance_type=ec2.InstanceType("t1.micro"),
                                                machine_image=amzn_linux
                                                )
            bastion_host.allow_ssh_access_from(ec2.Peer.any_ipv4())
            i += 1

        host_admin_group = iam.Group(self,
                                     "HostAdmins",
                                     )

        policy = iam.Policy(self,
                            "HostAdminPolicy",
                            groups=[host_admin_group]
                            )

        policy.add_statements(iam.PolicyStatement(effect=iam.Effect.ALLOW,
                                                  actions=["ec2-instance-connect:SendSSHPublicKey"],
                                                  resources=
                                                  [f"arn:aws:ec2:{self.region}:{self.account}:instance/*"],
                                                  conditions={"StringEquals": {"ec2:osuser": "ec2-user"}}
                                                  ))
