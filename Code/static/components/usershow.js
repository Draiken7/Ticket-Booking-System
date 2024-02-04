const usershow = {
    template:`
    <div>
        <div class="container">
            <div>
                <router-link to='/user'>
                    <button class="btn btn-outline-info" title="back">
                        <i class="bi bi-skip-backward fs-1"></i>
                    </button>
                </router-link>
            </div>
            <div class="row">
                <div v-if="this.data!=null && this.data[0].shows.length > 0">
                    <div v-for="(show, index) in this.data[0].shows" class="col-md-4">
                        <div class="card">
                            <div class="card-title">
                                <h4>{{show.name}}</h4>
                            </div>
                            <div class="card-body">
                                <p><strong>Theater Location: </strong>{{show.location}}</p>
                                <p><strong>Staring on: </strong>{{show.starton}}</p>
                                <p><strong>Timing: </strong>{{show.time}}</p>
                            </div>
                            <div class="card-footer">
                                <a class="stretched-link" @click="book(show.id)"></a>
                            </div>
                        </div>  
                    </div>  
                </div> 
                <div v-else>
                    No Shows Running!
                </div>           
            </div>
        </div>
    </div>
    `,
    data(){
        return {
            mid:null,
            queryparam:null,
            data:null,
        }
    },
    methods:{
        book(id){
            this.$store.commit("setSID", id)
            this.$router.push('/book')            
        }
    },
    async beforeMount(){
        console.log("Here in Before Mount")
        this.mid = this.$store.getters.getMID
        this.querparam = this.$store.getters.getQueryParam
        const res = await fetch(`http://127.0.0.1:5000/shows?name=${this.$store.getters.getQueryParam}&value=${this.mid}`, {
            method:'GET',
            headers:{
                'Authorization':`Bearer ${localStorage.getItem('auth-token')}`
            }
        })
        this.data = await res.json()
    }
}

export default usershow