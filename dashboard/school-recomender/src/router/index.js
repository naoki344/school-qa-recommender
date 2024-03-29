import Vue from "vue";
import VueRouter from "vue-router";
import userLoginPage from "../views/userLoginPage.vue";
import userSignUpPage from "../views/userSignUpPage.vue";
import userLogoutPage from "../views/userLogoutPage.vue";
import userVerifyPage from "../views/userVerifyPage.vue";
import passwordForgotPage from "../views/passwordForgotPage.vue";
import passwordResetPage from "../views/passwordResetPage.vue";
import invitePage from "../views/invitePage.vue";
import questionTopPage from "../views/questionTopPage.vue";
import topPage from "../views/topPage.vue";
import classroomWorkDetailPage from "../views/classroomWorkDetailPage.vue";

import { Auth } from "aws-amplify";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "topPage",
    component: topPage,
  },
  {
    path: "/userLogout",
    name: "userLogoutPage",
    component: userLogoutPage,
  },
  {
    path: "/userLogin",
    name: "userLoginPage",
    component: userLoginPage,
  },
  {
    path: "/userSignUp",
    name: "userSignUpPage",
    component: userSignUpPage,
  },
  {
    path: "/userVerify",
    name: "userVerifyPage",
    component: userVerifyPage,
  },
  {
    path: "/invite",
    name: "invitePage",
    component: invitePage,
  },
  {
    path: "/questionTop",
    name: "questionTopPage",
    component: questionTopPage,
  },
  {
    path: "/classroomWorkDetail",
    name: "classroomWorkDetailPage",
    component: classroomWorkDetailPage,
  },
  {
    path: "/passwordForgot",
    name: "passwordForgotPage",
    component: passwordForgotPage,
  },
  {
    path: "/passwordReset",
    name: "passwordResetPage",
    component: passwordResetPage,
  },
];

const router = new VueRouter({
  routes,
});

router.beforeEach(async (to, from, next) => {
  const isLogin = await Auth.currentAuthenticatedUser()
    .then((data) => {
      return true;
    })
    .catch((err) => {
      return false;
    });
  if (
    to.name === "userSignUpPage" ||
    to.name === "userVerifyPage" ||
    to.name === "invitePage" ||
    to.name === "passwordForgotPage" ||
    to.name === "passwordResetPage"
  ) {
    next();
    return;
  }
  if (to.name === "userLoginPage") {
    if (isLogin) {
      next("/");
      return;
    }
    next();
    return;
  }
  if (!isLogin) {
    next("/userLogin");
    return;
  }
  next();
});

export default router;
