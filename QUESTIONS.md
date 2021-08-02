# Questions and Contexts for Questions

USER STORY IN QUESTION:

As a community resident, I want to see which foods are offered `THIS WEEK` so that I can have them delivered and cook for the week.

- instead of having `harvest_date` and `expiration_date` attrs in the `farmer_contribution` model, should i do: `offering_post_date = db.Column(db.DateTime, default=datetime.now())` and then have in-app logic that auto-removes contents from db after 7 days have passed?

- if so, should this attr be in `farmer_contr` or `offering` model?
- how to make it so that user can assume that nothing they're looking at is more than 7 days old?

USER STORY IN QUESTION:
As a comm rep, I want to be able to select the count of each food that I want and add it to my weekly box.

- what's the best way to create an order? should i just rely on the way order is currently built and have some logic that queries all the offering ids that end up tied to the order id? 