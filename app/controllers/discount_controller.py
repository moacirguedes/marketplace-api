from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.discount_schema import DiscountCreate, DiscountResponse, DiscountUpdate
from app.services.discount_service import DiscountService
from app.dependencies.auth import is_admin

router = APIRouter()


@router.get(
    "/",
    response_model=list[DiscountResponse],
    summary="Obter todos os descontos",
    description="Retorna uma lista contendo todos os descontos cadastrados no sistema.",
)
def get_discounts(db: Session = Depends(get_db)):
    return DiscountService.get_all_discounts(db)


@router.get(
    "/{discount_id}",
    response_model=DiscountResponse,
    summary="Obter um desconto específico",
    description="Retorna detalhes de um desconto específico com base no seu ID.",
    responses={404: {"description": "Desconto não encontrado"}},
)
def get_discount(discount_id: int, db: Session = Depends(get_db)):
    discount = DiscountService.get_discount_by_id(db, discount_id)
    if not discount:
        raise HTTPException(status_code=404, detail="Desconto não encontrado")
    return discount


@router.post(
    "/",
    response_model=DiscountResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar um novo desconto",
    description="Cria um novo desconto. Requer privilégios de administrador.",
    responses={
        401: {"description": "Não autorizado"},
        403: {"description": "Acesso negado"},
        404: {"description": "Produto não encontrado"},
    },
)
def create_discount(
    discount_data: DiscountCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(is_admin),
):
    return DiscountService.create_discount(db, discount_data)


@router.put(
    "/{discount_id}",
    response_model=DiscountResponse,
    summary="Atualizar um desconto",
    description="Atualiza informações de um desconto específico com base no seu ID. Requer privilégios de administrador.",
    responses={
        404: {"description": "Desconto não encontrado"},
        404: {"description": "Produto não encontrado"},
        401: {"description": "Não autorizado"},
        403: {"description": "Acesso negado"},
    },
)
def update_discount(
    discount_id: int,
    discount_data: DiscountUpdate,
    db: Session = Depends(get_db),
    _: dict = Depends(is_admin),
):
    return DiscountService.update_discount(db, discount_id, discount_data)


@router.delete(
    "/{discount_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Excluir um desconto",
    description="Exclui um desconto específico com base no seu ID. Requer privilégios de administrador.",
    responses={
        404: {"description": "Desconto não encontrado"},
        401: {"description": "Não autorizado"},
        403: {"description": "Acesso negado"},
    },
)
def delete_discount(
    discount_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(is_admin),
):
    DiscountService.delete_discount(db, discount_id)
