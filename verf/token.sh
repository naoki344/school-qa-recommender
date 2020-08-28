#!/bin/sh
 
USER_POOL_ID="ap-northeast-1_tdnDpRB4D"
CLIENT_ID="sv3598bih0npekpghpapd1l6p"
USER_NAME="trombone344@gmail.com"
PASSWORD="q?J5kF"
new_PASSWORD="@Naoki007744"
 
# aws cognito-idp sign-up \
#   --client-id ${CLIENT_ID} \
#   --username ${USER_NAME} \
#   --password ${PASSWORD} \
#   --user-attribute "Name=email,Value=${USER_NAME}"

# CONFIRMATION_CODE="313105"
# aws cognito-idp confirm-sign-up \
#   --client-id ${CLIENT_ID} \
#   --username ${USER_NAME} \
#   --confirmation-code ${CONFIRMATION_CODE}

# aws cognito-idp admin-initiate-auth \
#   --user-pool-id ${USER_POOL_ID} \
#   --client-id ${CLIENT_ID} \
#   --auth-flow ADMIN_NO_SRP_AUTH \
#   --auth-parameters "USERNAME=${USER_NAME},PASSWORD=${PASSWORD}"
ID_TOKEN=$(aws cognito-idp admin-initiate-auth \
  --user-pool-id ${USER_POOL_ID} \
  --client-id ${CLIENT_ID} \
  --auth-flow ADMIN_NO_SRP_AUTH \
  --auth-parameters "USERNAME=${USER_NAME},PASSWORD=${PASSWORD}" \
  --query "AuthenticationResult.IdToken" | sed "s/\"//g") && echo ${ID_TOKEN}
