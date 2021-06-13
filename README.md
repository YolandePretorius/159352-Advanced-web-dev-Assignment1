> README
>
> The app is used to retrieve data from IEX server and place it in a
> user portfolio. The user can also generate a graph Daily closing price
> of a certain stock for one year by choosing the stock symbol.
>
> Included in the file is a user guide with screen grabs indicating how
> the app works as well as bugs got from heroku
>
> CONTACT
>
> Student name: Yolande Pretorius
>
> Student nr: 18068659
>
> d
>
> WEBSITE
>
> https://serverwevdev.herokuapp.com :Portfolio login
>
> username: 18038659 password: 18038659
>
> <https://serverwevdev.herokuapp.com/stock> :stock chart website
>
> NEWS
>
> **Section 1: login and portfolio**

1.  Type in https://serverwevdev.herokuapp.com a login box will pop up.

2.  Type username : 18038659

3.  Type password: 18038659

4.  If username and password is correct your profile html page
    will open. To view stock chart use
    <https://serverwevdev.herokuapp.com/stock> if user is not logged in
    a login window will pop up again otherwise the user will go to the
    **welcome to your stock page** (see section2).

5.  You can also access your portfolio page through:
    https://serverwevdev.herokuapp.com

6.  Click on View stock to view current stock

7.  **To view updated list after changing quantities, prices and stock
    symbol click on view stock again. **

    Symbol:

8.  To select stock symbol start typing in Stock symbol text box, while
    typing the box will automatically show symbols available

9.  If user types in a value that is not a string, an alert appears
    prompting user to type n correct symbol

    Quantity:

10. Update quantity by + value and – value. If more quantity is sold
    than the user has available on the profile, a alert pop up “some
    data provided is invalid”.

11. .

> Price:

1.  If user tries to sell stock that he doesn’t have, an alert pops up
    “some data provided is invalid”.

2.  Reset button resets text in text boxes

3.  If user adds correct data, the stock data will be adjusted
    as needed.

Section 2: stock chart page

1.  If user is not logged in, a log in window will pop in.

2.  Once logged in user can start typing and find the stock symbol.

3.  To view the stock chart press view chart button (this part is not
    working on Heroku as a time out occurs)

4.  Reset button will reset text in text box.

BUGS:

1.  Portfolio HTML:

    1.  When user send update, the values doesn’t automatically appears
        or change in the table, the **user has to click on the view
        stock data again to see updated table.**

    2.  Better user friendly messages if the values added is invalid

    3.  Add a method where user can remove certain stock from the list

2.  Stock graph HTML (Heroku issues):

    2.1 if user type in a symbol that is not in the list, user should be
    notified that the symbol is invalid.

    2.2 If there is no symbol or used types in a number for a stock
    symbol and the user click on view graph button, an empty graph
    appears

> 3\. Heroku is not retrieving data form the server even though the app are
> running. A H12 time out error occurs since the request took longer than
> 30 seconds.
