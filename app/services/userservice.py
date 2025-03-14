from datetime import datetime
from fastapi import HTTPException
from app.db.models import Product, ProductStatus, User
from app.repositories.userrepository import UserRepository
from app.repositories.productrepository import ProductRepository
from app.repositories.betrepository import BetRepository
from app.schemas import ProductBody, BetBody
from fastapi import BackgroundTasks
from app.tasks import check_end_auction
from exceptions import ProductNotFoundException, AuctionCompletedException, UserNotCorrectBetException

class UserService:
    def __init__(
        self, 
        user_repository: UserRepository,
        product_repository: ProductRepository,
        bet_repository: BetRepository
    ):
        self.user_repository = user_repository
        self.product_repository = product_repository
        self.bet_repository = bet_repository
    
    async def start_auction(self, data: ProductBody, user_id: int, bg: BackgroundTasks) -> int:
        data_dict = data.model_dump()
        data_dict['start_date'] = datetime.utcnow().replace(tzinfo=None)
        data_dict["end_date"] = data.end_date.replace(tzinfo=None)
        data_dict['current_price'] = data_dict['start_price']
        data_dict['user_id'] = user_id
        
        product_id = await self.product_repository.create(data_dict)
        bg.add_task(check_end_auction, product_id)
        return product_id
    
    
    async def create_bet(self, user_id: int, productid: int, data: BetBody) -> int:
        data_dict = data.model_dump()
        product = await self.product_repository.get_id(productid)
        if not product:
            raise ProductNotFoundException
        
        if product.status == ProductStatus.COMPLETED:
            raise AuctionCompletedException
        
        if product.current_price >= data.bet_price:
            raise UserNotCorrectBetException
        
        product_data = product.to_dict()
        product_data['current_price'] = data.bet_price
        product_data['current_winner_id'] = user_id
        product_data['id'] = product.id

        data_dict['product_id'] = product.id
        data_dict['user_id'] = user_id
        await self.product_repository.update(product, product_data)
        return await self.bet_repository.create(data_dict)
    

    async def delete_product(self, user_id: int, product_id: int) -> None:
        products = await self.user_repository.get_products(user_id)
        for product in products:
            if product.id == product_id:
                bids = await self.product_repository.get_bids(product_id)
                for bet in bids:
                    await self.bet_repository.delete(bet.id)
                return await self.product_repository.delete(product_id)
        raise ProductNotFoundException
    
    async def my_products(self, user_id: int) -> list[Product]:
        return await self.user_repository.get_products(user_id)
    
    async def check_product(self, product_id: int) -> Product:
        return await self.product_repository.get_id(product_id)
    
    async def search_product(self, query: str) -> list[Product]:
        return await self.product_repository.get_search(query)