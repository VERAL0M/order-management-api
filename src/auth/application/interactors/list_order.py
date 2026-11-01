from dataclasses import dataclass



from auth.application.interfaces.identity_provider import IdentityProvider
from auth.application.interfaces.user_data_gateway import UserDataGateway
from auth.application.interfaces.session_data_gateway import SessionDataGateway
from auth.application.interfaces.order_repository import OrderRepository
from auth.application.interfaces.request_manager import RequestManager
from auth.application.errors import AuthenticationError, OrderRequestError
from auth.domain.errors import AccessControlError


from auth.domain.entities.session import SessionId
from auth.domain.entities.user import UserId
from auth.domain.entities.order import  Order
from auth.domain.orders_status import OrderStatus
    
from auth.domain.user_role import UserRoleEnum


@dataclass
class StatusFilterOrderRequest:
    status: OrderStatus | None
    limit: int | None = None
    offset: int | None = None

@dataclass
class StatusFilterOrderResponse:
    items: list[Order] 

class StatusFilterOrderInteractor:
    def __init__(
        self,
        identity_provider: IdentityProvider,
        user_data_gateway: UserDataGateway,
        session_data_gateway: SessionDataGateway,
        request_manager: RequestManager,
        order_repository: OrderRepository,
        ):
        self._identity_provider = identity_provider
        self._user_data_gateway = user_data_gateway
        self._session_data_gateway = session_data_gateway
        self._request_manager = request_manager
        self._order_repository = order_repository

    async def __call__(self, 
                        request_data: StatusFilterOrderRequest, 
                        ) -> StatusFilterOrderResponse:
        is_authenticated: bool = await self._identity_provider.is_authenticated()

        if not is_authenticated:
            raise AuthenticationError("The user is not authorized. Sorting by order status is not possible.")

        session_id: SessionId | None = self._request_manager.get_session_id_from_request()
        if session_id is None:
            raise AuthenticationError("Session not found")


        user_id: UserId | None = await self._session_data_gateway.get_user_id(session_id=session_id)
        if user_id is None:
            raise AuthenticationError("The user ID was not found in the current session.")

        user_role: UserRoleEnum = await self._user_data_gateway.get_role(user_id=user_id)

        if request_data.offset is not None and request_data.offset < 0:
            raise OrderRequestError("Invalid offset value")

        if request_data.limit is not None and (request_data.limit < 1 or request_data.limit > 100):
            raise OrderRequestError("Invalid limit value")
        
        

        if user_role == UserRoleEnum.USER:
            list_order: list[Order] | None = await self._order_repository.list_by_user_id(
                user_id=user_id,
                status=request_data.status,
                limit=request_data.limit, 
                offset=request_data.offset
                )
            
        elif user_role == UserRoleEnum.ADMIN:
                
            list_order: list[Order] | None = await self._order_repository.list_all(
                status=request_data.status,
                limit=request_data.limit, 
                offset=request_data.offset

                )
        else:
            raise AccessControlError("Access error")
        
        return StatusFilterOrderResponse(items=list_order)

