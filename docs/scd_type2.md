# Slowly Changing Dimension Type 2

An SCD Type 2 table keeps history by adding a new row each time a dimension attribute changes, with start date, end date and a current flag. Example: a customer moves city, so the old row is closed and a new row is opened. It lets reports show the attribute as it was at the time of each transaction. Type 1 overwrites the old value and keeps no history.
