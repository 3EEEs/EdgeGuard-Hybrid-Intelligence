# Project Proposal: EdgeGuard Hybrid Intelligence
## Date: January 13, 2026 Course: CS 362

1. Team Info

Team Members & Roles
* Member 1 - Ethan Short: Role
* Member 2 - Name: Role
* Member 3 - Name: Role
* Member 4 - Name: Role

## Project Artifacts

Code Repository: [Link](https://github.com/3EEEs/EdgeGuard-Hybrid-Intelligence)

Project Board: [Github Project](https://github.com/users/3EEEs/projects/2/views/1)

## Communication Plan

Channels: Discord for daily synchronous chat; GitHub Issues for task tracking; Weekly meeting after class and as needed.

## Rules:
* All code changes must go through a Pull Request with at least one review.
* "Blockers" must be communicated in Discord immediately.
* Response time expectation: Within 24 hours on weekdays.

2. Product Description

3. Project Scope
## Major Features
* Local Motion "Gatekeeper": A Python application that reads a webcam feed and successfully filters out static backgrounds, triggering only on significant movement.
* Cloud Integration Pipeline: Automatic secure upload of captured frames to an AWS S3 bucket using the Boto3 SDK.
* AI Analysis Service: A backend Lambda function that processes uploaded images via Amazon Rekognition and returns a list of detected labels (e.g., Person, Car, Pet).
* Event Dashboard: A web-based user interface that displays a list of recent detections, showing the timestamp, the image, and the tags returned by the AI.

## Stretch Goals
* Cost-Savings Calculator: A visualization on the dashboard comparing "Estimated Cost if Full Streaming" vs. "Actual Cost with EdgeGuard," using live AWS pricing data.
* SMS/Email Alerts: Integration with AWS SNS (Simple Notification Service) to text the user immediately when a specific "High Threat" object (e.g., a person at night) is confirmed by the cloud.
