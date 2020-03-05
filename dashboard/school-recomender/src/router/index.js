import Vue from "vue";
import VueRouter from "vue-router";
import userLoginPage from "../views/userLoginPage.vue";
import userSignUpPage from "../views/userSignUpPage.vue";
import userVerifyPage from "../views/userVerifyPage.vue";
import classroomCreatePage from "../views/classroomCreatePage.vue";
import topPage from "../views/topPage.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "topPage",
    component: topPage
  },
  {
    path: "/about",
    name: "About",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/About.vue")
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
    path: "/classroomCreate",
    name: "classroomCreatePage",
    component: classroomCreatePage
  }
];

const router = new VueRouter({
  routes
});

export default router;
