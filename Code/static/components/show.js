const show = {
    template:`
<div>
    <div class="container">
        <div>
            <router-link to='/theater'>
                <button class="btn btn-outline-info" title="back">
                    <i class="bi bi-skip-backward fs-1"></i>
                </button>
            </router-link>
        </div>
        <h3> Show Management</h3>

        <div class="mx-auto my-2">
            <button class="btn btn-outline-primary" @click="toggleadd">
                <i class="bi bi-plus-square fs-2"></i>
            </button>
        </div>
        <div v-if="this.add">
            <div v-if="this.movies">
                <div class="text-white">
                    <p v-if="this.message" class="text-danger">{{this.message}}</p>
                    <span>
                        <label class="text-dark">Select A movie [REQUIRED]</label>
                        <select class="form-select" placeholder="Select a Movie" v-model="form.movie">
                            <option :value=movie.id v-for="(movie, index) in this.movies">{{movie.name}}</option>
                        </select>
                    </span>

                    <div>
                        <label class="text-dark">Enter Title [REQUIRED]</label>
                        <input type="text" placeholder="Title" class="form-control" required v-model="form.title">
                    </div>
                    <div>
                        <label class="text-dark">Enter caption</label>
                        <input type="text" placeholder="Caption" class="form-control" v-model="form.caption">
                    </div>
                    <div>
                        <label for="s" class="text-dark">Start From: [REQUIRED]</label>

                        <input id="s" type="date" class="form-control" required v-model="form.starton">
                    </div>
                    <div>
                        <label for="e" class="text-dark">End on: [REQUIRED]</label>

                        <input id="e" type="date" class="form-control" required v-model="form.endon">
                    </div>
                    <div>
                        <label for="t" class="text-dark">Time Slot: [REQUIRED]</label>

                        <input id="t" type="time" class="form-control" required v-model="form.time">
                    </div>
                    <div>
                        <label for="p" class="text-dark">Ticket Price: [REQUIRED]</label>

                        <input id="p" type="number" placeholder="Price" class="form-control" required
                            v-model="form.price">
                    </div>
                    <div class="my-2">
                        <button :class=this.button @click="addshow">
                            <i class="bi bi-bookmark-plus fs-2"></i>
                        </button>
                    </div>
                </div>
            </div>
        </div>
        <div v-else>
            <div v-for="(show, index) in data">

                <div class="card">
                    <h3 class="card-title">{{show.title}}</h3>
                    <div class="card-boy">
                        <p>Movie ID: {{show.movieid}}</p>
                        <p>{{show.caption}}</p>
                        <p>Starts on: {{show.starton}}</p>
                        <p>Ends on: {{show.endon}}</p>
                        <p>Timing: {{show.time}}</p>
                    </div>
                    <div v-if="update">
                        <button class="btn btn-secondary" @click="toggleupdate">
                            <i class="bi bi-x fs-2"></i>
                        </button>
                        <div class="mb-3">
                            <p>Change Title</p>
                            <input type="text" v-bind:placeholder="show.title" class="form-control"
                                v-model="form.title">
                        </div>
                        <div class="mb-3">
                            <p>Change Caption</p>
                            <input type="text" v-bind:placeholder="show.caption" class="form-control"
                                v-model="form.caption">
                        </div>
                        <div class="mb-3">
                            <p>Change Price</p>
                            <input type="number" v-bind:placeholder="show.price" class="form-control"
                                v-model="form.price">
                        </div>
                        <div class="mb-3">
                            <button class="btn btn-outline-primary" @click="updater(show.id)" title="Click to Update">
                                <i class="bi bi-clipboard-plus fs-2"></i>
                            </button>
                        </div>
                    </div>
                    <div class="card-footer">
                        <button class="btn btn-outline-warning" @click="toggleupdate" title="Update">
                            <i class="bi bi-pencil-square fs-2"></i>
                        </button>
                        <div v-if="flag(show.id)">
                            <button class="btn btn-outline-danger" @click="Delete(show.id)">
                                <i class="bi bi-trash3 fs-2"></i>
                            </button>
                        </div>
                        <div v-else>
                            <p>Show currently running!!</p>
                            <button class="btn btn-outline-secondary" disabled>
                                <i class="bi bi-trash3 fs-2"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
    `,
    data(){
        return{
            data:null,
            movies:null,
            theaters:null,
            id:null,
            now: new Date(),
            add:false,
            update:false,
            addable:null,
            form:{
                id:null,
                movie:null,
                title:null,
                caption:null,
                starton:null,
                endon:null,
                time:null,
                price:null
            },
            message:null,
            error:null,
            button: "btn btn-outline-primary",
        }
    },
    methods:{
        flag(id){
            // Getting show id
            let s = this.data.find(i=>i.id==id)
            var x  = ((new Date(s.starton)) - this.now) 
            var y = ((this.now - new Date(s.endon)))
            y =  y/1000 
            x = x/1000

            // Check if shows starts atleast 5 days after today
            if((x > 0) && (x > 5*24*60*60)){
                return true
            }
            // Check if show has already ended
            else if((y > 0) && (y > 1*24*60*60)){
                return true
            }
            else{
                return false
            }
            return false
        },
        toggleadd(){
            this.add = (!this.add)
        },
        toggleupdate(){
            this.update = (!this.update)
        },
        async addshow(){
            console.log("here")
            this.button = "btn btn-warning"
            this.message=null
            this.error = false
            this.form.id = this.id
            if ((!this.form.movie)||(!this.form.title)||(!this.form.starton)||(!this.form.endon)||(!this.form.time)||(!this.form.price)){
                this.message = "required fields CANNOT be empty!"
                this.error = true
            }

                if(!this.error){
                    const res = await fetch('http://127.0.0.1:5000/show', {
                        method:"POST",
                        headers:{
                            'Content-Type':'application/json',
                            'Authorization':'Bearer '+localStorage.getItem('auth-token')
                        },
                        body:JSON.stringify(this.form)
                    })
                    const dat = await res.json()
                    if(res.status==200){
                            this.data.push({
                            "id":this.id,
                            "movieid":this.form.movie,
                            "title":this.form.title,
                            "starton":this.form.starton,
                            "endon":this.form.endon,
                            "time":this.form.time,
                            "price":this.form.price   
                            })
                    }
                    else{
                        this.message = dat
                    }               
                        
            }
            this.form.id = null
            this.form.movie = null
            this.form.title = null
            this.form.starton = null
            this.form.endon = null
            this.form.time = null
            this.form.price = null
            this.button ="btn btn-primary" 
            this.error = false 
        },
        async updater(id) {
            var a = this.data.find(x => (x.id == id))
            if (!this.form.title) {
                this.form.title = a.title
            }
            if (!this.form.caption) {
                this.form.caption = a.caption
            }
            if (!this.form.price) {
                this.form.price = a.price
            }
            this.form.starton=''
            this.form.endon=''
            this.form.time=''
            var y = this.form
            y.id = id
            const res = await fetch('http://127.0.0.1:5000/show/' + id, {
                method: "PUT",
                body: JSON.stringify(y),
                headers: {
                    'Content-Type': 'application/json',
                    "Authorization": "Bearer " + localStorage.getItem('auth-token')
                }
            })
            const data = await res.json()
            if (res.status == 200) {
                this.data = this.data.map(x => {
                    if(x.id==id){
                        x = this.form
                        x.id = id
                    }
                    return x
                })
            }
        },
        Delete(id){
            let s = this.data.find(i=>i.id==id)
            var x  = ((new Date(s.starton)) - this.now) 
            var y = ((this.now - new Date(s.endon)))
            y =  y/1000 
            x = x/1000

            if((x > 0) && (x > 5*24*60*60)){
                const p = fetch(`http://127.0.0.1:5000/show/${s.id}`, {
                    method:"DELETE",
                    headers:{
                        'Authorization':`Bearer ${localStorage.getItem('auth-token')}`
                    }
                })
                this.data = this.data.filter(i=>i.id!=id)
            }
            else if((y > 0) && (y > 1*24*60*60)){
                const p = fetch(`http://127.0.0.1:5000/show/${s.id}`,{
                    method:"PATCH",
                    headers:{
                        'Authorization':`Bearer ${localStorage.getItem('auth-token')}`
                    }
                })
                this.data = this.data.filter(i=>i.id!=id)
            }
        }
    },
    async beforeMount(){
        this.id = this.$store.getters.getTID
        const a = await fetch('http://127.0.0.1:5000/movie', {
            methods:'GET',
            headers:{
                'Authorization':'Bearer '+localStorage.getItem('auth-token')
            }
        })
        this.movies = await a.json()
        // console.log(this.movies)
        const b = await fetch('http://127.0.0.1:5000/theater', {
            methods:'GET',
            headers:{
                'Authorization':'Bearer '+localStorage.getItem('auth-token')
            }
        })
        this.theaters = await b.json()
        this.theaters.forEach(element => {
            if (element.id == this.id){
                this.data = element.shows
                return
            }
        })

    }

}
export default show