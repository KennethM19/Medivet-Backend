from datetime import date
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query, File, Depends, UploadFile
from sqlalchemy.orm import Session, joinedload
from starlette import status

from database import get_db
from dependencies.auth import get_current_user
from firestore import delete_photo_from_firebase, upload_pet_image_to_firebase
from models import petsModel, usersModel
from schemes.petSchemes import PetResponse, PetCreate, PetUpdate

router =  APIRouter(prefix="/pets", tags=["Pets"])

#CREAR MASCOTA
@router.post("", response_model=PetResponse, status_code=status.HTTP_201_CREATED)
async def create_pet(request: PetCreate,  photo: Optional[UploadFile] = File(None), db: Session =  Depends(get_db), current_user: usersModel.Users = Depends(get_current_user)):

    if request.num_doc is not None:
        existing_pet = db.query(petsModel.Pets).filter(petsModel.Pets.num_doc == request.num_doc).first()

        if existing_pet:
            raise HTTPException(status_code=400, detail="Pet already exists")

    pet_data = request.model_dump()
    pet_data['user_id'] = current_user.id

    if photo is not None:
        contents = await photo.read()
        public_url = upload_pet_image_to_firebase(contents, photo.filename)
        pet_data['photo'] = public_url

    db_pet = petsModel.Pets(**pet_data)
    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)
    return db_pet

#SUBIR FOTO
@router.post("/upload-photo")
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
@router.put("/update-photo")
async def update_photo(
    pet_id: int,
    photo: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: usersModel.Users = Depends(get_current_user)
):
    pet = db.query(petsModel.Pets).filter(petsModel.Pets.id == pet_id).first()

    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")

    if pet.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot update photo for another user's pet"
        )

    # Si ya tiene foto, eliminarla de Firebase
    if pet.photo:
        delete_photo_from_firebase(pet.photo)

    # Subir nueva foto
    contents = await photo.read()
    public_url = upload_pet_image_to_firebase(contents, photo.filename)

    # Guardar URL en la mascota
    pet.photo = public_url
    db.commit()
    db.refresh(pet)

    return {
        "message": "Updated pet photo",
        "url": public_url
    }


#BORRAR FOTO
@router.delete("/delete-photo")
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
        # FILTROS
        user_id: Optional[int] = Query(None, description="Filter by user ID"),
        species_id: Optional[int] = Query(None, description="Filter by species"),
        breed_id: Optional[int] = Query(None, description="Filter by breed"),
        sex_id: Optional[int] = Query(None, description="Filter by sex"),
        neutered: Optional[bool] = Query(None, description="Filter by neutered status"),
        name: Optional[str] = Query(None, description="Filter by name (contains)"),
        pet_id: Optional[int] = Query(None, description="Filter by pet ID"),

        # PAGINACION
        skip: int = Query(0, ge=0, description="Skip records"),
        limit: int = Query(100, ge=1, le=1000, description="Limit records"),

        # ORDENAMIENTO
        sort_by: str = Query("name", description="Field to sort by"),
        sort_order: str = Query("asc", regex="^(asc|desc)$", description="Sort order"),

        db: Session = Depends(get_db)
):
    query = db.query(petsModel.Pets) \
        .join(petsModel.Breed, isouter=True) \
        .join(petsModel.Species, isouter=True) \
        .join(petsModel.Sex, isouter=True) \
        .options(
            joinedload(petsModel.Pets.breed),
            joinedload(petsModel.Pets.specie),
            joinedload(petsModel.Pets.sex),
            joinedload(petsModel.Pets.user)
        )

    # FILTROS
    if pet_id:
        query = query.filter(petsModel.Pets.id == pet_id)
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

    pets = query.offset(skip).limit(limit).all()

    # Convertir directamente a PetResponse
    result = []
    for pet in pets:
        age = calculate_age(pet.year_birth, pet.month_birth)
        pet_response = PetResponse(
            id=pet.id,
            name=pet.name,
            year_birth=pet.year_birth,
            month_birth=pet.month_birth,
            age=age,
            weight=pet.weight,
            photo=pet.photo,
            neutered=pet.neutered,
            sex=pet.sex,
            species=pet.specie,
            breed=pet.breed,
            user=pet.user
        )
        result.append(pet_response)

#OBTENER MASCOTA POR ID
@router.get("/{pet_id}", response_model=PetResponse, status_code=status.HTTP_200_OK)
def get_pet(pet_id: int, db: Session = Depends(get_db)):
    pet = db.query(petsModel.Pets).filter(petsModel.Pets.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    return pet

#EDITAR MASCOTA
@router.put("", response_model=PetResponse)
def update_pet(
    pet_id: int,
    request: PetUpdate,
    db: Session = Depends(get_db),
    current_user: usersModel.Users = Depends(get_current_user)
):
    pet = db.query(petsModel.Pets).filter(petsModel.Pets.id == pet_id).first()

    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")

    if pet.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot update pet for another user"
        )

    updated_fields = request.model_dump(exclude_unset=True)

    if "user_id" in updated_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot change pet owner"
        )

    allowed_fields = {"weight", "neutered", "photo"}
    for field, value in updated_fields.items():
        if field in allowed_fields:
            setattr(pet, field, value)

    db.commit()
    db.refresh(pet)
    return pet

@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
def delete_pet(
    pet_id: int,
    db: Session = Depends(get_db),
    current_user: usersModel.Users = Depends(get_current_user)
):
    # Buscar la mascota
    pet = db.query(petsModel.Pets).filter(petsModel.Pets.id == pet_id).first()

    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")

    # Validar que el dueño sea el usuario autenticado
    if pet.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot delete pet for another user"
        )

    # Eliminar
    db.delete(pet)
    db.commit()
    return {"detail": "Pet deleted successfully"}


def calculate_age(year_birth: int, month_birth: int):
    today = date.today()
    years = today.year - year_birth
    months = today.month - month_birth

    if months < 0:
        years -= 1
        months += 12

    return {"years": years, "months": months}
