import { createClient } from "@supabase/supabase-js";

const supabaseUrl = "https://dcipitpcohvsmexkfovz.supabase.co";
const supabaseAnonKey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRjaXBpdHBjb2h2c21leGtmb3Z6Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTYwMTEyMSwiZXhwIjoyMDg3MTc3MTIxfQ.w6H5-4BxbY_o76Wq9gkcDjzqmHgN_6PNh6DDP1eWBSg";

export const supabase = createClient(supabaseUrl, supabaseAnonKey);