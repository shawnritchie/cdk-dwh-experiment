from aws_cdk import (
    core,
    aws_iam as iam,
    aws_s3 as s3,
    aws_kms as kms,
    aws_redshift as redshift,
    aws_kinesis as kinesis,
    aws_kinesisfirehose as firehose,
    aws_s3_deployment as s3_deploy
)


class KinesisFirehoseStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, stream: kinesis.Stream, stream_key: kms.Key,
                 redshift: redshift.Cluster, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        firehouse_bucket = s3.Bucket(self, "firehoseBucket")
        s3_deploy.BucketDeployment(self,
                                   "firehose-jsonpath",
                                   destination_bucket=firehouse_bucket,
                                   sources=[s3_deploy.Source.asset("firehose/")]
                                   )

        firehose_role = iam.Role(self,
                                 "firehoseRole",
                                 assumed_by=iam.ServicePrincipal(service="firehose.amazonaws.com"),
                                 external_id=self.account,
                                 inline_policies={
                                     "firehosePolicy": iam.PolicyDocument(statements=[
                                         iam.PolicyStatement(effect=iam.Effect.ALLOW,
                                                             actions=["s3:AbortMultipartUpload",
                                                                      "s3:GetBucketLocation",
                                                                      "s3:GetObject",
                                                                      "s3:ListBucket",
                                                                      "s3:ListBucketMultipartUploads",
                                                                      "s3:PutObject"],
                                                             resources=[f"{firehouse_bucket.bucket_arn}/*",
                                                                        firehouse_bucket.bucket_arn]
                                                             ),
                                         iam.PolicyStatement(effect=iam.Effect.ALLOW,
                                                             actions=["kms:*"],
                                                             resources=[stream_key.key_arn]
                                                             ),
                                         iam.PolicyStatement(effect=iam.Effect.ALLOW,
                                                             actions=["kinesis:DescribeStream",
                                                                      "kinesis:GetShardIterator",
                                                                      "kinesis:GetRecords",
                                                                      "kinesis:ListShards"],
                                                             resources=[stream.stream_arn]
                                                             ),
                                         iam.PolicyStatement(effect=iam.Effect.ALLOW,
                                                             actions=["logs:putLogEvents"],
                                                             resources=[
                                                                 f"arn:aws:logs:{self.region}:{self.account}:log-group:*:log-stream:*"]
                                                             ),
                                     ])
                                 })

        # CDK does not enable loggin from the primitive type has to be done manually
        firehose.CfnDeliveryStream(self,
                                   id,
                                   delivery_stream_name="PaymentStream",
                                   delivery_stream_type="KinesisStreamAsSource",
                                   kinesis_stream_source_configuration={
                                       "kinesisStreamArn": stream.stream_arn,
                                       "roleArn": firehose_role.role_arn
                                   },
                                   redshift_destination_configuration={
                                       "clusterJdbcurl": f"jdbc:redshift://{redshift.cluster_endpoint.hostname}:5439/aml",
                                       "username": redshift.secret.secret_value_from_json("username").to_string(),
                                       "password": redshift.secret.secret_value_from_json("password").to_string(),
                                       "copyCommand": {
                                           "copyOptions": "json 'auto'",
                                           "dataTableColumns": "event_created,event_type,event_json_data",
                                           "dataTableName": "payments"
                                       },
                                       "roleArn": firehose_role.role_arn,
                                       "s3Configuration": {
                                           "bucketArn": firehouse_bucket.bucket_arn,
                                           "bufferingHints": {
                                               "intervalInSeconds": 60,
                                               "sizeInMBs": 60,
                                           },
                                           "compressionFormat": "UNCOMPRESSED",
                                           "prefix": "payments/",
                                           "roleArn": firehose_role.role_arn
                                       }
                                   }
                                   )

# create table payments (
#   event_created timestamp not null,
#   event_dw_regdate timestamp default GETDATE(),
#   event_type varchar(200) not null,
#   event_json_data varchar(65535) not null
# );
