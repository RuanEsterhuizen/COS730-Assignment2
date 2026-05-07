# Notes for while I'm building

## Assumptions
- From the seq diagram, we assume that objects are instantiated when the first method is called
- A research output is a JSON document with the following contents (see example)
- To simulate a bunch of reviewers scoring papers, random numbers are used 
- time.sleep(0.01) is used to mock calling some notification service, such as sendgrid
- All titles and authors are unique, but cannot be checked beforehand, due to the design

## Validation Rules
1. JSON must be valid format
2. All fields must be present
think of more

## Problems with current design
