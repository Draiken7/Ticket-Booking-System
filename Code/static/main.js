// id: 2
// str = "http://127.0.0..1:5000/show/" + this.id
// fetch(`http://127.0.0..1:5000/show/${this.id}`,
//     method:'delete',
//     headers:{
//         'Authorization':"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5MTI0MDY5MSwianRpIjoiZTAxYWI1NzEtNzRiNy00YmEwLWE2YzgtNWZiOWFmMmVlMTMyIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFkbWluMSIsIm5iZiI6MTY5MTI0MDY5MSwiZXhwIjoxNjkxNDEzNDkxfQ.szVCEkKzwYzdJ8O82adYervCL4JHTVPpFkzoah3QavM"
//     }    
// )
import router from './router.js'
import store from './store.js'

new Vue({
    el: '#app',
    store,
    template:`
    <div>
        <div class="d-flex justify-content-between container my-2">
            <div v-if="this.homeactive">
            <router-link to="/">
            <button class="btn btn-outline-warning" title="Home">
                <i class="bi bi-house fs-1"></i>
            </button></router-link>
            </div>
            <div class="mx-right" v-if="this.logoutactive">
            <button class="btn btn-outline-danger" @click="doLogout" title="Logout">
                <i class="bi bi-x-square fs-1"></i>
            </button>
            </div>
        </div>
        <router-view></router-view>
    </div>
    `,
    router,
    data:{
        logoutactive: false,
        homeactive: false
    },
    methods:{
        doLogout: function(){
            localStorage.removeItem('auth-token')
            localStorage.removeItem('role')
            this.logoutactive = false
            this.homeactive = false
            window.location='/'
        }
    },
    beforeMount: function(){
        if (localStorage.getItem('auth-token')){
            this.logoutactive = true,
            this.homeactive = true
        }
    },
    mounted:function(){
        console.log("mounted")

    },
    beforeUpdate(){
        if (localStorage.getItem('auth-token')){
            this.logoutactive = true,
            this.homeactive = true
        }
    }
})