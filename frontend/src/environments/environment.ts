/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'coffee-shop-fsnd-siphiwemanda.eu', // the auth0 domain prefix
    audience: 'coffee', // the audience set for the auth0 app
    clientId: 'GXLsZhRZiO8KkrXtL2apZ9i0Vyqjpig9', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:4200/tabs/drink-menu', // the base url of the running ionic application.
  }
};
