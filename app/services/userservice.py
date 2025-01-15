from datetime import datetime
from fastapi import HTTPException
from app.models import ProductStatus, User
from app.repositories.userrepository import UserRepository
from app.repositories.productrepository import ProductRepository
from app.repositories.betrepository import BetRepository
from app.schemas import ProductBody, BetBody
from fastapi import BackgroundTasks
from app.tasks import check_end_auction

class UserService:
    
    async def start_auction(self, data: ProductBody, user_id: int, bg: BackgroundTasks):
        data_dict = data.model_dump()
        data_dict['start_date'] = datetime.utcnow().replace(tzinfo=None)
        data_dict["end_date"] = data.end_date.replace(tzinfo=None)
        data_dict['current_price'] = data_dict['start_price']
        data_dict['user_id'] = user_id
        
        product_id = await ProductRepository().create(data_dict)
        bg.add_task(check_end_auction, product_id)
        return product_id
    
    
    async def create_bet(self, user_id: int, productid: int, data: BetBody):
        data_dict = data.model_dump()
        product = await ProductRepository().get_id(productid)
        if not product:
            raise HTTPException(status_code=404, detail="Товар не найден")
        
        if product.status == ProductStatus.COMPLETED:
            raise HTTPException(status_code=400, detail="Аукцион завершен")
        
        if product.current_price >= data.bet_price:
            raise HTTPException(status_code=400, detail="Ставка дожна быть выше, чем текущая")
        
        product_data = product.to_dict()
        product_data['current_price'] = data.bet_price
        product_data['current_winner_id'] = user_id
        product_data['id'] = product.id

        data_dict['product_id'] = product.id
        data_dict['user_id'] = user_id
        await ProductRepository().update(product, product_data)
        return await BetRepository().create(data_dict)
    

    async def delete_product(self, user_id: int, product_id: int):
        products = await UserRepository().get_products(user_id)
        for product in products:
            if product.id == product_id:
                return await ProductRepository().delete(product_id)
        raise HTTPException(status_code=404, detail="Товар не найден")
    
    async def my_products(self, user_id: int):
        return await UserRepository().get_products(user_id)
    
    async def check_product(self, product_id: int):
        return await ProductRepository().get_id(product_id)
    
    async def search_product(self, query: str):
        return await ProductRepository().get_search(query)