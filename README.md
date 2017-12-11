# jubilant-octo-garbanzo

## Name

TBD

## Project Overview

This project will be a prototype for new user-generated content applications to be potentially implemented on source.training, an electric-utility industry eTraining platform:
* Q&A application, similar to Stack Overflow, in which questions can be asked, and answer responses can be up or down voted by other users. Answers can be marked as the solution by the original question poster. Questions are separated into answered and unanswered lists, and everything is searchable.
* There should be some sort of topic tagging and filtering option
* There should also be a notification system that lets you know when answers have been posted to your questions
* Time permitting, users should be able to archive/delete/or otherwise moderate questions or answers by some sort of arbitrary consensus if content is offensive, irrelevant, etc.
* Time permitting, gamification will be added for points, badges, and ranks based on participation. Number of questions asked or answered, number of solutions provided, etc. Will include some sort of trophy case profile page.

## Functionality

Questions and answers are viewable by unauthenticated users. But posting either requires authentication, as does up or down voting an answer.
Main page consists of a list of answered and unanswered questions, as well as search and filter options.
A field or button that prompts the user to ask a question is prominently featured on the page. Posting a question instantiates a Question model. Answers work the same way.
Time-permitting w/the gamification features, there will need to be a function that is run whenever activity is saved to the platform that compares the user’s stats (# of questions asked/answered, etc.) with success conditions for each type of badge.

## Data Model
User (custom implementation):
* First/Last Names
* Email address
* Avatar
* Question count (Integer Field)
* Answer count
* Solution count
* Points
* Rank (Many to Many)
* Badges

Question:
* User
* Text Field
* Image Field (for screenshots)
* Date/Timestamp
* Tag(s)

Answers:
* User
* Text Field
* Image Field (for screenshots)
* Date/Timestamp
* Solution Boolean Field
* Votes

Badges:
* Name
* Image
* Date/time earned
* Conditions (Questions, Answers, Solutions)

## Schedule

December 11-15
Authentication system, and working prototype of basic Q&A functionality with up and down votes.

December 18-22
Search and tag functionality implemented; notifications time-permitting

December 25-29
If on schedule, basic gamification and notification elements should be implemented this week

January 1-5
Front end polish, particularly for mobile optimization via bootstrap

BEYOND!
Additional apps:
* Micro-blogging akin to Twitter
* Crowd-edited articles akin to Wikipedia
