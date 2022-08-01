import requests

booking_data = {'firstname': 'Jan',
                'lastname': 'Kowalski',
                'totalprice': 212,
                'depositpaid': True,
                'bookingdates': {'checkin': '2022-01-01', 'checkout': '2022-01-02'},
                'additionalneeds': 'dinner'}  # global variable for tests


def ping():
    """A simple health check endpoint to confirm whether the API is up and running."""
    response = requests.get("https://restful-booker.herokuapp.com/ping")
    return response


def get_bookingids(firstname="", lastname="", checkin="", checkout=""):
    """Returns the ids of all the bookings.
    Can take optional query strings to search and return a subset of booking ids """
    varlist = [firstname, lastname, checkin, checkout]
    url = "https://restful-booker.herokuapp.com/booking?"
    for i in varlist:
        if i:
            if i == firstname:
                url = url + "firstname=" + i + "&"
            if i == lastname:
                url = url + "lastname=" + i + "&"
            if i == checkin:
                url = url + "checkin=" + i + "&"
            if i == checkout:
                url = url + "checkout=" + i + "&"
    response = requests.get(url=url)
    return response


def get_booking(booking_id):
    """Returns a specific booking based upon the booking id provided"""
    response = requests.get(url=f"https://restful-booker.herokuapp.com/booking/{booking_id}")
    return response


def create_booking(update):
    """Creates a new booking in the API"""
    response = requests.post(url="https://restful-booker.herokuapp.com/booking", json=update)
    return response


def create_token(uname, passw):
    """Creates a new auth token to use for access to the PUT and DELETE /booking"""
    response = requests.post(url="https://restful-booker.herokuapp.com/auth",
                             data={"username": uname, "password": passw})
    return response


def update_booking(booking_id, update):
    """Updates a current booking with a partial payload"""
    response = requests.put(
        url=f"https://restful-booker.herokuapp.com/booking/{booking_id}",
        json=update,
        cookies={"token": create_token("admin", "password123").json()["token"]})
    return response


def partial_update(booking_id, update):
    """Updates a current booking with a partial payload"""
    response = requests.patch(
        url=f"https://restful-booker.herokuapp.com/booking/{booking_id}",
        json=update,
        cookies={"token": create_token("admin", "password123").json()["token"]})
    return response


def delete_booking(booking_id):
    """Deletes booking with given id"""
    response = requests.delete(
        url=f"https://restful-booker.herokuapp.com/booking/{booking_id}",
        cookies={"token": create_token("admin", "password123").json()["token"]})
    return response


class Tests:
    def test_ping(self):
        """healthcheck test"""
        assert ping().status_code == 201

    def test_get_bookingids(self):
        """get_bookingids test without arguments"""
        assert get_bookingids().status_code == 200

    def test_get_bookingids_fname(self):
        """get_bookingids test with one argument"""
        booking = create_booking(update={'firstname': 'Januszek', 'lastname': 'Kowalski', 'totalprice': 212,
                                          'depositpaid': True,
                                          'bookingdates': {'checkin': '2022-01-01', 'checkout': '2022-01-02'},
                                          'additionalneeds': 'dinner'}).json()['bookingid']
        booking_list = get_bookingids(firstname="Januszek")
        assert booking_list.status_code == 200
        assert booking_list.json()[0]['bookingid'] == booking
        delete_booking(booking)

    def test_get_bookingids_fandlname(self):
        """get_bookingids test with two arguments"""
        create_booking(booking_data)
        assert get_bookingids(firstname="Jan", lastname="Kowalski").status_code == 200

    def test_get_bookingids_fname_empty(self):
        """get_bookingids test with empty firstname value"""
        create_booking(booking_data)
        assert get_bookingids(firstname="").status_code == 200

    def test_get_bookingids_checkin(self):
        """get_bookingids test with checkin value greater than in argument"""
        booking = create_booking(booking_data)
        booking_list = get_bookingids(checkin="2022-01-01")
        assert booking_list.status_code == 200
        assert {'bookingid': booking.json()['bookingid']} in booking_list.json()

    def test_get_bookingids_checkin_year(self):
        """get_bookingids test with only year in checkin value"""
        create_booking(booking_data)
        assert get_bookingids(checkin="2021").status_code == 200

    def test_get_bookingids_checkin_incorrect(self):
        """get_bookingids test with incorrect checkin value"""
        create_booking(booking_data)
        assert get_bookingids(checkin="20").status_code == 500

    def test_get_bookingids_checkin_empty(self):
        """get_bookingids test with empty checkin value"""
        create_booking(booking_data)
        assert get_bookingids(checkin="").status_code == 200

    def test_get_booking_id(self):
        """get_booking with correct id value"""
        booking = get_bookingids().json()[0]['bookingid']
        assert get_booking(booking).status_code == 200

    def test_get_booking_badid(self):
        """get_booking with incorrect id value"""
        assert get_booking(0).status_code == 404

    def test_create_booking_correct_value(self):
        """create_booking with correct values"""
        booking = create_booking(booking_data)
        assert booking.status_code == 200
        assert booking.json()['booking'] == booking_data

    def test_create_booking_no_additional(self):
        """create_booking with correct values without key 'additionalneeds'"""
        data = {'firstname': 'Jan',
                'lastname': 'Kowalski',
                'totalprice': 212,
                'depositpaid': True,
                'bookingdates': {'checkin': '2022-01-01', 'checkout': '2022-01-02'},
                }
        booking = create_booking(data)
        assert booking.status_code == 200
        assert booking.json()['booking'] == data

    def test_create_booking_incorrect_value(self):
        """create_booking with incorrect 'firstname' type"""
        assert create_booking(update={'firstname': 1, 'lastname': 'Kowalski', 'totalprice': 212,
                                      'depositpaid': True,
                                      'bookingdates': {'checkin': '2022-01-01', 'checkout': '2022-01-02'},
                                      'additionalneeds': 'dinner'}).status_code == 500

    def test_create_booking_empty_value(self):
        """create_booking with incorrect 'firstname' type"""
        assert create_booking(update={'firstname': None, 'lastname': 'Kowalski', 'totalprice': 212,
                                      'depositpaid': True,
                                      'bookingdates': {'checkin': '2022-01-01', 'checkout': '2022-01-02'},
                                      'additionalneeds': 'dinner'}).status_code == 500

    def test_create_token_correct(self):
        """create_token with correct admin and password values"""
        token = create_token("admin", "password123")
        assert token.status_code == 200

    def test_create_token_incorrect(self):
        """create_token with incorrect admin and password values"""
        token = create_token("admi", "assword123")
        assert token.status_code == 200  # bad credentials should give 4XX status code
        assert token.json() == {'reason': 'Bad credentials'}

    def test_create_token_empty(self):
        """create_token with empty admin and password values"""
        assert create_token("", "").json() == {'reason': 'Bad credentials'}

    def test_update_booking_correct(self):
        """update_booking with correct values"""
        booking = create_booking(booking_data).json()
        assert update_booking(booking['bookingid'],
                              update={'firstname': 'Henry', 'lastname': 'Kowalski', 'totalprice': 212,
                                      'depositpaid': False,
                                      'bookingdates': {'checkin': '2022-01-01', 'checkout': '2022-01-02'},
                                      'additionalneeds': 'no bed'}).status_code == 200

    def test_update_booking_lack_of_values(self):
        """update_booking with no 'depositpaid' value"""
        booking = create_booking(booking_data).json()
        assert update_booking(booking['bookingid'],
                              update={'firstname': 'Henry', 'lastname': 'Kowalski', 'totalprice': 212,
                                      'bookingdates': {'checkin': '2022-01-01', 'checkout': '2022-01-02'},
                                      'additionalneeds': 'no bed'}).status_code == 400

    def test_update_booking_incorrect_id(self):
        """update_booking with incorrect id"""
        assert update_booking(0, update={'firstname': 'Henry', 'lastname': 'Kowalski', 'totalprice': 212,
                                         'depositpaid': False,
                                         'bookingdates': {'checkin': '2022-01-01', 'checkout': '2022-01-02'},
                                         'additionalneeds': 'no bed'}).status_code == 405

    def test_update_booking_incorrect_values(self):
        """update_booking with incorrect values"""
        booking = create_booking(booking_data).json()
        assert update_booking(booking['bookingid'], update={'firstname': True, 'lastname': 123, 'totalprice': 'Ham',
                                                            'depositpaid': 'money',
                                                            'bookingdates': {'checkin': '2022-01-01',
                                                                             'checkout': '2022-01-02'},
                                                            'additionalneeds': 'no bed'}).status_code == 500

    def test_delete_booking(self):
        """delete_booking with correct id"""
        booking = create_booking(booking_data).json()
        booking_list = get_bookingids(checkin="2022-01-01")
        assert delete_booking(booking['bookingid']).status_code == 201
        assert {'bookingid': booking['bookingid']} not in booking_list.json()

    def test_delete_booking_incorrect_id(self):
        """delete_booking with incorrect id"""
        assert delete_booking(0).status_code == 405

    def test_partial_update_booking_correct(self):
        """partial_update with correct values"""
        booking = create_booking(booking_data).json()
        assert partial_update(booking['bookingid'], update={'firstname': 'Jan'}).status_code == 200

    def test_partial_update_booking_incorrect_firstname(self):
        """partial_update with incorrect firstname values"""  # bug, it can update firstname with different type
        booking = create_booking(booking_data).json()
        booking1 = partial_update(booking['bookingid'], update={'firstname': 2})
        assert booking1.status_code == 200
        assert booking1.json()['firstname'] == 2

    def test_partial_update_booking_incorrect_lastname(self):
        """partial_update with incorrect firstname values"""  # bug, it can update lastname with different type
        booking = create_booking(booking_data).json()
        booking1 = partial_update(booking['bookingid'], update={'lastname': True})
        assert booking1.status_code == 200
        assert booking1.json()['lastname'] == True

    def test_partial_update_booking_incorrect_checkin(self):
        """partial_update with incorrect firstname values"""  # bug, status code is 200 but data is not updated
        booking = create_booking(booking_data).json()
        booking1 = partial_update(booking['bookingid'], update={'checkin': True})
        assert booking1.status_code == 200
        assert booking1.json()['bookingdates']['checkin'] == '2022-01-01'
