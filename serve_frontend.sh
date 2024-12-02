#!/bin/bash
cd frontend || { echo "Failed to navigate to frontend directory"; exit 1; }
npm run build || { echo "npm build failed"; exit 1; }
cd ../..
sudo cp -r fruit-ninja/frontend/build/* /var/www/react_app || { echo "Failed to copy build files"; exit 1; }
echo "Build and deployment completed successfully."
