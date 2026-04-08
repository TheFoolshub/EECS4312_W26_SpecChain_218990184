# Requirement ID: FR1 -- This is an example

- Description: [The system shall allow users to log workouts without the application crashing.]
- Source Persona: [Frequent Activity Tracker]
- Traceability: [Derived from review group G1]
- Acceptance Criteria: [Given the user is logging a workout When the logging process completes Then the application must not crash and the workout must be saved.]


Requirement ID: FR1

Description: The system shall clearly display subscription pricing, renewal dates, and billing terms before any charge is made.
Source Persona: P1 – Alex the Overcharged Subscriber
Traceability: Derived from review group G1
Acceptance Criteria:
Given the user is viewing the subscription page
When the page loads
Then the full price, billing cycle, renewal date, and cancellation instructions are visible without requiring additional navigation

Requirement ID: FR2

Description: The system shall allow users to cancel a free trial or subscription through a clearly labeled in-app option.
Source Persona: P1 – Alex the Overcharged Subscriber
Traceability: Derived from review group G1
Acceptance Criteria:
Given the user wants to cancel their subscription
When they navigate to Settings > Subscription
Then a clearly labeled “Cancel Subscription” option is available and completes within the app

Requirement ID: FR3

Description: The system shall not charge users after a free trial has been cancelled before its expiration date.
Source Persona: P1 – Alex the Overcharged Subscriber
Traceability: Derived from review group G1
Acceptance Criteria:
Given the user cancels a free trial before the trial end date
When the trial period expires
Then no charge is applied and access reverts to the free tier

Requirement ID: FR4

Description: The system shall not crash or freeze during an active meditation, sleepcast, or focus session.
Source Persona: P2 – Jordan the Interrupted Meditator
Traceability: Derived from review group G2
Acceptance Criteria:
Given the user is playing an audio session
When the session is in progress
Then the app remains stable and responsive until completion or manual stop

Requirement ID: FR5

Description: The system shall load and begin playback of selected content within an acceptable response time.
Source Persona: P2 – Jordan the Interrupted Meditator
Traceability: Derived from review group G2
Acceptance Criteria:
Given the user selects a session on a stable internet connection
When playback is initiated
Then audio begins within 5 seconds

Requirement ID: FR6

Description: The system shall maintain stability and performance after software updates.
Source Persona: P2 – Jordan the Interrupted Meditator
Traceability: Derived from review group G2
Acceptance Criteria:
Given a new app update is installed
When the user uses core features
Then no new crashes occur and average load time remains within ±10% of the previous version

Requirement ID: FR7

Description: The system shall allow users to play downloaded content without requiring an internet connection.
Source Persona: P3 – Sam the Offline Sleeper
Traceability: Derived from review group G3
Acceptance Criteria:
Given the user has downloaded a session
When the device is offline
Then the session plays fully without buffering or connectivity errors

Requirement ID: FR8

Description: The system shall retain downloaded content across app updates.
Source Persona: P3 – Sam the Offline Sleeper
Traceability: Derived from review group G3
Acceptance Criteria:
Given the user has downloaded sessions before an update
When the app updates
Then all downloaded sessions remain accessible and playable offline

Requirement ID: FR9

Description: The system shall provide a simple and intuitive navigation structure.
Source Persona: P4 – Taylor the Overwhelmed Navigator
Traceability: Derived from review group G4
Acceptance Criteria:
Given the user is on the home screen
When they navigate to a content category
Then the desired content is reachable within 3 taps or fewer

Requirement ID: FR10

Description: The system shall provide a search function that returns relevant results based on user input.
Source Persona: P4 – Taylor the Overwhelmed Navigator
Traceability: Derived from review group G4
Acceptance Criteria:
Given the user enters a keyword in the search bar
When the search is executed
Then relevant results are displayed within the top results

Requirement ID: FR11

Description: The system shall provide diverse meditation and sleep content supporting stress reduction and daily use.
Source Persona: P5 – Emma the Consistent Relaxation Seeker
Traceability: Derived from review group G5
Acceptance Criteria:
Given the user browses the content library
When selecting categories such as stress, sleep, focus, or mindfulness
Then at least 10 sessions are available per category

Requirement ID: FR12

Description: The system shall allow users to track their meditation activity and progress.
Source Persona: P5 – Emma the Consistent Relaxation Seeker
Traceability: Derived from review group G5
Acceptance Criteria:
Given the user has completed sessions
When they access their profile or progress section
Then at least 30 days of activity, session history, and streak data are displayed
