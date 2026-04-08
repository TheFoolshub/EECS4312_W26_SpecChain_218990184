Requirement ID: FR_1

Description: The system shall not crash or freeze when users are meditating, sleeping, or interacting with the screens of the application. Source Persona: Jordan Martinez (P_1) Traceability: Derived from review group H1 (App Performance and Stability Issues) Acceptance Criteria: Given a user begins a meditation or sleep session, when the session is playing, the application shall not crash or freeze until the user ends the session. Notes: Rewrote according to review group H1. Removed stable internet connection requirement since that was not mentioned in the review group. Testable via observing if the sessions play without any crashes.

Requirement ID: FR_2

Description: The system shall load the meditation or sleep content within 10 seconds of tapping play on a working internet connection. Source Persona: Jordan Martinez (P_1) Traceability: Derived from review group H1 (App Performance and Stability Issues) Acceptance Criteria: Given a user selects a meditation or sleep content session and taps play, the content will begin playing within 10 seconds of tapping play on a wifi or mobile data connection. Notes: New requirement from review group H1 regarding loading. Using 10 seconds as a time frame instead of “takes forever” as mentioned by the users in the survey. Can be tested by measuring the amount of time it takes for the content to begin playing after the user taps play.

Requirement ID: FR_3

Description: The system shall not experience any performance issues or crashes after being updated to a new version of the application. Source Persona: Jordan Martinez (P_1) Traceability: Derived from review group H1 (App Performance and Stability Issues) Acceptance Criteria: Given a user updates the application to a new version, when they perform the same actions as before the update, the application should perform at least as well as it did in the previous version of the application. Notes: New requirement as many reviews from H1 stated that the updates to the application resulted in worse performance. This was not mentioned in the Auto spec document.

Requirement ID: FR_4

Description: The system shall display the price of the subscription, the billing cycle, and that the subscription will automatically renew before any payment is charged to the user. Source Persona: Taylor Kim (P_2) Traceability: Derived from review group H2 (Subscription, Billing, and Customer Service Issues) Acceptance Criteria: Given a user views the subscription options, when the subscription page is loaded, the price, billing cycle, and auto-renewal of the subscription will be visible without the user having to navigate to any other pages. Notes: Improved suggestion from R3. Based on the reviews in H2 the subscription should indicate the price, billing cycle, and auto-renewal status. Removed vague language as requested by the users.

Requirement ID: FR_5

Description: The system shall allow users to cancel their subscription to the meditation and sleep application through the settings within the application. Source Persona: Taylor Kim (P_2) Traceability: Derived from review group H2 (Subscription, Billing, and Customer Service Issues) Acceptance Criteria: Given a user navigates to the settings for the application, when they navigate to the subscription management settings, there should be an option for the user to click to cancel their subscription within the application. Notes: Rewrote R4 to specifically target the issue mentioned by the users in H2. Removed time frame of 2 minutes to cancel as it was not mentioned in the reviews.

Requirement ID: FR_6

Description: The system shall not begin to charge a user after they have cancelled their subscription to the application. Source Persona: Taylor Kim (P_2) Traceability: Derived from review group H2 (Subscription, Billing, and Customer Service Issues) Acceptance Criteria: Given a user cancels their subscription to the application, when the subscription is cancelled, no charges shall occur after the current subscription period. Notes: New requirement to address the main point of the H2 review groups. Users were concerned that they would be charged after cancelling their subscription. This point was not mentioned in the Auto specification.

Requirement ID: FR_7

Description: The system shall have a search function that returns relevant meditation or sleep content based upon the keywords that are entered by the user. Source Persona: Sam Patel (P_3) Traceability: Derived from review group H3 (Navigation, UI/UX, and Content Discovery Issues) Acceptance Criteria: Given a user types a specific keyword into the search bar, when they perform the search, the application shall return relevant meditation or sleep content to that search term. Notes: Simplified from R7. Removed references to navigating to the content in less than 2 clicks as this was not mentioned in the reviews. Focus on search function as this was the main issue mentioned by the users.

Requirement ID: FR_8

Description: The system shall organize the content in a way that is easy to read and that does not overwhelm the users with numerous sections on the home screen. Source Persona: Sam Patel (P_3) Traceability: Derived from review group H3 (Navigation, UI/UX, and Content Discovery Issues) Acceptance Criteria: Given a user opens the meditation and sleep application, when the home screen is loaded, the content should be organized into sections with visible labels that are no more than three sections that require the users to scroll horizontally to view the content. Notes: New requirement based upon the feedback from review group H3 regarding the organization of the content. Users commented that the current application is overwhelming with the number of sections. Specifically limiting the number of sections that must scroll horizontally to view the content is a new requirement. This is the main issue stated by the users.

Requirement ID: FR_9

Description: The system shall allow for user downloaded meditation and sleep content to be played without the need for an internet connection. Source Persona: Casey Rodriguez (P_4) Traceability: Derived from review group H4 (Offline Access and Download Problems) Acceptance Criteria: Given a user downloads content while connected to the internet, when the user turns off the wifi and mobile data, the downloaded content will play without any internet connection errors. Notes: Rewrote requirement R2 to include the perspective of user P_4. Downloads must be able to occur offline as stated by the users. Removed time frame of 30 days as this was not mentioned by the users in their reviews.

Requirement ID: FR_10

Description: The system shall retain any content that is downloaded by the user even after the application is updated. Source Persona: Casey Rodriguez (P_4) Traceability: Derived from review group H4 (Offline Access and Download Problems) Acceptance Criteria: Given a user has downloaded content before the application is updated, when the application is updated, the content that was downloaded prior to the update is still retained by the application and can be accessed by the user. Notes: New requirement as mentioned in H4. Users are concerned that when the application is updated, any content that was downloaded is deleted. This point was not mentioned in the Auto specification document.

Requirement ID: FR_11

Description: The system shall display information regarding the data that is collected from the users and allow the user to opt out of sharing their data with third parties for advertising purposes. Source Persona: Morgan Chen (P_5) Traceability: Derived from review group H5 (Privacy, Data Collection, and AI Integration Concerns) Acceptance Criteria: Given that a user navigates to the privacy settings of the application, when the privacy settings page is loaded, the application will display the types of data that is collected from the users and allow the user to opt out of sharing that data for advertising purposes. Notes: Combined requirement R8 and R9 into one requirement. Focus on displaying information on the privacy settings page as mentioned in H5. Removed vague language.

Requirement ID: FR_12

Description: The system shall not use any data from the users’ meditation or personal data to train artificial intelligence models without the consent of the users. Source Persona: Morgan Chen (P_5) Traceability: Derived from review group H5 (Privacy, Data Collection, and AI Integration Concerns) Acceptance Criteria: Given that a user is using the meditation and sleep application, when the developers are training artificial intelligence models for new features, the system shall not use the data from the users’ meditation or personal data without the user explicitly agreeing to that use of their data. Notes: New requirement based upon H5 review groups regarding artificial intelligence. While this is a growing issue in the meditation and sleep industry, it was not mentioned in the auto specification for the application.
