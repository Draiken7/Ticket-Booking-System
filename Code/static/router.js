import rootv from "./root.js"
import login from "./components/login.js"
import signup from "./components/signup.js"
import admin from "./components/admin.js"
import theaters from "./components/theaters.js"
import movies from "./components/movies.js"
import show from "./components/show.js"
import user from "./components/user.js"
import usershow from "./components/usershow.js"
import book from "./components/book.js"
import bookings from "./components/bookings.js"

const routes = [
    {
        path:'/',
        name:'Root',
        component: rootv,
    },
    {
        path: '/signup',
        name: 'Signup',
        component: signup,
    },
    {
        path:'/login',
        name:'Login',
        component: login,
    },
    {
        path:'/admin',
        name:'AdminView',
        component: admin,
    },
    {
        path:'/theater',
        name:'Theaters',
        component: theaters,
    },
    {
        path:'/movies',
        name:'Movies',
        component: movies,
    },
    {
        path:'/showm',
        name:'Show',
        component: show,
    },
    {
        path:'/user',
        name:"User",
        component:user,
    },
    {
        path:'/show',
        name:"User Show",
        component:usershow,
    },
    {
        path:'/book',
        name:'User book',
        component: book
    },
    {
        path:'/bookings',
        name:'User Bookings',
        component: bookings
    },
]

const router = new VueRouter({
    routes:routes,
})

export default router