// Create this file at: src/lib/services/supabaseClient.js

import { createClient } from '@supabase/supabase-js'

// IMPORTANT: Replace with your actual Supabase Project URL and Anon Key
// It's best practice to store these in environment variables
const supabaseUrl = 'https://ymvbkeffjqrqqykdhoqk.supabase.co'
const supabaseAnonKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InltdmJrZWZmanFycXF5a2Rob3FrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTIyMDY5MDgsImV4cCI6MjA2Nzc4MjkwOH0.2Lw7oxrGn-z4P2AEYGlBM80aUdbqO9B_9piFo2HmZfg'

export const supabase = createClient(supabaseUrl, supabaseAnonKey)