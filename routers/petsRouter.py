from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query, File, Depends, UploadFile
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from dependencies.auth import get_current_user
from firestore import upload_user_image_to_firebase, delete_photo_from_firebase, upload_pet_image_to_firebase
from models import petsModel, usersModel
from schemes.petSchemes import PetResponse, PetCreate, PetUpdate

router =  APIRouter(prefix="/pets", tags=["Pets"])

#CREAR MASCOTA
@router.post("", response_model=PetResponse, status_code=status.HTTP_201_CREATED)
def create_pet(request: PetCreate, db: Session =  Depends(get_db), current_user: usersModel.Users = Depends(get_current_user)):

    if request.num_doc is not None:
        existing_pet = db.query(petsModel.Pets).filter(petsModel.Pets.num_doc == request.num_doc).first()

        if existing_pet:
            raise HTTPException(status_code=400, detail="Pet already exists")

    pet_data = request.model_dump()
    pet_data['user_id'] = current_user.id

    db_pet = petsModel.Pets(**pet_data)
    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)
    return db_pet

#SUBIR FOTO
@router.post("/upload-photo/{pet_id}")
async def upload_photo(
        pet_id: int,
        photo: UploadFile = File(...),
        db: Session = Depends(get_db),
        current_user: usersModel.Users = Depends(get_current_user),
):
    pet = db.query(petsModel.Pets).filter(petsModel.Pets.id == pet_id).first()
    contents = await photo.read()
    public_url = upload_pet_image_to_firebase(contents, photo.filename)

    pet.photo = public_url
    db.commit()
    db.refresh(pet)

    return {
        "message": "Updated profile photo",
        "url": public_url
    }

#ACTUALIZAR FOTO
@router.put("/update-photo/{pet_id}")
async def update_photo(
        pet_id: int,
        photo: UploadFile = File(...),
        db: Session = Depends(get_db),
        current_user: usersModel.Users = Depends(get_current_user)
) :
    pet = db.query(petsModel.Pets).filter(petsModel.Pets.id == pet_id).first()

    if pet.photo:
        delete_photo_from_firebase(pet.photo)

    contents = await photo.read()
    public_url = upload_pet_image_to_firebase(contents, photo.filename)

    current_user.photo = public_url
    db.commit()
    db.refresh(current_user)
    return {
        "message": "Updated pet photo",
    }

#BORRAR FOTO
@router.delete("/delete-photo/{pet_id}")
def delete_photo(
        pet_id: int,
        current_user: usersModel.Users = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    pet = db.query(petsModel.Pets).filter(petsModel.Pets.id == pet_id).first()
    if pet.photo:
        delete_photo_from_firebase(pet.photo)
        pet.photo = None
        db.commit()
        db.refresh(pet)
        return {
            "message": "Deleted pet photo",
        }
    raise HTTPException(status_code=404, detail="Photo not found")

#OBTENER TODAS LAS MASCOTAS
@router.get("", response_model=List[PetResponse])
def get_all_pets(
        #FILTROS
        user_id: Optional[int] = Query(None, description="Filter by user ID"),
        species_id: Optional[int] = Query(None, description="Filter by species"),
        breed_id: Optional[int] = Query(None, description="Filter by breed"),
        sex_id: Optional[int] = Query(None, description="Filter by sex"),
        neutered: Optional[bool] = Query(None, description="Filter by neutered status"),
        name: Optional[str] = Query(None, description="Filter by name (contains)"),

        #PAGINACION
        skip: int = Query(0, ge=0, description="Skip records"),
        limit: int = Query(100, ge=1, le=1000, description="Limit records"),

        #ORDENAMIENTO
        sort_by: str = Query("name", description="Field to sort by"),
        sort_order: str = Query("asc", regex="^(asc|desc)$", description="Sort order"),

        db: Session = Depends(get_db)
):
    query = db.query(petsModel.Pets)

    #SE APLICAN LOS FILTROS
    if user_id:
        query = query.filter(petsModel.Pets.user_id == user_id)
    if species_id:
        query = query.filter(petsModel.Pets.specie_id == species_id)
    if breed_id:
        query = query.filter(petsModel.Pets.breed_id == breed_id)
    if sex_id:
        query = query.filter(petsModel.Pets.sex_id == sex_id)
    if neutered is not None:
        query = query.filter(petsModel.Pets.neutered == neutered)
    if name:
        query = query.filter(petsModel.Pets.name.ilike(f"%{name}%"))

    #SE APLICA EL ORDEN
    sort_field = getattr(petsModel.Pets, sort_by, None)
    if sort_field is not None:
        if sort_order == "desc":
            query = query.order_by(sort_field.desc())
        else:
            query = query.order_by(sort_field.asc())
    else:
        #ORDEN POR DEFECTO
        query = query.order_by(petsModel.Pets.name.asc())

    return query.offset(skip).limit(limit).all()

#OBTENER MASCOTA POR ID
@router.get("/{pet_id}", response_model=PetResponse, status_code=status.HTTP_200_OK)
def get_pet(pet_id: int, db: Session = Depends(get_db)):
    pet = db.query(petsModel.Pets).filter(petsModel.Pets.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    return pet

#OBTENER MASCOTA POR USUARIO
@router.get("/{user_id}", response_model= PetResponse, status_code=status.HTTP_200_OK)
def get_pet_by_user(user_id: int, db: Session = Depends(get_db)):
    pet = db.query(petsModel.Pets).filter(petsModel.Pets.user_id == user_id).all()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    return pet

#EDITAR MASCOTA
@router.put("/{pet_id}", response_model=PetResponse)
def update_pet(pet_id: int, request: PetUpdate, db: Session = Depends(get_db), current_user: usersModel.Users = Depends(get_current_user)):
    pet = db.query(petsModel.Pets).filter(petsModel.Pets.id == pet_id).first()

    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")

    if pet.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot update pet for another user"
        )

    updated_pet = request.model_dump(exclude_unset=True)

    if 'user_id' in update_pet:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot change pet owner"
        )

    for field, value in updated_pet.items():
        setattr(pet, field, value)

    db.commit()
    db.refresh(pet)
    return pet
