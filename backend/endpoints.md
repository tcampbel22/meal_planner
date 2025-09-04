# Endpoints to create

## Auth
|        Route        |  Method | Test  |     Notes           |
| ------------------- | ------- | ----- | ------------------- |
| "/auth/login"       |   POST  | - []  | Login user          |
| "/auth/logout"      |   POST  | - []  | Logout user         |
| "/auth/register"    |   POST  | - []  | Register user       |


## User
|        Route           |  Method | Test  |     Notes           |
| ---------------------- | ------- | ----- | ------------------- |
| "/user/id"             |  GET    | - []  | Users profile page  |
| "/user/id"             |  DELETE | - []  | Delete user         |
| "/user/settings/id"    |  GET    | - []  | User settings page  |
| "/user/pw/id"          |  POST   | - []  | Reset password      |
| "/user/uname/id"       |  POST   | - []  | Reset username      |


## Recipe
|        Route        |  Method  | Test  |     Notes                  |
| ------------------- | -------- | ----- | -------------------------- |
| "/recipe"           |   GET    | - []  | Fetch all recipes          |
| "/recipe/id"        |   GET    | - []  | Fetch specific recipe      |
| "/recipe/id"        |   POST   | - []  | Add recipe                 |
| "/recipe/id"        |   PUT    | - []  | Update recipe              |
| "/recipe/id"        |   DELETE | - []  | Delete recipe              |

## Meal Plans
|        Route        |  Method  | Test  |     Notes                  |
| ------------------- | -------- | ----- | -------------------------- |
| "/plan"             |   GET    | - []  | Fetch all mealplans        |
| "/plan"             |   POST   | - []  | Generate meal plan         |
| "/plan/id"          |   PUT    | - []  | Regenerate meal plan       |
| "/plan/id"          |   GET    | - []  | Fetch specific mealplan    |
| "/plan/id"          |   DELETE | - []  | Delete specific mealplan   |
