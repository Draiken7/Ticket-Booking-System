const user = {
    template:
    `
<div>
<div class="container">
    <div class="my-2">
        <router-link to="/bookings">
            <button class="btn btn-outline-dark">
                <i class="bi bi-file-earmark-spreadsheet">Your Bookings</i>
            </button>
        </router-link>
    </div>
    <div class="row g-3">
        <div class="col-md-6">
            <div class="row">
                <div class="col-auto">
                    <label for="theater-movie-dropdown" class="col-form-label">Theater/Movie</label>
                </div>
                <div class="col">
                    <select name="theater-movie-dropdown" id="theaterMovieDropdown" class="form-select" v-model="obj">
                        <option value="theater">Search Theater</option>
                        <option value="movie">Search Movie</option>
                    </select>
                </div>
            </div>
        </div>
        <div class="col-md-6">
            <div class="row">

                <div class="col-auto">
                    <label for="location-tag-dropdown" class="col-form-label">Search By:</label>
                </div>
                <div v-if="this.optionmarker==0">
                    <div class="col">
                        <select name="location-tag-dropdown" id="locationTagDropdown" class="form-select" v-model="form.name">
                            <option v-for="(option, index) in this.option.theater" :value=option>{{option}}</option>
                        </select>
                    </div>
                </div>
                <div v-else-if="this.optionmarker==1">
                    <div class="col">
                        <select name="location-tag-dropdown" id="locationTagDropdown" class="form-select" v-model="form.name">
                            <option v-for="(option, index) in this.option.movie" :value=option>{{option}}</option>
                        </select>
                    </div>
                </div>
                <div v-else>
                    <div class="col">
                        <select name="location-tag-dropdown" id="locationTagDropdown" class="form-select" v-model="form.name" disabled>
                            <option v-for="(option, index) in this.option.theater" :value=option>{{option}}</option>
                        </select>
                    </div>
                </div>
            </div>
        </div>

        <div class="col-auto">

            <div class="row g-3 align-items-center">
                <div class="col-auto">
                    <label for="inputPassword6" class="col-form-label">Search</label>
                </div>
                <div v-if="this.searchmarker==0">
                    <div class="col-auto">
                        <input type="text" id="searchBox" class="form-control" v-model="form.value">
                    </div>
                </div>
                <div v-else-if="this.searchmarker==1">
                    <div class="col-auto">
                        <input type="text" id="searchBox" class="form-control" v-model="form.value">
                    </div>
                </div>
                <div v-else-if="this.searchmarker==2">
                    <div class="col-auto">
                        <select name="location-tag-dropdown" id="locationTagDropdown" class="form-select" v-model="form.value">
                            <option v-for="(rt, index) in this.rating" :value=rt>{{rt}}</option>
                        </select>
                    </div>
                </div>
                <div v-else-if="this.searchmarker==3">
                    <div class="col-auto">
                        <input type="number" id="searchBox" class="form-control" v-model="form.value">
                    </div>
                </div>
                <div v-else-if="this.searchmarker==4">
                    <div class="col-auto">
                        <input type="text" id="searchBox" class="form-control" v-model="form.value">
                    </div>
                </div>
                <div v-else-if="this.searchmarker==5">
                    <div class="col-auto">
                        <input type="text" id="searchBox" class="form-control" v-model="form.value">
                    </div>
                </div>
                <div v-else>
                    <div class="col-auto">
                        <input type="text" id="searchBox" class="form-control" disabled>
                    </div>
                </div>
            </div>
        </div>

        <div v-if="this.searchbutton">
            <div class="col-auto">
                <button class="btn btn-outline-primary" title="Search" @click="search">
                    <i class="bi bi-search fs-2"></i>
                </button>
            </div>
        </div>
        <div v-else>
            <div class="col-auto">
                <button class="btn btn-outline-secondary" disabled>
                    <i class="bi bi-search fs-2"></i>
                </button>
            </div>
        </div>
    </div>
    <div>
        </br>
            <h3 v-if="!this.header">NEW RELEASES!</h3>
            <h3 v-else>RESULTS!</h3>
        </br>
    </div>
    <div v-if="this.data.length > 0">
        <div class="row">
            <div v-for="(movies, index) in this.data" class="col-md-4">
                <div class="card">
                    <div class="card-title">
                        <h4>{{movies.name}}</h4>
                    </div>
                    <div class="card-body">
                        <p><strong>User Rating: </strong>{{movies.userRating}}</p>
                        <p><strong>Rating: </strong>{{movies.rating}}</p>
                        <p><strong>Duration: </strong>{{movies.duration}}</p>
                        <p><strong>Taggs: </strong>{{movies.tags}}</p>
                    </div>
                    <div class="card-footer">
                        <a class="stretched-link" @click="movieshow(movies.id)"></a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
</div>
    `,
    data() {
        return{
            data:null,
            obj:null,
            form:{
                name:null,
                value:null,
            },
            option:{
                theater:['location', 'title'],
                movie:['name', 'tags', 'rating', 'userRating']
            },
            optionmarker:3,
            searchmarker:9,
            searchbutton:false,
            rating:['G', 'PG', 'PG-13', 'R', 'NC-17', '14A'],
            header:false,
        }
    },
    methods: {
        movieshow(id){
            this.$store.commit("setMID", id)
            this.$store.commit("setQueryParam", "movieid")
            this.$router.push('/show')
        },
        async search(){
            const res = await fetch(`http://127.0.0.1:5000/shows?name=${this.form.name}&value=${this.form.value}`, {
                method:'GET',
                headers:{
                    'Authorization': `Bearer ${localStorage.getItem('auth-token')}`
                }
            })
            this.data = await res.json()
            if (this.data.length>0){
                this.header=true
            }
        }
    },
    watch:{
        obj(newval){
            if(newval == "theater"){
                this.optionmarker = 0
            }
            else if(newval == "movie"){
                this.optionmarker = 1
            }
            else{
                this,optionmarker = 3
            }
        },
        'form.name'(newval){
            if (newval == 'name'){
                this.searchmarker = 0
            }
            else if (newval == 'tags'){
                this.searchmarker = 1
            }
            else if (newval == 'rating'){
                this.searchmarker = 2
            }
            else if (newval == 'userRating'){
                this.searchmarker = 3
            }
            else if (newval == 'location'){
                this.searchmarker = 4
            }
            else if (newval == 'title'){
                this.searchmarker = 5
            }
            else{
                this.searchmarker = 9
            }
        },
        'form.value'(newval){
            if(!newval){
                this.searchbutton = false
            }
            else{
                this.searchbutton = true
            }
        }
    },
    async created(){
        const two = await fetch("http://127.0.0.1:5000/recent", {
            method:'GET',
            headers:{
                'Authorization':"Bearer "+localStorage.getItem('auth-token')
            }
        })
        this.data = await two.json()
    },
}

export default user