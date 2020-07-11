from aws_cdk import (
    core,
    aws_redshift as redshift,
    aws_iam as iam,
    aws_ec2 as ec2,
    aws_kms as kms,
    aws_s3 as s3
)


class RedshiftStack(core.Stack):

    @property
    def cluster(self):
        return self._cluster

    def __init__(self, scope: core.Construct, id: str, vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        kms_policy = iam.PolicyDocument()
        kms_policy.add_statements(
            iam.PolicyStatement(effect=iam.Effect.ALLOW,
                                actions=["kms:*"],
                                resources=['*'],
                                principals=[iam.AccountPrincipal(account_id=self.account)]
                                )
        )

        redshift_key = kms.Key(self,
                               "volumeKey",
                               enable_key_rotation=True,
                               policy=kms_policy,
                               removal_policy=core.RemovalPolicy.RETAIN
                               )

        redshift_bucket = s3.Bucket(self, "redshiftBucket")
        redshift_bucket.add_to_resource_policy(
            permission=iam.PolicyStatement(effect=iam.Effect.ALLOW,
                                           actions=["s3:*"],
                                           resources=[f"{redshift_bucket.bucket_arn}/*",
                                                      redshift_bucket.bucket_arn],
                                           principals=[iam.ArnPrincipal(f"arn:aws:iam::193672423079:user/logs")]
                                           )
        )

        self._cluster = redshift.Cluster(self,
                                         id,
                                         master_user=redshift.Login(master_username="root",
                                                              encryption_key=redshift_key
                                                              ),
                                         port=5439,
                                         vpc=vpc,
                                         cluster_name="dwh",
                                         cluster_type=redshift.ClusterType.MULTI_NODE,
                                         number_of_nodes=2,
                                         default_database_name="aml",
                                         encrypted=True,
                                         encryption_key=redshift_key,
                                         logging_bucket=redshift_bucket,
                                         logging_key_prefix="dwh",
                                         node_type=redshift.NodeType.DC2_LARGE,
                                         removal_policy=core.RemovalPolicy.DESTROY,
                                         security_groups=[self.redshift_sg(vpc)],
                                         vpc_subnets=ec2.SubnetSelection(subnet_group_name="DBS")
                                         )

    def redshift_sg(self, vpc):
        private_security_group = ec2.SecurityGroup(self,
                                                   id='redshift_security_group',
                                                   vpc=vpc,
                                                   allow_all_outbound=False
                                                   )
        private_security_group.add_ingress_rule(ec2.Peer.ipv4(vpc.vpc_cidr_block),
                                                ec2.Port.tcp(5439),
                                                'allow all vpc traffic'
                                                )
        private_security_group.add_egress_rule(ec2.Peer.ipv4(vpc.vpc_cidr_block),
                                               ec2.Port.all_traffic(),
                                               'allow all internal requests'
                                               )
        return private_security_group
