# openx_intership_tasks
Task for internship

# longest_substring.xlsx
First task. File with table of input/output data sets with description.

# test_sample.py
Second task. File with functions and test-cases for restful-booker API

# Observations:
- PartialUpdateBooking can take inncorrect values types in place of strings. No matter value tape it allways returns hhtps code 200
- CreateToken return code 200 with incorrect creditential given, but JSON obcjet is {'reason': 'Bad credentials'}
- GetBookingIds with checkin parameter, return only dates greater that given. Documentation says it should also return equal dates, so test fails 
