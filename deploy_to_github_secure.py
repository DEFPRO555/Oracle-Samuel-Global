# © 2025 Dowek Analytics Ltd.
# Secure GitHub Deployment Script
# Uses GitHub API to deploy Oracle Samuel

import os
import sys
import json
import base64
from datetime import datetime
from github_config import GitHubConfig

class OracleSamuelDeployer:
    """Secure deployment manager for Oracle Samuel"""
    
    def __init__(self):
        self.github = GitHubConfig()
        self.repo_name = "oracle-samuel"
        self.deployment_files = [
            "app.py",
            "requirements.txt",
            "README.md",
            "assets/luxury_theme.css",
            "assets/premium_enhanced.css"
        ]
    
    def create_deployment_repository(self) -> bool:
        """Create deployment repository"""
        try:
            print(f"🚀 Creating repository: {self.repo_name}")
            
            # Check if repo exists
            repo_info = self.github.get_repository_info(self.repo_name)
            if repo_info:
                print(f"✅ Repository {self.repo_name} already exists")
                return True
            
            # Create new repository
            success = self.github.create_repository(
                repo_name=self.repo_name,
                description="Oracle Samuel - Real Estate Market Prophet | AI-Powered Property Analysis",
                private=False
            )
            
            if success:
                print(f"✅ Repository {self.repo_name} created successfully")
                return True
            else:
                print(f"❌ Failed to create repository {self.repo_name}")
                return False
                
        except Exception as e:
            print(f"❌ Error creating repository: {e}")
            return False
    
    def deploy_files(self) -> bool:
        """Deploy application files to GitHub"""
        try:
            print("📦 Deploying files to GitHub...")
            
            deployed_count = 0
            for file_path in self.deployment_files:
                if os.path.exists(file_path):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # Create commit message
                        commit_message = f"Deploy {file_path} - Oracle Samuel v{datetime.now().strftime('%Y.%m.%d')}"
                        
                        # Upload file
                        success = self.github.upload_file(
                            repo_name=self.repo_name,
                            file_path=file_path,
                            content=content,
                            commit_message=commit_message
                        )
                        
                        if success:
                            print(f"✅ Deployed: {file_path}")
                            deployed_count += 1
                        else:
                            print(f"❌ Failed to deploy: {file_path}")
                            
                    except Exception as e:
                        print(f"❌ Error deploying {file_path}: {e}")
                else:
                    print(f"⚠️  File not found: {file_path}")
            
            print(f"\n📊 Deployment Summary:")
            print(f"✅ Successfully deployed: {deployed_count}/{len(self.deployment_files)} files")
            
            return deployed_count > 0
            
        except Exception as e:
            print(f"❌ Error during deployment: {e}")
            return False
    
    def create_github_pages_config(self) -> bool:
        """Create GitHub Pages configuration"""
        try:
            print("🌐 Setting up GitHub Pages configuration...")
            
            # Create index.html for GitHub Pages
            index_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Oracle Samuel - Real Estate Prophet</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container {
            text-align: center;
            color: white;
            max-width: 600px;
            padding: 2rem;
        }
        h1 {
            font-size: 3rem;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        p {
            font-size: 1.2rem;
            margin-bottom: 2rem;
            opacity: 0.9;
        }
        .btn {
            display: inline-block;
            padding: 1rem 2rem;
            background: rgba(255,255,255,0.2);
            color: white;
            text-decoration: none;
            border-radius: 50px;
            border: 2px solid rgba(255,255,255,0.3);
            transition: all 0.3s ease;
            font-size: 1.1rem;
            margin: 0.5rem;
        }
        .btn:hover {
            background: rgba(255,255,255,0.3);
            transform: translateY(-2px);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏠 Oracle Samuel</h1>
        <p>The Real Estate Market Prophet</p>
        <p>AI-Powered Property Analysis & Market Prediction</p>
        <a href="https://github.com/your-username/oracle-samuel" class="btn">View on GitHub</a>
        <a href="https://your-streamlit-app.herokuapp.com" class="btn">Launch App</a>
    </div>
</body>
</html>
            """
            
            # Upload index.html
            success = self.github.upload_file(
                repo_name=self.repo_name,
                file_path="index.html",
                content=index_html,
                commit_message="Add GitHub Pages landing page"
            )
            
            if success:
                print("✅ GitHub Pages configuration created")
                return True
            else:
                print("❌ Failed to create GitHub Pages configuration")
                return False
                
        except Exception as e:
            print(f"❌ Error creating GitHub Pages config: {e}")
            return False
    
    def deploy(self) -> bool:
        """Main deployment process"""
        try:
            print("🚀 Starting Oracle Samuel GitHub Deployment...")
            print("=" * 50)
            
            # Test GitHub connection
            if not self.github.test_connection():
                print("❌ GitHub API connection failed")
                return False
            
            # Create repository
            if not self.create_deployment_repository():
                return False
            
            # Deploy files
            if not self.deploy_files():
                return False
            
            # Setup GitHub Pages
            if not self.create_github_pages_config():
                return False
            
            print("\n" + "=" * 50)
            print("🎉 Oracle Samuel deployment completed successfully!")
            print(f"📱 Repository: https://github.com/{self.github.get_user_info()['login']}/{self.repo_name}")
            print("🌐 GitHub Pages will be available after a few minutes")
            
            return True
            
        except Exception as e:
            print(f"❌ Deployment failed: {e}")
            return False

def main():
    """Main deployment function"""
    deployer = OracleSamuelDeployer()
    success = deployer.deploy()
    
    if success:
        print("\n✅ Deployment completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Deployment failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
