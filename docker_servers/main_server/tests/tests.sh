#!/bin/bash

MAIN_SERVER_URL="http://localhost:8002"

# Test User Data
USER_NAME="TestUser"
USER_EMAIL="testuser@example.com"
USER_LOGIN="testlogin"
USER_PASSWORD="testpassword"

# Test Matrix File
MATRIX_FILE_PATH="./mongo_app/tests/Matrix_JGL009.mtx"
MATRIX_FILE_NAME="Matrix_JGL009.mtx"

# cd ../../ 
# docker-compose up -u
# sleep 3

echo "Running tests for Main Server..."

# Function to print test result
print_result() {
    if [ $1 -eq 0 ]; then
        echo "✅ $2 passed"
    else
        echo "❌ $2 failed"
    fi
}

# 1. Test user registration
echo ""
echo ""
echo "1. Testing user registration..."
curl -s -X POST "$MAIN_SERVER_URL/register" \
    -H "Content-Type: application/json" \
    -d '{
        "name": "'"$USER_NAME"'",
        "email": "'"$USER_EMAIL"'",
        "login": "'"$USER_LOGIN"'",
        "password": "'"$USER_PASSWORD"'"
    }' 
#print_result $? "User registration"

# 2. Test user login
echo ""
echo ""
echo "2. Testing user login..."
curl -s -X POST "$MAIN_SERVER_URL/login" \
    -H "Content-Type: application/json" \
    -d '{
        "login": "'"$USER_LOGIN"'",
        "password": "'"$USER_PASSWORD"'"
    }' 
#print_result $? "User login"

# # 3. Test uploading matrix
# echo ""
# echo ""
# echo "3. Testing matrix upload..."
# curl -s -X POST "$MAIN_SERVER_URL/save_matrix" \
#     -F "login=$USER_LOGIN" \
#     -F "matrix_file=@$MATRIX_FILE_PATH" > /dev/null
# #print_result $? "Matrix upload"

# # 4. Test retrieving list of matrices for user
# echo ""
# echo ""
# echo "4. Testing retrieval of matrix list for user..."
# curl -s -X POST "$MAIN_SERVER_URL/get_matrix_names_by_user_login" \
#     -F "login=$USER_LOGIN" 
#     #| grep -q "$MATRIX_FILE_NAME"
# #print_result $? "Retrieve matrix list"

# # 5. Test retrieving matrix data by filename
# echo ""
# echo ""
# echo "5. Testing retrieval of matrix data by filename..."
# curl -s "$MAIN_SERVER_URL/get_matrix_by_filename/$MATRIX_FILE_NAME" 
#     #| grep -q "%%MatrixMarket"
# #print_result $? "Retrieve matrix data by filename"

# 6. Test system status
echo ""
echo ""
echo "6. Testing main server status check..."
curl -s "$MAIN_SERVER_URL/status"
#print_result $? "Main server status check"

echo ""
echo ""
echo "All tests completed."

# Остановить все контейнеры
# docker-compose down

# # Удалить все контейнеры, созданные docker-compose
# docker-compose down --rmi all -v

# # Альтернативный способ удаления контейнеров и образов вручную:
# # Удалить все контейнеры, связанные с проектом
# docker container prune -f

# # Удалить все образы, связанные с проектом
# docker image prune -a -f