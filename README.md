# ESEP Assignment 8 · Event-Driven Architecture

Opening an issue in `lazysince87/esep-webhooks` sends a GitHub webhook to API Gateway. The REST API passes the JSON body to a Python Lambda, which reads `issue.html_url` and sends `Issue Created: <link>` to Slack. The handler ignores GitHub's ping and accepts issue updates as well as new issues.

## Deploy to AWS

1. Open **CloudFormation** in **US East (Ohio)** (`us-east-2`). Choose **Create stack → With new resources (standard)**. Choose an existing template, select **Upload a template file**, and upload `a8-aws-stack.yaml`.
2. Name the stack `esep-webhooks`. Accept the defaults and acknowledge the IAM resource on the stack configuration page. The template creates a Lambda execution role for writing CloudWatch logs. Submit the stack and wait for `CREATE_COMPLETE`.
3. In **Lambda → EsepWebhook → Configuration → Environment variables**, add `SLACK_URL` with your section's Canvas webhook URL. Store the value only in Lambda's environment variables.
4. In the CloudFormation stack's **Outputs**, copy `InvokeUrl`. It ends in `/default` and accepts `POST` at the root of the stage.

## Connect GitHub

1. Create a **public** GitHub repository called `esep-webhooks` under `lazysince87`. Upload `lambda_function.py`, `a8-aws-stack.yaml`, and this README. These files are ready to commit as provided.
2. Go to **Settings → Webhooks → Add webhook**. Paste `InvokeUrl` into **Payload URL**, set **Content type** to `application/json`, leave **Secret** empty for the assignment, and keep SSL verification and **Active** enabled.
3. Choose **Let me select individual events** and select **Issues** only. Save the webhook.

## Verify and submit

1. Check **Recent Deliveries** for a successful ping. An `"ignored"` response is expected for a ping.
2. Open an issue titled `A8 webhook test`. The new delivery should have HTTP 200 with body `"ok"`, and Slack's **#eventing-webhook** should show `Issue Created:` followed by the issue URL.
3. Enter `https://github.com/lazysince87/esep-webhooks` in the Canvas **Web URL** field.

If the issue delivery fails, inspect its response in **Recent Deliveries** and check **Lambda → EsepWebhook → Monitor → View CloudWatch logs**. A 403 from API Gateway can indicate a wrong stage URL. A 502 points to a Lambda or Slack failure.
