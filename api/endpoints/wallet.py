import logging
from flask import request
from flask_restplus import Resource
from api.controllers.wallet import get_holdings, get_holding, get_holdings_historical
from api.repositories.models.serialisers import holding
from api.restplus import api
from api import auth
from api.cache import cache


log = logging.getLogger(__name__)

ns = api.namespace('wallet', description='Operations related to wallet holdings')

CACHE_PREFIX = 'auth:'


@ns.route('/')
class HoldingsCollection(Resource):
    @api.marshal_list_with(holding)
    @auth.requires_auth
    def get(self):
        """
        Returns list of Holdings
        """
        cache_key = CACHE_PREFIX + request.headers.get("Authorization", None)
        rv = cache.get(cache_key)
        if rv is None:
            user_info = auth.get_userinfo_with_token()
            rv = user_info['email']
            cache.set(cache_key, rv, timeout=60 * 50)
        response = get_holdings(rv)
        return response, 200


@ns.route('/<string:ticker>')
@api.response(404, 'Holdings not found.')
class HoldingItem(Resource):
    @auth.requires_auth
    @api.marshal_with(holding)
    def get(self, ticker):
        """
        Returns list of Holdings
        # """
        cache_key = CACHE_PREFIX + request.headers.get("Authorization", None)
        rv = cache.get(cache_key)
        if rv is None:
            user_info = auth.get_userinfo_with_token()
            rv = user_info['email']
            cache.set(cache_key, rv, timeout=60 * 50)

        response = get_holding(rv, ticker)
        return response, 200


@auth.requires_auth
@ns.route('/historical/')
class HistoricalHoldings(Resource):
    def get(self):
        cache_key = CACHE_PREFIX + request.headers.get("Authorization", None)
        rv = cache.get(cache_key)
        if rv is None:
            user_info = auth.get_userinfo_with_token()
            rv = user_info['email']
            cache.set(cache_key, rv, timeout=60 * 50)
        response = get_holdings_historical()
        return response, 200


# @auth.requires_auth
# @ns.route('/historical/<string:ticker>')
# class HistoricalHolding(Resource):
#     def get(self, ticker):
#         cache_key = CACHE_PREFIX + request.headers.get("Authorization", None)
#         rv = cache.get(cache_key)
#         if rv is None:
#             user_info = auth.get_userinfo_with_token()
#             rv = user_info['email']
#             cache.set(cache_key, rv, timeout=60 * 50)
#             response = get_historical_holding(ticker)
#         return response, 200
