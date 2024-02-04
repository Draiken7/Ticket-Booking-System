const theaters = {
    template:`
<div>
    <div class="container">
        <div class="row bg-transparent text-white">
            <div>
                <router-link to='/admin'>
                    <button class="btn btn-outline-info" title="back">
                        <i class="bi bi-skip-backward fs-1"></i>
                    </button>
                </router-link>
            </div>
            <div class="header text-center text-dark">
                <h2>THEATER MANAGEMENT (AND SHOW MANAGEMENT)</h2>
            </div>
            <div class="mx-auto my-2">
                <button class="btn btn-outline-primary" @click="toggleadd">
                    <i class="bi bi-plus-square fs-1"></i>
                </button>
            </div>
        </div>
        <div id="hiderif" v-if="this.add">
            <h3>Add Theater Details</h3>
            <p v-bind:class="this.messagecolor" v-if="this.message">{{this.message}}</p>
            <button class="btn btn-secondary" @click="toggleadd">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x-lg"
                    viewBox="0 0 16 16">
                    <path
                        d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8 2.146 2.854Z" />
                </svg>
            </button>
            <div class="mb-3">
                <input type="text" placeholder="Name" class="form-control" v-model="form.name">
            </div>
            <div class="mb-3">
                <input type="text" placeholder="Location" class="form-control" v-model="form.location">
            </div>
            <div class="mb-3">
                <input type="number" placeholder="Capacity" classs="form-control" v-model="form.capacity">
            </div>
            <div class="mb-3">
                <button v-bind:class="this.button" @click="addTheater" title="Add New">
                    <i class="bi bi-building-add fs-2"></i>
                </button>
            </div>
        </div>
        <div id="hiderelse" v-else>
            <div v-if="this.data != null && this.data.length > 0" class="row">
                <div class="accordion">
                    <div class="accordion-item bg-dark text-white" v-for="(theater, index) in this.data">
                        <h2 class="accordion-header" :id="'panelsStayOpen-heading-'+index">
                            <button class="accordion-button" type="button" data-bs-toggle="collapse"
                                :data-bs-target="'#panelsStayOpen-collapse-'+index" aria-expanded="true"
                                :aria-controls="'panelsStayOpen-collapse-'+index">
                                <h3>{{theater.name}}</h3>
                            </button>
                        </h2>
                        <div :id="'panelsStayOpen-collapse-'+index" class="accordion-collapse collapse show"
                            :aria-labelledby="'panelsStayOpen-heading'+index">
                            <div class="accordion-body">
                                <div>
                                    <h4>Location: {{theater.location}}</h4>
                                    <p><strong>Capacity:</strong> {{theater.capacity}}</p>
                                    <div class="my-2">
                                        <button class="btn btn-outline-secondary">
                                            <i class="bi bi-filetype-csv fs-5" @click="generateReport(theater.id)">Download Theater Report</i>
                                        </button>
                                        <p v-if="this.mes_csv!=null" :class=this.mes_col>{{this.mes_csv}}</p>
                                    </div>
                                    <div class="my-2">
                                        <button class="btn btn-outline-primary" @click="showmanager(theater.id)"><i
                                                class="bi bi-kanban fs-4"></i> Show Management for
                                            {{theater.name}}</button>
                                    </div>
                                </div>
                                <div v-if="update">
                                    <button class="btn btn-secondary" @click="toggleupdate">
                                        <i class="bi bi-pencil-square fs-3"></i>
                                    </button>
                                    <div class="mb-3">
                                        <input type="text" v-bind:placeholder="theater.name" class="form-control"
                                            v-model="form.name">
                                    </div>
                                    <div class="mb-3">
                                        <input type="text" v-bind:placeholder="theater.location" class="form-control"
                                            v-model="form.location">
                                    </div>
                                    <div class="mb-3">
                                        <input type="number" v-bind:placeholder="theater.capacity" classs="form-control"
                                            v-model="form.capacity">
                                    </div>
                                    <div class="mb-3">
                                        <button class="btn btn-outline-primary" @click="updater(theater.id)"
                                            title="Update">
                                            <i class="bi bi-pen fs-2"></i>
                                        </button>
                                    </div>
                                </div>
                                <div>
                                    <button class="btn btn-outline-warning" @click="toggleupdate" title="update">
                                        <i class="bi bi-pencil-square fs-3"></i>
                                    </button>
                                    <span v-if="theater.shows.length>0">
                                        <p>There are currently active Shows for this theater!</p>
                                        <button class="btn btn-outline-secondary" disabled>
                                            <i class="bi bi-trash3"></i>
                                        </button>
                                    </span>
                                    <span v-else>
                                        <button class="btn btn-outline-danger" @click="remove(theater.id)">
                                            <i class="bi bi-trash3 fs-3"></i>
                                        </button>
                                    </span>
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
    data(){
        return{
            data:null,
            add:false,
            form:{
                name:null,
                location:null,
                capacity:null
            },
            message:null,
            error: false,
            update: false,
            button: "btn btn-primary",
            buttonup: "btn btn-primary",
            messagecolor: "text-danger",
            mes_csv:null,
            mes_col: "text-success"
        }
    },
    methods:{
        toggleadd(){
            console.log("theater toggle add")
            this.add = !this.add
        },
        toggleupdate(){
            this.update = !this.update
        },
        showmanager(id){
            this.$store.state.tid = id
            // this.$store.commit("setID", id)
            this.$router.push('/showm')
        },
        addTheater(){
            this.button = "btn btn-warning"
            this.message=null
            this.error = false
            if (!this.form.name){
                this.message = "name cannot be empty"
                this.messagecolor = "text-danger"
            }
            else if (!this.form.location){
                this.message = "Location cannot be empty"
                this.messagecolor = "text-danger"
            }
            else if(!this.form.capacity){
                this.message = "Capacity cannot be empty!"
                this.messagecolor = "text-danger"

            }
            else{
                if (this.data.length>0){
                    for(var x of this.data){
                        if(x.name==this.form.name){
                            this.error = true
                            this.message = "Theater with same name exists!"
                            this.messagecolor = 'text-danger'
                            break
                        }
                    }  
                }
                if(!this.error){
                    fetch('http://127.0.0.1:5000/theater', {
                        method:"POST",
                        headers:{
                            'Content-Type':'application/json',
                            'Authorization':'Bearer '+localStorage.getItem('auth-token')
                        },
                        body:JSON.stringify(this.form)
                    }).then((res)=>res.json()).then((data)=>{
                        console.log(data)
                        this.message = data.message
                        this.messagecolor = 'text-success'
                        this.button = "btn btn-success"
                        
                        this.data.push({
                            "id":data.id,
                            "name":this.form.name,
                            "location":this.form.location,
                            "capacity":this.form.capacity
                    })}).catch((error)=>{
                        console.log(error)
                    })
                }    
            }
            this.form.name = null
            this.form.location = null
            this.form.capacity = null
            this.button ="btn btn-primary" 
            this.error = false           
        },
        async remove(id){
            const res = await fetch('http://127.0.0.1:5000/theater/'+id, {
                method:"DELETE",
                headers:{
                    "Authorization":"Bearer "+localStorage.getItem('auth-token')
                }
            })
            const data = await res.json()
            if (res.status == 200){
                this.data = this.data.filter(x=>x.id!=id)
            }
        },
        async updater(id){
            var a = this.data.find(x=>(x.id == id))
            if (!this.form.name){
                this.form.name =a.name
            }
            if (!this.form.location){
                this.form.location = a.location
            }
            if(!this.form.capacity){
                this.form.capacity = a.capacity
            }
            var x = this.form
            x.id = id
            console.log(JSON.stringify(this.form))
            const res = await fetch('http://127.0.0.1:5000/theater/'+id, {
                method:"PUT",
                body:JSON.stringify(x),
                headers:{
                    'Content-Type':'application/json',
                    "Authorization":"Bearer "+localStorage.getItem('auth-token')
                }
            })
            const data = await res.json()
            if (res.status == 200){
                this.data = this.data.map(x => {
                    if(x.id==id){
                        x = this.form
                        x.id = id
                    }
                    return x
                })
            }
        },
        generateReport(id){
            fetch(`http://127.0.0.1:5000/theatercsv/${id}`, {
                method:'GET',
                headers:{
                    'Authorization':`Bearer ${localStorage.getItem('auth-token')}`
                }
            }).then((res)=>{
                if (res.ok){
                    this.mes_csv = "Report Generation Initiated! Report will be sent via mail!"
                }
            }).catch((err)=>{
                this.mes_col = "text-danger"
                this.mes_csv = err.json()
            })
        }
    },
    async created(){
        const response = await fetch('http://127.0.0.1:5000/theater', {
            method:'GET',
            headers:{
                'Authorization':'Bearer '+localStorage.getItem('auth-token')
            }
        })
        this.data = await response.json()
    }
}

export default theaters