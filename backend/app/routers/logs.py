from fastapi import APIRouter, Depends, HTTPException
from app.services.supabase_service import supabase
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/logs", tags=["Logs"])

@router.get("/")
def get_logs(current_user: dict = Depends(get_current_user)):
    try:
        
       response = (
            supabase.table("activity_logs")
            .select("""
                *,
                employees(name)
            """)
            .eq("company_id", current_user["company_id"])
            .order("created_at", desc=True)
            .limit(100)
            .execute()
        )


       return response.data

    except Exception as e:
        print("Logs Error:", e)
        raise HTTPException(status_code=500, detail="Failed to fetch logs")