from aws_cdk import (
    core,
    aws_s3 as s3,
    aws_iam as iam,
    aws_kms as kms,
    aws_kinesis as kinesis,
    aws_s3_deployment as s3_deploy,
    aws_kinesisanalytics as kinesis_analytics,
    aws_logs as logs
)


class FlinkStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, stream: kinesis.Stream, stream_key: kms.Key, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        fat_jar = "payment-digestor-1.0-SNAPSHOT-all.jar"
        path_to_fat_jar = f"../payment-digestor/build/libs/"

        flink_log_group = logs.LogGroup(self,
                                        "FlinkLogGroup",
                                        log_group_name="/aws/kinesis-analytics/FlinkLogGroup",
                                        removal_policy=core.RemovalPolicy.DESTROY,
                                        retention=logs.RetentionDays.THREE_DAYS)
        flink_log_stream = flink_log_group.add_stream("FlinkLogStream", log_stream_name="FlinkLogStream")

        flink_app_bucket = s3.Bucket(self, "FlinkAppBucket")
        flink_fatjar_deployment = s3_deploy.BucketDeployment(self,
                                                             "fat-jar-upload",
                                                             destination_bucket=flink_app_bucket,
                                                             sources=[s3_deploy.Source.asset(path_to_fat_jar)]
                                                             )
        flink_fatjar_deployment.node.add_dependency(flink_app_bucket)

        flink_role = iam.Role(self,
                              "FlinkRole",
                              assumed_by=iam.ServicePrincipal(service="kinesisanalytics.amazonaws.com"),
                              inline_policies={
                                  "flinkPolicy": iam.PolicyDocument(statements=[
                                      iam.PolicyStatement(sid="ReadCode",
                                                          effect=iam.Effect.ALLOW,
                                                          actions=["s3:GetObject",
                                                                   "s3:GetObjectVersion"],
                                                          resources=[f"{flink_app_bucket.bucket_arn}/*"]
                                                          ),
                                      iam.PolicyStatement(sid="ListCloudwatchLogGroups",
                                                          effect=iam.Effect.ALLOW,
                                                          actions=["logs:DescribeLogGroups"],
                                                          resources=[
                                                              f"arn:aws:logs:{self.region}:{self.account}:log-group:*"]
                                                          ),
                                      iam.PolicyStatement(sid="ListCloudwatchLogStreams",
                                                          effect=iam.Effect.ALLOW,
                                                          actions=["logs:DescribeLogStreams"],
                                                          resources=[
                                                              f"arn:aws:logs:{self.region}:{self.account}:log-group:{flink_log_group.log_group_name}:log-stream:*"]
                                                          ),
                                      iam.PolicyStatement(sid="PutCloudwatchLogs",
                                                          effect=iam.Effect.ALLOW,
                                                          actions=["logs:PutLogEvents","logs:PutMetricData"],

                                                          resources=[
                                                              f"arn:aws:logs:{self.region}:{self.account}:log-group:{flink_log_group.log_group_name}:log-stream:{flink_log_stream.log_stream_name}"
                                                          ]
                                                          ),
                                      iam.PolicyStatement(sid="DecryptStream",
                                                          effect=iam.Effect.ALLOW,
                                                          actions=["kms:*"],
                                                          resources=[stream_key.key_arn]
                                                          ),
                                      iam.PolicyStatement(sid="ReadWriteInputStream",
                                                          effect=iam.Effect.ALLOW,
                                                          actions=["kinesis:DescribeStream",
                                                                   "kinesis:GetShardIterator",
                                                                   "kinesis:GetRecords",
                                                                   "kinesis:ListShards",
                                                                   "kinesis:PutRecords"],
                                                          resources=[stream.stream_arn]
                                                          )
                                  ])
                              })

        flink_app = kinesis_analytics.CfnApplicationV2(self,
                                                       id,
                                                       application_name='PaymentDigestor',
                                                       runtime_environment="FLINK-1_8",
                                                       service_execution_role=flink_role.role_arn,
                                                       application_configuration={
                                                           "applicationCodeConfiguration": {
                                                               "codeContent": {
                                                                   "s3ContentLocation": {
                                                                       "bucketArn": flink_app_bucket.bucket_arn,
                                                                       "fileKey": fat_jar
                                                                   }
                                                               },
                                                               "codeContentType": "ZIPFILE"
                                                           },
                                                           "flinkApplicationConfiguration": {
                                                               "monitoringConfiguration": {
                                                                   "configurationType": "CUSTOM",
                                                                   "logLevel": "INFO",
                                                                   "metricsLevel": "TASK"
                                                               }
                                                           },
                                                           "applicationSnapshotConfiguration": {
                                                               "snapshotsEnabled": True
                                                           }
                                                       })
        flink_app.node.add_dependency(flink_fatjar_deployment)

        flink_log_group_arn = f"arn:aws:logs:{self.region}:{self.account}:log-group:{flink_log_group.log_group_name}:log-stream:{flink_log_stream.log_stream_name}"
        flink_log_group = kinesis_analytics.CfnApplicationCloudWatchLoggingOptionV2(self,
                                                                                    "flinkLogGroup",
                                                                                    application_name=flink_app.ref,
                                                                                    cloud_watch_logging_option={
                                                                                        "logStreamArn": flink_log_group_arn
                                                                                    })


