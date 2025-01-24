---
name: Bug report
about: Create a report to help us improve
title: "[BUG]"
labels: ""
assignees: ""
---

## 🚨 **Please Note** 🚨

To ensure efficient investigation of the issue, please fill out the fields below with as much detail as possible. **Reports that do not follow this template may be closed without notification.** We appreciate your cooperation.

## 🐞Describe the bug

A clear and concise description of what the bug is.

## 🔄 To Reproduce

Steps to reproduce the behavior:

1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

## 📷 Screenshots

If applicable, add screenshots to help explain your problem.

## 🔎 Logs for Chat Issues

If the issue occurs during a chat interaction, please check the following logs on Amazon Cloudwatch Logs and include the relevant entries in your issue:

- `/aws/lambda/BedrockChatStack-BackendApiHandlerXXXX`
- `/aws/lambda/BedrockChatStack-WebSocketHandlerXXXX`

## 🔎 Logs for Bot Creation/Update Issues

If the issue occurs during bot creation or updating, please check the execution records of the AWS Step Functions state machine named `EmbeddingStateMachineXXX` and include the details in your issue.

## 📝 Additional context

Add any other context about the problem here.
