// See also about the way to load the AmazonCognitoIdentity module.
// https://github.com/aws-amplify/amplify-js/tree/master/packages/amazon-cognito-identity-js#usage
// import { CognitoUserPool, CognitoUserAttribute, CognitoUser } from 'amazon-cognito-identity-js';
// require('amazon-cognito-js');

const AmazonCognitoIdentity = require('amazon-cognito-identity-js');
const AWS = require('aws-sdk');
const apigClientFactory = require('aws-api-gateway-client').default;

// ------------------------------------------------------------
// Global variables
// ------------------------------------------------------------

export default {
  userLogin(cognitoConfig, userInfo){
    return new Promise((resolve, reject) => {
      const userPoolData = {
        UserPoolId: cognitoConfig.userPoolId,
        ClientId: cognitoConfig.appClientId,
      }
      const gCognitoUserPool = new AmazonCognitoIdentity.CognitoUserPool(userPoolData);
      const authenticationDetails = new AmazonCognitoIdentity.AuthenticationDetails(userInfo);
      const userData = {
        Username: userInfo.Username,
        Pool: gCognitoUserPool
      };
  
      const cognitoUser = new AmazonCognitoIdentity.CognitoUser(userData);
      cognitoUser.authenticateUser(authenticationDetails, {
        onSuccess: (result) => {
          cognitoUser.Session = result;
          alert("ログイン成功");
          resolve(cognitoUser);
        },
        onFailure: (err) => {
          alert("APIログインエラーが発生しました", err);
          reject();
        },
      });
    });
  },
  userSignUp(cognitoConfig, inputData){
    return new Promise((resolve, reject) => {
      const userPoolData = {
        UserPoolId: cognitoConfig.userPoolId,
        ClientId: cognitoConfig.appClientId,
      }
      const gCognitoUserPool = new AmazonCognitoIdentity.CognitoUserPool(userPoolData);
      const attributeList = [
          { key: 'email', name: 'email'},
          { key: 'nickname', name: 'nickname'},
          { key: 'lastName', name: 'custom:last_name'},
          { key: 'firstName', name: 'custom:first_name'},
          { key: 'firstNameKana', name: 'custom:first_name_kana'},
          { key: 'lastNameKana', name: 'custom:last_name_kana'}];
      const userAttributeList = attributeList.map(attribute => {
        return new AmazonCognitoIdentity.CognitoUserAttribute({
          Name: attribute.name,
          Value: inputData[attribute.key],
        });
      })
      console.log(userAttributeList);

      gCognitoUserPool.signUp(inputData.email, inputData.password, userAttributeList, null, function(err, result) {
        console.log("err: ", err);
        console.log("result: ", result);
        if(err){
          alert("sorry, your try to sign up has failed.");
          reject(err);
        }
        resolve(result.user);
      });
    });
  },
  userConfirm(cognitoConfig, verifyData){
    return new Promise((resolve, reject) => {
      const userPoolData = {
        UserPoolId: cognitoConfig.userPoolId,
        ClientId: cognitoConfig.appClientId,
      }
      const gCognitoUserPool = new AmazonCognitoIdentity.CognitoUserPool(userPoolData);
      const userData = {
        Username: verifyData.email,
        Pool: gCognitoUserPool
      };

      const cognitoUser = new AmazonCognitoIdentity.CognitoUser(userData);

      cognitoUser.confirmRegistration(verifyData.verificationCode, true, function(err, result) {
        if (err) {
          alert("sorry, verification has failed.");
          reject(err);
        }
        resolve(result);
      });
    });
  },
  getApiData(cognitoConfig, apiUrl, method, pathTemplate, pathParams, queryParams, body){
    const userPoolData = {
      UserPoolId: cognitoConfig.userPoolId,
      ClientId: cognitoConfig.appClientId,
    }
    const gCognitoUserPool = new AmazonCognitoIdentity.CognitoUserPool(userPoolData);
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
        const credentials = new AWS.CognitoIdentityCredentials(cognitoIdentityParams);
  
        // refresh AWS credentials
        new Promise((resolve, reject) => {
          credentials.refresh((err) => {
            if (err){
              console.log(err);
              return;
            }
            const apiConfig = {
              invokeUrl: apiUrl,
              region: cognitoConfig.region,
              accessKey: credentials.accessKeyId,
              secretKey: credentials.secretAccessKey,
              sessionToken: credentials.sessionToken,
            }
            const apiClient = apigClientFactory.newClient(apiConfig);
            const additionalParams = {
                headers: {},
                queryParams: queryParams
            }
            apiClient.invokeApi(pathParams, pathTemplate, method, additionalParams, body)
            .then(function(result){
                return resolve(result);
            }).catch( function(result){
                console.log(result);
                reject(result);
            });
          });
        }).then((result) => {
          return resolve(result);
        }).catch( function(result){
            console.log(result);
            reject(result);
        });
      });
    });
  },
  fetchRestAPI(cognitoConfig, cognitoUser, method, pathTemplate, pathParams, queryParams, body){
    const apiUrl = process.env.VUE_APP_TOITOY_API_URL;
    return this.getApiData(cognitoConfig, apiUrl, method, pathTemplate, pathParams, queryParams, body);
  }
}
