# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from aws_cdk import (
    aws_iam as iam,
    aws_lambda as _lambda,
    aws_dynamodb as ddb,
    aws_lambda_event_sources as lambdaevent,
    aws_appsync as appsync,
    core
)
import boto3

class SecondaryRegionStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, primary: bool, primary_region: str, secondary_region: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # =============================================================================================
        #           INPUTS
        # =============================================================================================
        # The stack depends on the ARN of the Stream for the Global Table created in the Primary Region
        # We retrieve this using the AWS SDK
        
        client = boto3.client('dynamodbstreams', region_name=secondary_region)

        response = client.list_streams(
            TableName='GlobalDDBTableForAppSync',
            Limit=1
            )
        global_table_stream_arn = response['Streams'][0]['StreamArn']

        # =============================================================================================
        #           DYNAMO DB GLOBAL TABLE
        # =============================================================================================
        # Since we intend to use tableStreamArn we must use Table.fronTableAttributes method
        globaltable = ddb.Table.from_table_attributes(
            self,
            'GlobalTable',
            table_name="GlobalDDBTableForAppSync",
            table_stream_arn = global_table_stream_arn
        )

         # =============================================================================================
        #           IAM
        # =============================================================================================
        lambdaexecutionrole = iam.Role(
           self, 'LambdaExecutionRole',
           assumed_by = iam.ServicePrincipal('lambda.amazonaws.com'),
           managed_policies = [iam.ManagedPolicy.from_aws_managed_policy_name('AWSAppSyncInvokeFullAccess')]
        )

        # =============================================================================================
        #           APPSYNC API
        # =============================================================================================
        api = appsync.GraphqlApi(self, 'SydneyGQLSchemaID',
            schema = appsync.Schema.from_asset('appsync/schema.graphql'),
            name='SydneyGQLSchema',
            authorization_config = appsync.AuthorizationConfig(
                default_authorization = appsync.AuthorizationMode(
                    authorization_type = appsync.AuthorizationType.API_KEY
                )
            ),
        )

        ddbdatasource = api.add_dynamo_db_data_source('DynamoDataSource', globaltable)
        nonedatasource = api.add_none_data_source('RealTimeData')

        # Define resolvers
        ddbdatasource.create_resolver(
            type_name = 'Mutation',
            field_name = 'createItemsModel',
            request_mapping_template = appsync.MappingTemplate.from_file('appsync/resolvers/Mutation.CreateItemsModel.req.vtl'),
            response_mapping_template = appsync.MappingTemplate.from_file('appsync/resolvers/Mutation.CreateItemsModel.resp.vtl')
        )

        ddbdatasource.create_resolver(
            type_name = 'Mutation',
            field_name = 'deleteItemsModel',
            request_mapping_template = appsync.MappingTemplate.from_file('appsync/resolvers/Mutation.DeleteItemsModel.req.vtl'),
            response_mapping_template = appsync.MappingTemplate.from_file('appsync/resolvers/Mutation.DeleteItemsModel.resp.vtl')
        )

        ddbdatasource.create_resolver(
            type_name = 'Mutation',
            field_name = 'updateItemsModel',
            request_mapping_template = appsync.MappingTemplate.from_file('appsync/resolvers/Mutation.UpdateItemsModel.req.vtl'),
            response_mapping_template = appsync.MappingTemplate.from_file('appsync/resolvers/Mutation.UpdateItemsModel.resp.vtl')
        )

        nonedatasource.create_resolver(
            type_name = 'Mutation',
            field_name = 'publishItemsModel',
            request_mapping_template = appsync.MappingTemplate.from_file('appsync/resolvers/Mutation.PublishItemsModel.req.vtl'),
            response_mapping_template = appsync.MappingTemplate.from_file('appsync/resolvers/Mutation.PublishItemsModel.resp.vtl')
        )

        ddbdatasource.create_resolver(
            type_name = 'Query',
            field_name = 'getItemsModel',
            request_mapping_template = appsync.MappingTemplate.from_file('appsync/resolvers/Query.GetItemsModel.req.vtl'),
            response_mapping_template = appsync.MappingTemplate.from_file('appsync/resolvers/Query.GetItemsModel.resp.vtl')
        )

        ddbdatasource.create_resolver(
            type_name = 'Query',
            field_name = 'listItemsModel',
            request_mapping_template = appsync.MappingTemplate.from_file('appsync/resolvers/Query.ListItemsModel.req.vtl'),
            response_mapping_template = appsync.MappingTemplate.from_file('appsync/resolvers/Query.ListItemsModel.resp.vtl')
        )

        # =============================================================================================
        #           LAMBDA FUNCTION
        # =============================================================================================
        # Define the Lambda 'Stream Processor Function'
        my_lambda = _lambda.Function(
            self, 'StreamProcessorFunction',
            runtime=_lambda.Runtime.NODEJS_14_X,
            code=_lambda.Code.from_asset('lambdacode/Archive.zip'),
            handler='exports.handler',
            role = lambdaexecutionrole,
            environment = {
                "AppSyncAPIEndpoint" : api.graphql_url,
                "AppSyncAPIKey": api.api_key
            }
        )

        my_lambda.add_event_source(lambdaevent.DynamoEventSource(globaltable, starting_position=_lambda.StartingPosition.TRIM_HORIZON))

        # =============================================================================================
        #           OUTPUTS
        # =============================================================================================
        core.CfnOutput(self, 'STACK_REGION', value = self.region )
        core.CfnOutput(self, 'API_URL', value = api.graphql_url )
        core.CfnOutput(self, 'API_KEY', value = api.api_key )
        core.CfnOutput(self, 'API_ID', value= api.api_id )
