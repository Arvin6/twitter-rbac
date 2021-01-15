## How to run
- Install [docker](https://docs.docker.com/engine/install/), [docker-compose](https://docs.docker.com/compose/install/) (Preferably on a linux machine).

- Run `docker-compose up --build` in the same folder as the docker-compose.yaml file is located

- Open your browser and navigate to http://localhost:8000/

## How to login
- This is a headless backend app, so we will use Swagger UI to interact with it. This will display the API documentation in a convenient, usable form.
- Scroll down to the `token` section of the UI and you will be able to login with the credentials. 
- If the login is successful, you will be see a  `jwt token` in the response.
- Copy this `token` and navigate to the top right of the UI. Now click on the Authorize button, paste the token in the format specified below and then click on the login button.

    ``` Bearer <jwt-token>```
- Now you have successfully logged in to the app.

## User stories
- User can login, view, update, delete only their own tweets.
- Admin can view everyone's tweets.
- Admin can modify, delete, create tweets on user's behalf. This action has to be approved by the superadmin to take effect.
- Admin can delete their own request and not of other admin's requests.
- A request once approved by the superadmin cannot be modified.
- Superadmin has ultimate power and can view, edit, delete tweets.
- Superadmin can approve the requests from admin.
- Logs pertaining to Access, Audit and Actions performed by each user including the superadmin is captured.
- Superadmin can query/filter requests/actions and logs and generate insights (for the current scope insights are limited to count of any query).

## Demo credentials
#### format: ({username}:{password}) 
- User
  - user1:user1
  - user2:user2
- Admin
  - admin1:admin1
  - admin2:admin2
- Superadmin
  - superadmin:superadmin

## How to use the APIs
### User:
    - Login as User A
    - Post a tweet X
    - Edit the tweet X with a new text content
    - Delete the tweet X (finally)

### Admin
    - Login as Admin M.
    - View tweets from all users.
    - Create an action (RequestAction) to create a tweet Y on behalf of User A called as Action C.
    - You will now be able to list actions including Q.
    - Create an action (RequestAction) to edit the content of tweet X called as Action U.
    - Attempting to do anything other than GET request from `/tweets/*` endpoints will result in Permission error.
    - Admins can create and edit user details as well.

### Superadmin
    - Login as superadmin S.
    - View all actions and be able to filter all actions based on set parameters. Eg: View all actions that are requested by Admin M.
    - Approve Action C using the `PATCH` request method of actions api. (PUT will not work since the requests cannot be updated once created, admins have to delete existing Action and raise a new request if they need changes). Once approved, you will notice a couple of logs in the terminal saying there were signals received.
    - Now if you GET the `/logs` api and you will see two logs pertaining to the approval that was done. 
      - 1. UPDATE action on the RequestAction entity that was created.
      - 2. CREATE action on the Tweet that was requested to be created on behalf of user.
    - If you list the tweets now, you can see the new tweet posted on behalf of a user.
    - Now you can do the same process to approve an UPDATE action on tweet X as raised by Admin M.
    - You can now find two logs pertaining to the latest approval which is, 
      - 1. UPDATE action on the RequestAction entity that was created.
      - 2. UPDATE action on tweet X that was requested to be updated.
    - If you check logs, you can also find Access logs pertaining to the login events you made.

## Database
- Sqlite3 (for simplicity sake, will prefer postgress for a production grade application)

## Attachments
- [DB design](models.pdf)
