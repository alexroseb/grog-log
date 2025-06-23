# Overview
This site will allow users to track their progress through the Grog Log at Tonga Hut.
# Database Setup
- Grog Log Drinks (drinks)
  - id - integer, unique
  - name - String
  - ingredients - String (note: maybe individual columns for each ingredient? Will see what format the data is in)
- Users (users)
  - username - String, unique
  - password - encrypted (how?)
  - drink_log - list of JSON entries
    - id - integer
    - date - datetime
    - comment - String
# Pages Needed
- index
  - login form
- view entries
- add entry
# References
- [Grog Log Data](https://itsdatadana.com/2017/07/27/the-grog-log-blog/)