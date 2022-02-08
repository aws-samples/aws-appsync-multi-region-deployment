/*
 * Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 * SPDX-License-Identifier: MIT-0
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this
 * software and associated documentation files (the "Software"), to deal in the Software
 * without restriction, including without limitation the rights to use, copy, modify,
 * merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
 * permit persons to whom the Software is furnished to do so.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
 * INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
 * PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 * HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
 * OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
 * SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

const axios = require('axios');
const gql = require('graphql-tag');
const graphql = require('graphql');
const { print } = graphql;
const util = require('util');

const publishItem = gql`
  mutation PublishMutation($name: String!, $id: ID!) {
    publishItemsModel(input: {id: $id, item: $name}) {
      id
      item
    }
  }
`

const executeMutation = async(id, name) => {
  console.info("Executing Mutation")
  console.info("DEBUG1901: EXPORTS.JS executeMutation")
  const mutation = {
    query: print(publishItem),
    variables: {
      name: name,
      id: id,
    },
  };
  console.info("Mutation generated. Mutation: "+util.inspect(mutation))
  console.info("Mutation json stringify: "+JSON.stringify(mutation))
  try {
    console.info("Attempting Axios")
    let response = await axios({
      url: process.env.AppSyncAPIEndpoint,
      method: 'post',
      headers: {
        'x-api-key': process.env.AppSyncAPIKey
      },
      data: JSON.stringify(mutation)
    });
    console.info("Axios Completed. Data: "+util.inspect(response.data))
    console.log("Response: " + response.data);
  } catch (error) {
    console.info("Error caught")
    console.error(`[ERROR] ${error.response.status} - ${JSON.stringify(error.response.data)}`);
    throw error;
  }
};

exports.handler = async(event) => {
  console.info("DEBUG1901: EXPORTS.JS exports.handler")
  console.log("API Key: "+process.env.AppSyncAPIKey)
  for (let record of event.Records) {
    switch (record.eventName) {
      case 'INSERT':
        console.info("Item Inserted");
        // Grab the data we need from stream...
        let id = record.dynamodb.Keys.id.S;
        let name = record.dynamodb.NewImage.item.S;
        console.info("id: "+id)
        console.info("name: "+name)
        // ... and then execute the publish mutation
        await executeMutation(id, name);
        break;
      case 'UPDATE':
        /* To keep this example simple, we do not notify about UPDATES made to the data,
         * we only notify about new data being inserted.
         * However we have left the case here as a placeholder.
        */
        console.info("Item Updated");
        break;
      case 'DELETE':
        /* To keep this example simple, we do not notify about DELETES made to the data,
         * we only notify about new data being inserted.
         * however we have left the case here as a placeholder.
        */
        console.info("Item Deleted");
        break;
      default:
        break;
    }
  }
  return { message: `Finished processing ${event.Records.length} records` }
}
