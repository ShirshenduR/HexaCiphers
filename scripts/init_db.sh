#!/bin/bash
# Database initialization script for HexaCiphers

set -e

echo "🚀 Initializing HexaCiphers Database..."

# Wait for PostgreSQL to be ready
until pg_isready -h ${POSTGRES_HOST:-localhost} -p ${POSTGRES_PORT:-5432} -U ${POSTGRES_USER:-hexaciphers_user}
do
  echo "⏳ Waiting for PostgreSQL to be ready..."
  sleep 2
done

echo "✅ PostgreSQL is ready!"

# Initialize Flask database
export FLASK_APP=backend.app
echo "📊 Creating database tables..."
flask db init || echo "Database already initialized"
flask db migrate -m "Initial migration" || echo "Migration already exists"
flask db upgrade

echo "🎉 Database initialization complete!"

# Create initial data (optional)
python -c "
from backend.app import create_app
from backend.db.models import db, User, Post, Campaign
from datetime import datetime

app = create_app()
with app.app_context():
    # Create sample admin user if none exists
    if User.query.count() == 0:
        print('📝 Creating sample data...')
        
        # Sample users
        admin_user = User(
            user_id='admin_001',
            username='admin',
            followers=1000,
            is_bot=False
        )
        
        sample_user = User(
            user_id='user_001',
            username='sample_user',
            followers=500,
            is_bot=False
        )
        
        db.session.add(admin_user)
        db.session.add(sample_user)
        db.session.commit()
        
        print('✅ Sample data created!')
    else:
        print('📊 Database already contains data')
"

echo "🚀 HexaCiphers is ready to launch!"
