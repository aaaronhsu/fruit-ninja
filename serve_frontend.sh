#!/bin/bash

# Navigate to the frontend directory
cd frontend || { echo "Failed to navigate to frontend directory"; exit 1; }

# Run the npm build command
npm run build || { echo "npm build failed"; exit 1; }

# Navigate back to the root directory
cd ../..

# Copy the build output to the target directory with sudo
sudo cp -r fruit-ninja/frontend/build/* /var/www/react_app || { echo "Failed to copy build files"; exit 1; }

echo "Build and deployment completed successfully."
