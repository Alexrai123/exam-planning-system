from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import pandas as pd
import io

from ..db.base import get_db
from ..models.user import User, UserRole
from ..models.grupa import Grupa
from ..core.security import get_password_hash
from ..routes.auth import get_current_user, is_secretariat

router = APIRouter(prefix="/group-leaders", tags=["Group Leaders"])

@router.post("/upload", status_code=status.HTTP_200_OK)
async def upload_group_leaders(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(is_secretariat)
):
    """
    Upload a list of group leaders from an Excel file.
    Only secretariat users can access this endpoint.
    The Excel file should contain at least two columns: 'Name' and 'Email'.
    Emails must be of the form @student.usv.ro.
    """
    # Check file extension
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only Excel files (.xlsx, .xls) are allowed"
        )
    
    try:
        # Read Excel file
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents))
        
        # Validate columns
        required_columns = ['Name', 'Email', 'Group']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Missing required columns: {', '.join(missing_columns)}"
            )
        
        # Process data
        created_users = 0
        updated_groups = 0
        errors = []
        
        for index, row in df.iterrows():
            # Create a savepoint for this row
            try:
                name = row['Name']
                email = row['Email']
                # Ensure group_name is always a string, even if it's a number
                group_name = str(row['Group'])
                
                # Validate email format
                if not email or '@student.usv.ro' not in email:
                    errors.append(f"Row {index+2}: Email must be of the form @student.usv.ro")
                    continue
                
                # Process each row in its own transaction
                try:
                    # Check if group exists
                    group = db.query(Grupa).filter(Grupa.name == group_name).first()
                    if not group:
                        errors.append(f"Row {index+2}: Group '{group_name}' not found")
                        continue
                    
                    # Skip groups that already have a leader assigned
                    if group.leader_id is not None:
                        errors.append(f"Row {index+2}: Group '{group_name}' already has a leader assigned")
                        continue
                    
                    # Check if user already exists
                    user = db.query(User).filter(User.email == email).first()
                    
                    if user:
                        # Update existing user
                        user.name = name
                        user.role = UserRole.STUDENT
                    else:
                        # Create new user with a default password
                        default_password = "student123"  # This should be changed by the user on first login
                        user = User(
                            name=name,
                            email=email,
                            password=get_password_hash(default_password),
                            role=UserRole.STUDENT
                        )
                        db.add(user)
                        db.flush()
                        created_users += 1
                    
                    # Update group with leader
                    group.leader_id = user.id
                    db.flush()
                    updated_groups += 1
                    
                    # Commit this row's changes
                    db.commit()
                    
                except Exception as e:
                    # Roll back this row's changes
                    db.rollback()
                    errors.append(f"Row {index+2}: {str(e)}")
                    
            except Exception as e:
                errors.append(f"Row {index+2}: {str(e)}")
        
        return {
            "message": "Group leaders uploaded successfully",
            "created_users": created_users,
            "updated_groups": updated_groups,
            "errors": errors
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing file: {str(e)}"
        )
