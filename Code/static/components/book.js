const book = {
    template:`
    <div>
    <div class="container">
    <div>
        <router-link to='/show'>
            <button class="btn btn-outline-info" title="back">
                <i class="bi bi-skip-backward fs-1"></i>
            </button>
        </router-link>
    </div>
    <div>
        <div v-if="this.data.length>0 && this.data[0].availableShows.length>0">
            <div v-for="(show, index) in this.data[0].availableShows" class="col-md-4">
                <div class="card">
                    <div class="card-title">
                        <h4>{{show.date}}</h4>
                    </div>
                    <div class="card-body">
                        <p><strong>Time: </strong>{{show.s_time}}</p>
                        <p><strong>Available Seats: </strong>{{show.seats}}</p>
                        <p><strong>Price/Ticket: </strong>{{show.price}}</p>
                    </div>
                    <div class="card-footer">
                        <button class="btn btn-outline-primary" @click="loads(show.id)" title="Book Show">
                            <i class="bi bi-journal-plus fs-2"></i>
                        </button>
                    </div>
                </div>
            </div>
            <div v-if="this.showform">
                <div>
                    <div class="card my-2 border-warning border-4">
                        <div class="card-body">
                            <div class="input-group mb-3">
                                <span class="input-group-text" id="basic-addon1">Date</span>
                                <input type="text" class="form-control" :placeholder=form.date disabled>
                            </div>
                            <div class="input-group mb-3">
                                <span class="input-group-text" id="basic-addon1">Time</span>
                                <input type="text" class="form-control" :placeholder=form.time disabled>
                            </div>
                            <div class="input-group mb-3">
                                <span class="input-group-text" id="basic-addon1">Seats</span>
                                <input type="text" class="form-control" :placeholder=form.seats v-model="form.seats">
                            </div>
                            <div class="input-group mb-3">
                                <span class="input-group-text" id="basic-addon1">Price</span>
                                <input type="text" class="form-control" :placeholder=this.computedPrice disabled>
                            </div>
                        </div>
                        <div class="card-footer">
                            <button class="btn btn-outline-primary" title="Confirm" @click="bookticket">
                                <i class="bi bi-check fs-2"></i>
                            </button>
                            <div v-if="this.message!=null">
                                {{this.message}}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div v-else>
            There are No available shows!
        </div>
    </div>
</div>
    </div>
    `,
    data(){
        return{
            data:null,
            form:{
                id:null,
                date:null,
                time:null,
                seats:1,
                price:0,
            },
            showform:false,
            computedPrice:0,
            message:null,
            error:false,
        }
    },
    methods:{
        loads(id){
            var x = this.data[0].availableShows.find(i=>(i.id==id))
            console.log(x)
            this.form.id = x.id
            this.form.date=x.date
            this.form.time=x.s_time
            this.form.seats=1
            this.form.price=x.price
            this.showform=true
            this.computedPrice = x.price
            this.message=null
        },
        async bookticket(){
            var x = this.data[0].availableShows.find(i=>(i.id==this.form.id))
            if (this.form.seats > x.seats){
                this.message="The Seat number should be less than equal to the number of available seats!"
            }
            else{
                var form = {
                    "bookedshow":this.form.id,
                    "seats":this.form.seats,
                    "total": this.form.seats*this.form.price
                }
                const res = await fetch('http://127.0.0.1:5000/booking',{
                    method:"POST",
                    body:JSON.stringify(form),
                    headers:{
                        'Content-Type':'application/json',
                        'Authorization':`Bearer ${localStorage.getItem('auth-token')}`
                    }
                })
                this.message = await res.json()
                if (res.status==200){
                    x.seats = x.seats - this.form.seats
                }  
            }
        }
    },
    watch:{
        'form.seats'(newval){
            this.computedPrice = (newval*this.form.price)
        }
    },
    async beforeCreate(){
        const res = await fetch(`http://127.0.0.1:5000/shows/${this.$store.getters.getSID}`,{
            method:'GET',
            headers:{
                'Authorization':`Bearer ${localStorage.getItem('auth-token')}`
            }
        })
        this.data = await res.json()
    }
}
export default book