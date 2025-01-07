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
    
    def start_auction(self, data: ProductBody, user: User, bg: BackgroundTasks):
        data_dict = data.model_dump()
        data_dict['start_date'] = datetime.utcnow()
        data_dict['current_price'] = data_dict['start_price']
        product_id = ProductRepository().create(data_dict, user)
        bg.add_task(check_end_auction, product_id)
        return product_id
    
    
    def create_bet(self, user: User, productid: int, data: BetBody):
        data_dict = data.model_dump()
        product = ProductRepository().get_id(productid)
        if not product:
            raise HTTPException(status_code=404, detail="Товар не найден")
        
        if product.status == ProductStatus.COMPLETED:
            raise HTTPException(status_code=400, detail="Аукцион завершен")
        
        if product.current_price >= data.bet_price:
            raise HTTPException(status_code=400, detail="Ставка дожна быть выше, чем текущая")
        
        product_data = product.to_dict()
        product_data['current_price'] = data.bet_price
        product_data['current_winner_id'] = user.id
        ProductRepository().update(product, product_data)
        return BetRepository().create(data_dict, user, product)
    

    def delete_product(self, user: User, id: int):
        for product in user.products:
            if product.id == id:
                return ProductRepository().delete(id)
        raise HTTPException(status_code=404, detail="Товар не найден")