import Vue from "vue";
import VueRouter from "vue-router";
import userLoginPage from "../views/userLoginPage.vue";
import userSignUpPage from "../views/userSignUpPage.vue";
import userLogoutPage from "../views/userLogoutPage.vue";
import userVerifyPage from "../views/userVerifyPage.vue";
import invitePage from "../views/invitePage.vue";
import classroomCreatePage from "../views/classroomCreatePage.vue";
import questionTopPage from "../views/questionTopPage.vue";
import topPage from "../views/topPage.vue";
import classroomWorkDetailPage from "../views/classroomWorkDetailPage.vue";

import {
  Auth
} from "aws-amplify";

Vue.use(VueRouter);

const routes = [{
    path: "/",
    name: "topPage",
    component: topPage
  },
  {
    path: "/userLogout",
    name: "userLogoutPage",
    component: userLogoutPage
  },
  {
    path: "/userLogin",
    name: "userLoginPage",
    component: userLoginPage
  },
  {
    path: "/userSignUp",
    name: "userSignUpPage",
    component: userSignUpPage
  },
  {
    path: "/userVerify",
    name: "userVerifyPage",
    component: userVerifyPage
  },
  {
    path: "/invite",
    name: "invitePage",
    component: invitePage
  },
  {
    path: "/questionTop",
    name: "questionTopPage",
    component: questionTopPage,
  },
  {
    path: "/classroomCreate",
    name: "classroomCreatePage",
    component: classroomCreatePage
  },
  {
    path: "/classroomWorkDetail",
    name: "classroomWorkDetailPage",
    component: classroomWorkDetailPage
  },

];

const router = new VueRouter({
  routes
});

router.beforeEach(async (to, from, next) => {
  const isLogin = await Auth.currentAuthenticatedUser()
    .then(data => {
      return true;
    })
    .catch(err => {
      return false;
    });
  if (to.name === "userSignUpPage" || to.name === "userVerifyPage" || to.name === "invitePage") {
    next();
    return
  }
  if (to.name === "userLoginPage") {
    if (isLogin) {
      next('/');
      return
    }
    next();
    return
  }
  if (!isLogin) {
    next('/userLogin');
    return
  }
  next();
});

export default router;
