
const rootv ={
    template:`
        <div>

        </div>
    `,
    data: function(){
        return{
            logoutactive:false
        }
    },
    beforeMount: function(){
        // check if user is already logged in
        if(localStorage.getItem('auth-token')==null){
            this.$router.push('/login')
        }
        else{
            if(localStorage.getItem('role')=='admin'){
                // route to admin view
                this.$router.push('/admin')
            }

            if(localStorage.getItem('role')=='user'){
                // route to user view
                this.$router.push('/user')
            }
            this.logoutactive = true
        }
        // Check which view to render

    }
}

export default rootv