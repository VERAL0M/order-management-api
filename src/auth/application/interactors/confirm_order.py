from dataclasses import dataclass
from auth.application.interfaces.identity_provider import IdentityProvider
from auth.application.interfaces.order_repository import OrderRepository
from auth.application.interfaces.request_manager import RequestManager
from auth.application.interfaces.session_data_gateway import SessionDataGateway
from auth.application.interfaces.transaction_manager import TransactionManager
from auth.application.interfaces.user_data_gateway import UserDataGateway
from auth.domain.entities.order import Order, OrderId
from auth.domain.entities.session import SessionId
from auth.domain.entities.user import UserId
from auth.application.errors import  AuthenticationError, OrderConfirmError, OrderFindError
from auth.domain.errors import AccessControlError
from auth.domain.user_role import UserRoleEnum
from auth.domain.errors import OrderStateError



@dataclass
class ConfirmOrderRequest:
    order_id: OrderId


@dataclass
class ConfirmOrderResponse:
    order: Order


class ConfirmOrderInteractor:
    def __init__(
        self,
        identity_provider: IdentityProvider,
        user_data_gateway: UserDataGateway,
        session_data_gateway: SessionDataGateway,
        request_manager: RequestManager,
        order_repository: OrderRepository,
        transaction_manager: TransactionManager,
    ):
        self._identity_provider = identity_provider
        self._user_data_gateway = user_data_gateway
        self._session_data_gateway = session_data_gateway
        self._request_manager = request_manager
        self._order_repository = order_repository
        self._transaction_manager = transaction_manager
    
    async def __call__(self, request_data: ConfirmOrderRequest) -> ConfirmOrderResponse:
        is_authenticated: bool = await self._identity_provider.is_authenticated()
        if not is_authenticated:
            raise AuthenticationError("You are not authenticated.")
    
        session_id: SessionId | None = self._request_manager.get_session_id_from_request()
        if session_id is None:
            raise AuthenticationError("Session not found")
    
        user_id: UserId | None = await self._session_data_gateway.get_user_id(session_id=session_id)
        if user_id is None:
            raise AuthenticationError("User not found")
    
        order: Order | None = await self._order_repository.get_by_id(order_id=request_data.order_id)
        if order is None:
            raise OrderFindError("Order not found")
    
        user_role: UserRoleEnum | None = await self._user_data_gateway.get_role(user_id=user_id)
        if user_role != UserRoleEnum.ADMIN:
            raise AccessControlError("You are not authorized to confirm this order")
    
        try:
            order.confirm()
        except OrderStateError as error:
            raise OrderConfirmError(str(error)) from error
    
        await self._transaction_manager.commit()
    
    
        return ConfirmOrderResponse(order=order)
        
    
