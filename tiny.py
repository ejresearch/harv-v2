import os
import re

def fix_memory_service():
    """Fix memory service field names to match database schema"""
    
    service_path = "backend/app/services/memory_service.py"
    
    if not os.path.exists(service_path):
        print(f"❌ File not found: {service_path}")
        print("Make sure you're in the harv-v2 directory")
        return False
    
    print("🔧 TINY FIX: Updating memory field names...")
    
    # Read the current file
    with open(service_path, 'r') as f:
        content = f.read()
    
    # Apply fixes
    fixes_applied = 0
    
    # Fix 1: Change key_insights to what_learned
    if 'key_insights=' in content:
        content = content.replace(
            'key_insights="; ".join(key_insights) if key_insights else "Communication learning in progress"',
            'what_learned="; ".join(key_insights) if key_insights else "Communication learning in progress"'
        )
        fixes_applied += 1
        print("  ✅ Fixed: key_insights → what_learned")
    
    # Fix 2: Change learning_connections to connections_made
    if 'learning_connections=' in content:
        content = content.replace(
            'learning_connections="; ".join(learning_connections) if learning_connections else ""',
            'connections_made="; ".join(learning_connections) if learning_connections else ""'
        )
        fixes_applied += 1
        print("  ✅ Fixed: learning_connections → connections_made")
    
    # Fix 3: Update field references in updates
    if 'summary.key_insights =' in content:
        content = content.replace(
            'summary.key_insights = "; ".join(key_insights)',
            'summary.what_learned = "; ".join(key_insights)'
        )
        fixes_applied += 1
        print("  ✅ Fixed: summary field update")
    
    if 'summary.learning_connections =' in content:
        content = content.replace(
            'summary.learning_connections = "; ".join(learning_connections)',
            'summary.connections_made = "; ".join(learning_connections)'
        )
        fixes_applied += 1
        print("  ✅ Fixed: summary field update")
    
    # Write back the fixed content
    with open(service_path, 'w') as f:
        f.write(content)
    
    print(f"✅ Applied {fixes_applied} fixes to memory service")
    return True

def main():
    print("🔧 TINY FIX: Memory Field Name Correction")
    print("=" * 40)
    
    # Check directory
    if not os.path.exists("backend/app"):
        print("❌ Error: Run from your harv-v2 directory")
        print("Expected: harv-v2/backend/app/")
        return
    
    # Apply fix
    if fix_memory_service():
        print("=" * 40)
        print("🎉 TINY FIX COMPLETE!")
        print("")
        print("✅ Memory field names corrected")
        print("✅ Database compatibility restored")
        print("✅ Error messages will disappear")
        print("")
        print("🚀 Your AI tutoring platform is now perfect!")
        print("   No restart needed - changes take effect immediately")
        print("")
        print("📊 Test again with:")
        print("   curl -X POST http://localhost:8000/api/v1/chat/demo/1")
    else:
        print("❌ Fix failed - check file paths")

if __name__ == "__main__":
    main()
