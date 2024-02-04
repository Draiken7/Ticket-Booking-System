
const login ={
    template: `
        <div class="container">
    <div class="d-flex justify-content-center align-items-center" style="min-height:100vh">
            <div class="row">
                <div class="col-md">
                    <div id="left" class="card bg-dark text-white ">
                        <img src="https://wallpaperaccess.com/full/238215.jpg" class="card-img" alt="...">
                        <div class="card-img-overlay">
                          <h5 class="card-title mx-auto">Hello fellow Movie Nerd!</h5>
                          <p class="card-text mx-auto">login or Signup to Access the Site!</p>
                        </div>
                    </div>
                </div>
                <div class="col-md mt-3 mt-md-0 text-center">
                    <div id="right" class="card bg-dark text-dark">
                    <img src="https://wallpaperaccess.com/full/646166.jpg" class="card-img" alt="...">
                    <div class="card-img-overlay">
                    <div class="card-title">
                        <h3 class="mx-auto p-2">Login</h3>
                    </div>
                    <div>
                    <div>
                    <p class="text-danger" v-show="this.message">{{this.message}}</p>
                    </div>
    <div class="form-floating mb-3 p-2 text-dark">
        <input type="email" class="form-control" id="floatingInput" placeholder="Username" v-model="creds.username">
        <label for="floatingInput">Username</label>
    </div>
    <div class="form-floating p-2 text-dark">
        <!--<p class="text-danger" v-if="this.message_p">{{this.message_p}}</p>-->
        <input type="password" class="form-control" id="floatingPassword" placeholder="Password" v-model="creds.password">
        <label for="floatingPassword">Password</label>
    </div>
    <div>
        <button class="btn btn-outline-primary p-2" @click="doLogin">
            <i class="bi bi-door-open fs-1"></i>
        </button>
    </div>
    <div class="card-footer p-2">
         or <router-link to="/signup"><h6>Signup!</h6></router-link>
    </div>
</div>
</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
        `,
    data: function(){
        return{
            creds:{
                username:null,
                password:null,
            },
            message:null
        }
    },
    methods:{
        doLogin: function(){
            this.message = null
            if (!this.creds.username){
                this.message = "Username cannot be empty!"
            }
            else if (!this.creds.password){
                this.message = "Password cannot be empty!"
            }
            else{
                fetch('http://127.0.0.1:5000/login_user', {
                    method:"POST",
                    headers:{
                    'Content-Type':'application/json'
                    },
                    body: JSON.stringify(this.creds)
                }).then((res)=>{
                        return res.json()
                }).then((data)=>{
                    try{
                        localStorage.setItem('auth-token', data.user.token)
                        localStorage.setItem('role', data.user.role)
                        if (data.user.role=='admin'){
                            console.log("redirect to admin view")
                            this.$router.push('/admin')
                            
                        }
                        else{
                            console.log("redirect to user view")
                            this.$router.push('/user')
                        }
                    }
                    catch{
                        this.message = data.error
                    }
                })
            }
            this.creds.username = null
            this.creds.password = null

        }        
    }
}

export default login