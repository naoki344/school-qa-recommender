import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";
import userLoginPage from "../views/userLoginPage.vue";
import userSignUpPage from "../views/userSignUpPage.vue";
import userConfirmPage from "../views/userConfirmPage.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home
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
    path: "/userConfirm",
    name: "userConfirmPage",
    component: userConfirmPage
  }
];

const router = new VueRouter({
  routes
});

export default router;
