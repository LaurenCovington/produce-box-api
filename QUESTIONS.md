# Questions and Contexts for Questions

USER STORY IN QUESTION:

As a community resident, I want to see which foods are offered `THIS WEEK` so that I can have them delivered and cook for the week.

- instead of having `harvest_date` and `expiration_date` attrs in the `farmer_contribution` model, should i do: `offering_post_date = db.Column(db.DateTime, default=datetime.now())` and then have in-app logic that auto-removes contents from db after 7 days have passed?

- if so, should this attr be in `farmer_contr` or `offering` model?
- in general, how to make it so that user can assume that nothing they're looking at is more than 7 days old?



USER STORY IN QUESTION:
As a comm_res, I want to be able to select the count of each food I want in my box

- need if statement in `"/<offering_id>/choose_count"` route: 
  - if 'up' button hit, decrease avail_inv x1/click; elif 'down' button hit, increase, else pass
- does avail_inv need to be the only attr that changes? should desired_count be added to one of the tables (offering? order_box?)
  
USER STORY IN QUESTION:
As a comm res, I want to be able to delete foods from my cart so that I'm free to change my mind and make sure my order matches that

- How to delete something from a specific order but not from the whole database?
  - Vishaal and Bri: toggle related ID to null to break the association without deleting from database