import asyncio
import time
from app.models import ProductStatus
from app.repositories.productrepository import ProductRepository
from datetime import datetime

async def check_end_auction(auction_id):
    while True:
        product = await ProductRepository().get_id(auction_id)
        now = datetime.utcnow()
        if product.end_date <= now:
            print("Аукцион завершен")
            product_data = product.to_dict()
            product_data['status'] = ProductStatus.COMPLETED
            await ProductRepository().update(product, product_data)
            break
        asyncio.sleep(60)

    

    