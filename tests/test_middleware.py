import pytest

from django.conf import settings

from django_ent.middleware import CASMiddleware

pytestmark = pytest.mark.django_db

ENT_QUERY_STRING_TRIGGER = settings.ENT_QUERY_STRING_TRIGGER


class TestCASMiddleware:
    @staticmethod
    def test_init():
        """Testing the __init__ method"""
        # WHEN
        cas_middleware = CASMiddleware("dump_response")

        # THEN
        assert cas_middleware.get_response == "dump_response"

    def test_no_uai_no_ticket(self, request_builder):
        """Testing the middleware if not a connection to ent"""
        # GIVEN
        cas_middleware = CASMiddleware(request_builder.get)

        # WHEN
        response = cas_middleware(request_builder.get())

        # THEN
        assert cas_middleware.get_response().path == "/"
        assert ENT_QUERY_STRING_TRIGGER not in response.GET
        assert "ticket" not in response.GET

    def test_when_uai_number(self, user, request_builder):
        """Testing the __call__ method with uai_number in url"""
        # GIVEN
        uai_number = user.entinstitution.uai
        query_params = "/?{}={}".format(ENT_QUERY_STRING_TRIGGER, uai_number)
        request = request_builder.get(query_params)
        cas_middleware = CASMiddleware(request)

        # WHEN
        response = cas_middleware(request)

        # THEN
        assert settings.ENT_HDF_BASE_URL in response.url

    def test_when_cas_ticket_valid(
        self, mock_validate_valid_ticket, user, request_builder
    ):
        """
        Testing the __call__ method with valid cas_ticket in url and user
        has access (is_active is True)
        """
        # GIVEN
        uai_number = user.entinstitution.uai
        cas_ticket = "this-is-a-ticket"
        query_params = "/?ticket={}".format(cas_ticket)
        request = request_builder.get(query_params)
        request.session["uai_number"] = uai_number
        request.session["is_ent"] = uai_number
        cas_middleware = CASMiddleware(request_builder.get)

        # WHEN
        cas_middleware(request)

        # THEN
        assert mock_validate_valid_ticket.call_count == 1

    def test_when_cas_ticket_invalid(
        self, mock_validate_invalid_ticket, request_builder
    ):
        """
        Testing the __call__ method with invalid cas_ticket in url and user
        has access (is_active is True)
        """
        # GIVEN
        uai_number = "invalid-uai"
        cas_ticket = "this-is-a-ticket"
        query_params = "/?ticket={}".format(cas_ticket)
        request = request_builder.get(query_params)
        request.session["uai_number"] = uai_number
        request.session["is_ent"] = uai_number
        cas_middleware = CASMiddleware(request_builder.get)

        # WHEN
        response = cas_middleware(request)

        # THEN
        assert response.status_code == 302
        assert mock_validate_invalid_ticket.call_count == 1

    def test_institution_does_not_exist(self, request_builder):
        """Testing the __call_ method with an unknown institution"""
        # GIVEN
        uai_number = "fake-uai"
        query_params = "/?{}={}".format(ENT_QUERY_STRING_TRIGGER, uai_number)
        request = request_builder.get(query_params)
        request.session["uai_number"] = uai_number
        cas_middleware = CASMiddleware(request)

        # WHEN
        cas_middleware(request)

        # THEN
        assert cas_middleware.get_response.path == "/"

    @pytest.mark.parametrize(
        "uai_number, ent",
        [
            ("9999999Q", "HDF"),
            ("EXPDATA2MIDIPY", "OCCITANIE"),
            ("031MONITORING", "OCCITANIEAGR"),
            ("VAUCLUSE", "GMINVENT"),
        ],
    )
    def test_validate_ticket(
        self, uai_number, ent, mock_verification_response, request_builder
    ):
        # GIVEN
        request = request_builder.get()
        request.session["uai_number"] = uai_number
        request.session["ent"] = ent

        # WHEN
        mock_verification_response.get(ent)
        uai_numbers = CASMiddleware.validate_ticket(request, "dummy-ticket")

        # THEN
        assert uai_number in uai_numbers
        mock_verification_response.assert_called_once()

    @pytest.mark.parametrize(
        "uai_number, ent",
        [("9999999Q", "HDF"), ("EXPDATA2MIDIPY", "OCCITANIE")],
    )
    def test_validate_ticket_parse_error(
        self, uai_number, ent, mocker, request_builder
    ):
        # GIVEN
        mocker.patch(
            "cas.CASClientV2.get_verification_response",
            return_value="""<?xml version="1.0"?>
            <catalog>
               <book id="bk101">
                  <author>Gambardella, Matthew</author>
                  <title>XML Developer's Guide</title>
                  <genre>Computer</genre>
                  <price>44.95</price>
                  <publish_date>2000-10-01</publish_date>
                  <description>An in-depth look at creating applications 
                  with XML.</description>
               </book>
           </catalog>""",
        )
        request = request_builder.get()
        uai_number = "invalid-uai"
        request.session["uai_number"] = uai_number
        request.session["ent"] = ent

        # WHEN
        response = CASMiddleware.validate_ticket(request, "dummy-ticket")

        # THEN
        assert not response
