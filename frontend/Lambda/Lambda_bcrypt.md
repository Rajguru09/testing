✅ Fix: Deploy Lambda with bcrypt using a ZIP package
🔧 Step-by-Step Guide:
✅ 1. Create a project directory on your local machine

mkdir lambda-login-function
cd lambda-login-function

✅ 2. Create your Lambda function file
Save your lambda_function.py in this directory.

✅ 3. Install bcrypt into a python directory
Use a Linux-compatible environment (such as WSL, Docker, or EC2), because Lambda uses Amazon Linux under the hood.

pip install bcrypt -t .
This installs bcrypt and its dependencies into the current directory.

❗ Don't use pip install bcrypt on Windows directly — it will cause binary incompatibility with Lambda.

✅ 4. Zip the contents
Make sure you zip all files, not the folder itself:

zip -r lambda_function.zip .
✅ 5. Upload the ZIP to AWS Lambda
Go to the AWS Lambda Console

Select your Lambda function

Choose Upload from → .zip file

Upload your lambda_function.zip

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<

**To send the lambda_function.zip file from your local WSL (Ubuntu/Linux) environment to your AWS Lambda function, you have two common options:**
✅ Option 1: Upload using AWS Management Console
Locate the ZIP in WSL
If you created the ZIP inside WSL (~/lambda-login-function/lambda_function.zip), you can copy it to your Windows filesystem like this:

cp lambda_function.zip /mnt/c/Users/<YourUsername>/Downloads/
Open AWS Console

Go to https://console.aws.amazon.com/lambda

Select your Lambda function

Click "Upload from" > ".zip file"

Upload the ZIP you copied to Downloads.

✅ Option 2: Upload using AWS CLI
Make sure AWS CLI is configured
In WSL:

aws configure
Update the Lambda function
Use this command (replace your-function-name with your actual Lambda function name):

aws lambda update-function-code \
  --function-name your-function-name \
  --zip-file fileb://lambda_function.zip

🔁 Quick Tip: Get function name from console
Go to AWS Lambda > Your function > Copy the name and use in the CLI.

