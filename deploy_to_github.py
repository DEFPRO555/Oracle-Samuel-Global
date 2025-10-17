#!/usr/bin/env python3
"""
Oracle Samuel - GitHub Deployment Script
© 2025 Dowek Analytics Ltd. All Rights Reserved.

This script helps deploy Oracle Samuel to GitHub Pages.
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        print(f"Error: {e.stderr}")
        return False

def main():
    """Main deployment function."""
    print("🚀 Oracle Samuel - GitHub Deployment Script")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("ORACLE_SAMUEL_GITHUB").exists():
        print("❌ ORACLE_SAMUEL_GITHUB folder not found!")
        print("Please run this script from the main project directory.")
        return False
    
    # Change to GitHub folder
    os.chdir("ORACLE_SAMUEL_GITHUB")
    print(f"📁 Changed to: {os.getcwd()}")
    
    # Check if git is initialized
    if not Path(".git").exists():
        print("🔧 Initializing Git repository...")
        if not run_command("git init", "Git initialization"):
            return False
    else:
        print("✅ Git repository already initialized")
    
    # Add all files
    if not run_command("git add .", "Adding files to Git"):
        return False
    
    # Check for changes
    result = subprocess.run("git diff --cached --name-only", shell=True, capture_output=True, text=True)
    if not result.stdout.strip():
        print("ℹ️  No changes to commit")
        return True
    
    # Commit changes
    commit_message = "Update Oracle Samuel for GitHub Pages deployment"
    if not run_command(f'git commit -m "{commit_message}"', "Committing changes"):
        return False
    
    # Check if remote exists
    result = subprocess.run("git remote -v", shell=True, capture_output=True, text=True)
    if "origin" not in result.stdout:
        print("\n🔗 Please add your GitHub repository remote:")
        print("Example: git remote add origin https://github.com/yourusername/oracle-samuel-universal.git")
        print("\nAfter adding the remote, run:")
        print("git push -u origin main")
        return True
    
    # Push to GitHub
    if not run_command("git push origin main", "Pushing to GitHub"):
        print("\n💡 If this is your first push, try:")
        print("git push -u origin main")
        return False
    
    print("\n🎉 Deployment completed successfully!")
    print("🌐 Your site will be available at:")
    print("https://yourusername.github.io/oracle-samuel-universal/")
    print("\n📋 Next steps:")
    print("1. Go to your GitHub repository")
    print("2. Navigate to Settings → Pages")
    print("3. Select 'Deploy from a branch' → 'main'")
    print("4. Wait 5-10 minutes for deployment to complete")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️  Deployment cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
