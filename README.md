## AWS AppSync Multi Region Deployment

This repository contains code written in the [AWS Cloud Development Kit (CDK)](https://aws.amazon.com/cdk/) which launches infrastructure across two different regions to demonstrate using AWS AppSync in a multi-region setup.

By default, AWS AppSync endpoints only trigger GraphQL subscriptions in response to data mutations received on that same endpoint. This means that if data is changed by any other source or endpoint, as it is the case of multi-region deployment, then AppSync is not aware of this change and the subscription will not be triggered. To address this, you can use [AWS Lambda](https://aws.amazon.com/lambda/) functions and [Amazon DynamoDB Streams](http://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Streams.html) to enable subscriptions to work globally across Regions.

This pre-built AWS CDK solution extends AWS AppSync, enabling global applications with GraphQL subscriptions, and can be deployed to your AWS environment for testing purposes.

![Global Serverless Infrastructure](infrastructure.png?raw=true "Global Serverless Infrastructure")


## Pre-Requisites
### AWS Cloud9 Environment

[AWS Cloud9](<https://aws.amazon.com/cloud9/>) is a cloud-based integrated development environment (IDE) that lets you write, run, and debug your code with just a browser.

AWS Cloud9 contains a collection of tools that let you code, build, run, test, debug, and release software in the cloud using your internet browser. The IDE offers support for python, pip, AWS CLI, and provides easy access to AWS resources through Identity and Access Management (IAM) user credentials. The IDE includes a terminal with sudo privileges to the managed instance that is hosting your development environment. This makes it easy for you to quickly run commands and directly access AWS services.

#### Create an AWS Cloud9 environment:

1. Open the [AWS Cloud9 console](<https://eu-west-1.console.aws.amazon.com/cloud9/home?region=eu-west-1>) in the Ireland region (eu-west-1).
1. Choose **[Create Environment](<https://eu-west-1.console.aws.amazon.com/cloud9/home/create>)** or open the [link](<https://eu-west-1.console.aws.amazon.com/cloud9/home/create>).
1. For **Name**, enter **myDevEnv**.
1. Choose **Next step**
1. For **Cost-saving setting**, choose **After four hours**.
1. Select **Create a new no-ingress EC2 instance for environment (access via Systems Manager)**.
1. Leave the remaining parameters to the default.
1. Choose **Next Step**.
1. Choose **Create Environment**.
1. It will start the creation of the Cloud9 environment.

This Cloud 9 environment will come pre installed with the following tools, which are required to launch the infrastructure:
- AWS CLI
- Node JS
- Python v3
- Pip

### AWS CDK Toolkit
The toolkit is a command-line utility which allows you to work with CDK apps.
To install the toolkit, run the following command:
```bash
npm install -g aws-cdk
```

## Launch the Infrastructure
To launch the infrastructure that is detailed in the CDK stacks, first clone this repository onto the cloud9 machine:
```bash
git clone git@github.com:aws-samples/aws-appsync-multi-region-deployment.git
```

Then we can run the `setup.sh` script, which will launch the two CDK stacks.
```bash
cd aws-appsync-multi-region-deployment
bash setup.sh
```

This script will perform the following tasks automatically:
1. Setup the Lambda functions by installing the required Node modules and compressing into a .zip package.
2. Install the required CDK packages and modules
3. Boostrap the CDK
4. Launch the CDK stacks in the primary and secondary regions

Whilst this script is running, it will require your confirmation before infrastructure is launched in your account. On two occasions you will be prompted to type `y` and press the return key.

## Test the Solution
To test the solution, we will open a subscription to AWS AppSync in the Ireland region, and insert some data via a mutation to AWS AppSync in the Sydney region.

1. Open the [AWS AppSync Console in Ireland](https://eu-west-1.console.aws.amazon.com/appsync/home?region=eu-west-1) in one browser window.
2. In a separate browser window, open the [AWS AppSync Console in Sydney](https://ap-southeast-2.console.aws.amazon.com/appsync/home)
3. In the Ireland region, open the GraphQL API titled "IrelandGQLSchema" by clicking on its title. Then click on the 'Queries' tab on the menu on the left.
4. In the Sydney region, open the GraphQL API titled "SydneyGQLSchema" by clicking on its title. Then click on the 'Queries' tab on the menu on the left.
5. In the Ireland region, enter the following query into the query window and click the play button to open a subscription to the Ireland AppSync endpoint:
```
subscription MySubscription {
  onCreateItemsModel {
    id
    item
  }
}
```
6. In the Sydney region, enter the following mutation into the Query window and click the play button to send the data to the Sydney AppSync endpoint:
```
mutation MyMutation {
  createItemsModel(input: {id: "Item001", item: "MyItem"}) {
    id
    item
  }
}
```
7. In the Ireland region, where you have a subscription open, observe the new data being received by the client. This data has traveled from your client, to the AWS AppSync endpoint in Sydney, into the backend DynamoDB Global Table, replicated to Sydney, triggered the Lambda function in Sydney which notified the AWS AppSync endpoint in Sydney to the new data, which in turn delivered it to the client subscribed to it.

## Clean up
To clean up the infrastructure launched, execute the following commands from your cloud9 environment:
```bash
cd globalserverless
cdk destroy
cd ../globalserverlesssecondregion
cdk destroy
```

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.