const AWS = require("aws-sdk");
const ddb = new AWS.DynamoDB.DocumentClient();

exports.handler = async (event) => {
  const email = event.requestContext.authorizer.claims.email;

  console.log("Email from token:", email);

  const params = {
    TableName: "users-table", // update to your actual table name
    Key: { email },
  };

  try {
    const result = await ddb.get(params).promise();

    if (!result.Item) {
      return {
        statusCode: 404,
        body: JSON.stringify({ message: "User not found" }),
      };
    }

    return {
      statusCode: 200,
      body: JSON.stringify(result.Item),
    };
  } catch (err) {
    console.error("Error fetching user:", err);
    return {
      statusCode: 500,
      body: JSON.stringify({ message: "Internal server error" }),
    };
  }
};
