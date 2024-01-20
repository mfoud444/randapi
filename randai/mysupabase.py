import os
from supabase import create_client, Client

# url: str = os.environ.get("SUPABASE_URL")
# key: str = os.environ.get("SUPABASE_KEY")
url="https://fvpmikdmeystnnxnloqe.supabase.co"
key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ2cG1pa2RtZXlzdG5ueG5sb3FlIiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTY5NDQ1OTYsImV4cCI6MjAxMjUyMDU5Nn0.2M-NejfxfGlU1guyRIfNKL7kE94WysWj_T-NmFXypSg"
supabase: Client = create_client(url, key)

