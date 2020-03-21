import Vue from "vue";
import VueRouter from "vue-router";
import userLoginPage from "../views/userLoginPage.vue";
import userSignUpPage from "../views/userSignUpPage.vue";
import userVerifyPage from "../views/userVerifyPage.vue";
import classroomCreatePage from "../views/classroomCreatePage.vue";
import questionTopPage from "../views/questionTopPage.vue";
import schoolApiClient from "@/api/common.js";
import topPage from "../views/topPage.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "topPage",
    component: topPage
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
    path: "/questionTop",
    name: "questionTopPage",
    component: questionTopPage,
  },
  {
    path: "/classroomCreate",
    name: "classroomCreatePage",
    component: classroomCreatePage
  }
];

const router = new VueRouter({
  routes
});

router.beforeEach((to, from, next) => {
  if (to.name === "userLoginPage") {
    if (schoolApiClient.isUserLogin()) {
      next('/');
    } else {
      next();
    }
  } else if (!schoolApiClient.isUserLogin()) {
    next('/userLogin');
  }else{
    next();
  }
});

export default router;
