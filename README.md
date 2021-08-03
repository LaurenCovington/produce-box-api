# produce-box-api - BE repo

# General project idea
- Small, local community food movements often have trouble coordinating efforts when bringing community supported agriculture initiatives to life. 
- The problem the project hopes to solve is one of connecting all parties involved in creating a produce delivery system for a neighborhood. 
- The product will allow community residents to view and choose culturally-relevant foods they might like delivered, send that information to local growers who participate at farmer's markets (urban farmers as well as rural ones in a given state) so that they can bring what's requested to a city, and offer a 'connector' non-profit the final collection of info for each household: what and how much needs to be delivered and delivery address so that employees can deliver.

## MVP Feature Set

An App feature
    - Product will offer database whose data is viewable by consumers, farmers and nonprofit employees
    - Database can be populated with data from farmers (with info on produce grown, how much can be offered for a CSA)
    - Database can be populated with data from community residents (contact/delivery info and produce selections)
    - Database is viewable by nonprofit employees, who will orchestrate delivery (can view delivery addresses, any order discrepancies)

### Potential Additional Features
    - Ability to post milestones of produce box initiative success on social media
    - Push notification to NPO at time of supply-demand reconciliation where what was offered, what was ordered, and delivery location and date/time is displayed 

## Draft Technology Choices
    - React (web app for nonprofit use)
    - Progressive Web Apps (accessibility for food-insecure community residents)
    - O-Authorization
    - Flask
    - Python
    - PostgreSQL (data persistence)
