// See also about the way to load the AmazonCognitoIdentity module.
// https://github.com/aws-amplify/amplify-js/tree/master/packages/amazon-cognito-identity-js#usage
// import { CognitoUserPool, CognitoUserAttribute, CognitoUser } from 'amazon-cognito-identity-js';
// require('amazon-cognito-js');
import { Auth, Storage } from "aws-amplify";

const AmazonCognitoIdentity = require("amazon-cognito-identity-js");
const AWS = require("aws-sdk");
const apigClientFactory = require("aws-api-gateway-client").default;
var cognitoConfig = {
  region: process.env.VUE_APP_REGION,
  userPoolId: process.env.VUE_APP_COGNITO_USER_POOL_ID,
  appClientId: process.env.VUE_APP_COGNITO_APP_CLIENT_ID,
  identifyPoolId: process.env.VUE_APP_IDENTITY_POOL_ID,
  loginsKey: process.env.VUE_APP_LOGINS_KEY
};

export default {
  userLogin(username, password) {
    return new Promise((resolve, reject) => {
      Auth.signIn(username, password)
        .then(data => {
          console.log(data);
          resolve(data);
        })
        .catch(err => {
          reject(err);
        });
    });
  },
  isUserLogin() {
    const userPoolData = {
      UserPoolId: cognitoConfig.userPoolId,
      ClientId: cognitoConfig.appClientId
    };
    const gCognitoUserPool = new AmazonCognitoIdentity.CognitoUserPool(
      userPoolData
    );
    const cognitoUser = gCognitoUserPool.getCurrentUser();
    if (cognitoUser == null) {
      return false;
    }
    return true;
  },
  userSignUp(inputData) {
    return new Promise((resolve, reject) => {
      const userPoolData = {
        UserPoolId: cognitoConfig.userPoolId,
        ClientId: cognitoConfig.appClientId
      };
      const gCognitoUserPool = new AmazonCognitoIdentity.CognitoUserPool(
        userPoolData
      );
      const attributeList = [
        { key: "email", name: "email" },
        { key: "nickname", name: "nickname" },
        { key: "lastName", name: "custom:last_name" },
        { key: "firstName", name: "custom:first_name" },
        { key: "firstNameKana", name: "custom:first_name_kana" },
        { key: "lastNameKana", name: "custom:last_name_kana" }
      ];
      const userAttributeList = attributeList.map(attribute => {
        return new AmazonCognitoIdentity.CognitoUserAttribute({
          Name: attribute.name,
          Value: inputData[attribute.key]
        });
      });
      console.log(userAttributeList);

      gCognitoUserPool.signUp(
        inputData.email,
        inputData.password,
        userAttributeList,
        null,
        function(err, result) {
          if (err) {
            reject(err);
          }
          resolve(result.user);
        }
      );
    });
  },
  userVerify(verifyData) {
    return new Promise((resolve, reject) => {
      const userPoolData = {
        UserPoolId: cognitoConfig.userPoolId,
        ClientId: cognitoConfig.appClientId
      };
      const gCognitoUserPool = new AmazonCognitoIdentity.CognitoUserPool(
        userPoolData
      );
      const userData = {
        Username: verifyData.email,
        Pool: gCognitoUserPool
      };

      const cognitoUser = new AmazonCognitoIdentity.CognitoUser(userData);

      cognitoUser.confirmRegistration(
        verifyData.verificationCode,
        true,
        function(err, result) {
          if (err) {
            reject(err);
          }
          resolve(result);
        }
      );
    });
  },
  getApiData(apiUrl, method, pathTemplate, pathParams, queryParams, body) {
    const userPoolData = {
      UserPoolId: cognitoConfig.userPoolId,
      ClientId: cognitoConfig.appClientId
    };
    const gCognitoUserPool = new AmazonCognitoIdentity.CognitoUserPool(
      userPoolData
    );
    const cognitoUser = gCognitoUserPool.getCurrentUser();
    return new Promise((resolve, reject) => {
      cognitoUser.getSession((err, session) => {
        if (err) {
          console.log("getSession: err: " + JSON.stringify(err));
          return;
        }
        const cognitoIdentityParams = {
          IdentityPoolId: cognitoConfig.identifyPoolId,
          Logins: {
            [cognitoConfig.loginsKey]: session.getIdToken().getJwtToken()
          }
        };

        AWS.config.region = cognitoConfig.region;
        const credentials = new AWS.CognitoIdentityCredentials(
          cognitoIdentityParams
        );

        // refresh AWS credentials
        new Promise((resolve, reject) => {
          credentials.refresh(err => {
            if (err) {
              console.log(err);
              return;
            }
            const apiConfig = {
              invokeUrl: apiUrl,
              region: cognitoConfig.region,
              accessKey: credentials.accessKeyId,
              secretKey: credentials.secretAccessKey,
              sessionToken: credentials.sessionToken
            };
            const apiClient = apigClientFactory.newClient(apiConfig);
            const additionalParams = {
              headers: {},
              queryParams: queryParams
            };
            apiClient
              .invokeApi(
                pathParams,
                pathTemplate,
                method,
                additionalParams,
                body
              )
              .then(function(result) {
                return resolve(result);
              })
              .catch(function(result) {
                console.log(result);
                reject(result);
              });
          });
        })
          .then(result => {
            return resolve(result);
          })
          .catch(function(result) {
            console.log(result);
            reject(result);
          });
      });
    });
  },
  fetchRestAPI(
    cognitoUser,
    method,
    pathTemplate,
    pathParams,
    queryParams,
    body
  ) {
    const apiUrl = process.env.VUE_APP_TOITOY_API_URL;
    return this.getApiData(
      apiUrl,
      method,
      pathTemplate,
      pathParams,
      queryParams,
      body
    );
  },
  getS3PublicFile(filePath) {
    return new Promise((resolve, reject) => {
      Storage.configure({ level: "public" });
      Storage.get(filePath, { expires: 3600 })
        .then(result => {
          resolve(result);
        })
        .catch(err => {
          reject(err);
        });
    });
  },
  putS3PublicFile(file) {
    return new Promise((resolve, reject) => {
      const dt = new Date();
      const filePath = dt.getTime() + "-" + file.name;
      Storage.configure({ level: "public" });
      Storage.put("" + filePath, file)
        .then(result => {
          resolve(result);
        })
        .catch(err => {
          reject(err);
        });
    });
  }
};
