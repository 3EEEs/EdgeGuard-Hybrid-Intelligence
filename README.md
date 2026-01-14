# Project Proposal: EdgeGuard Hybrid Intelligence
## Date: January 13, 2026 Course: CS 362

1. Team Info

Team Members & Roles
* Member 1 - Ethan Short: Role
* Member 2 - Calvin Grabowski: Role
* Member 3 - Michael Wilde: Role
* Member 4 - Samuel Dressel: Role

## Project Artifacts

Code Repository: [Link](https://github.com/3EEEs/EdgeGuard-Hybrid-Intelligence)

Project Board: [Github Project](https://github.com/users/3EEEs/projects/2/views/1)

## Communication Plan

Channels: Discord and text groupchat for daily synchronous chat; GitHub Issues for task tracking; Weekly meeting after class and as needed.

## Rules:
* All code changes must go through a Pull Request with at least one review.
* "Blockers" must be communicated in Discord immediately.
* Response time expectation: Within 24 hours on weekdays.

2. Product Description

* Goal: Takes snippets of movement from a video and saves those snippets. This saves total storage, saves money by making our customers not having to submit as much to amazon rekognition, and it makes it easier for humans to go through the snippets. Our product would send only exact frames or small clips to amazon rekognition to save money, by sending less frames than other services and less expensive than other options.

3. Project Scope
## Major Features
* Local Motion "Gatekeeper": A Python application that reads a webcam feed and successfully filters out static backgrounds, triggering only on significant movement.
* Cloud Integration Pipeline: Automatic secure upload of captured frames to an AWS S3 bucket using the Boto3 SDK.
* AI Analysis Service: A backend Lambda function that processes uploaded images via Amazon Rekognition and returns a list of detected labels (e.g., Person, Car, Pet).
* Event Dashboard: A web-based user interface that displays a list of recent detections, showing the timestamp, the image, and the tags returned by the AI.

## Stretch Goals
* Cost-Savings Calculator: A visualization on the dashboard comparing "Estimated Cost if Full Streaming" vs. "Actual Cost with EdgeGuard," using live AWS pricing data.
* SMS/Email Alerts: Integration with AWS SNS (Simple Notification Service) to text the user immediately when a specific "High Threat" object (e.g., a person at night) is confirmed by the cloud.

## Other Ideas
* Running app: Make a running app that allows the user to help make workout paces for the user based on what they want to do. This would be useful with all runners by making it easier for people with different paces to get the exact pace that they should be running
* Guitar Idea: Make an ai that reads music and writes it into the app. Then the app would have recorded videos of each note on a guitar to help with fingering. It would play a clip of ethan playing the guitar at each note when the note hits. You can change tempo, and it would play the song with clips of Ethan playing combined
* Motion Detection: check to see movement in frames, and then send it to amazon to figure out what moved, and provide a cheaper process than others availiable
* Worship night: have an app to help work with schedules and visualize who is playing what on what day
* Losing Tickets: make a system that fixes that by making a better ticketing system with an interface that connects to a new ticket system that makes it easier to track status on a ticket, and what computers are linked to the ticket, and who is working on the ticket.
